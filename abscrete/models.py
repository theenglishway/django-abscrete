from collections import OrderedDict, defaultdict
import functools
import sys

from django.db.models.query import QuerySet, ModelIterable
from django.db import models
from django.db.models.base import ModelBase
from django.utils import six


def abscrete_application_ready(app):
    for m in app.get_models():
        if AbscreteType.is_abscrete(m):
            m._abscrete.tree.prune(m)


# Recursive setattr/getattr functions : https://stackoverflow.com/a/31174427
def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


sentinel = object()
def rgetattr(obj, attr, default=sentinel):
    if default is sentinel:
        _getattr = getattr
    else:
        def _getattr(obj, name):
            return getattr(obj, name, default)
    return functools.reduce(_getattr, [obj]+attr.split('.'))


class AbscreteType:
    """
    Handle for type management within abscrete app
    """
    #: Model that is the base for all the roots (ie the model exported by this
    # app, 'AbstractModel'
    GROUND = 'ground'
    #: Model that is a direct child of the 'ground' AbstractModel
    ROOT = 'root'
    #: Intermediate model whose instances won't be immediately accessible
    NODE = 'node'
    #: Actual concrete models
    LEAF = 'leaf'

    @classmethod
    def is_abscrete(cls, model):
        return hasattr(model, '_abscrete')

    @classmethod
    def get_type(cls, bases):
        """
        Since the tree is build from the 'ground' down to the leaves, there is
        absolutely no way to distinguish a node from a leaf while the class is
        being build (the only way would be to check whether a model is
        subclassed but that information is not available since a parent class
        is build before its potential subclasses).
        The detection of leaves is made within AbstractTree.prune, once the
        shape of the whole tree is known.

        :param bases: The base classes of the model
        :return: The type of the model
        """
        if models.Model in bases:
            return cls.GROUND

        if any((b._abscrete.type == cls.GROUND for b in bases)):
            return cls.ROOT

        return cls.NODE


class AbscreteBranch(list):
    """
    Representation of the branch leading to a given node/leaf, with some
    additional handy attributes.
    """
    @classmethod
    def _get_parent(cls, bases):
        for b in bases:
            if AbscreteType.is_abscrete(b):
                return b

        return None

    @classmethod
    def get(cls, bases):
        branch = []

        parent = cls._get_parent(bases)
        while parent and parent._abscrete.type != AbscreteType.GROUND:
            branch.append(parent)
            parent = cls._get_parent(parent.__bases__)

        return AbscreteBranch(branch)

    @property
    def empty(self):
        return self == []

    @property
    def root(self):
        return self[-1] if not self.empty else None

    @property
    def parent(self):
        return self[0] if not self.empty else None

    @property
    def up(self):
        return self

    @property
    def down(self):
        return list(reversed(self))

    def path_from_root(self, model):
        if isinstance(model, str):
            model_name = model
        elif issubclass(model, AbscreteModel):
            model_name = model._abscrete.model_name

        return '.'.join([n._abscrete.model_name for n in self.down] + [model_name])


class AbscreteTree(OrderedDict):
    """
    Representation of the abscrete inheritance tree, as a cascade of
    OrderedDict. It will e.g. look like :
        {
            root1: {
                node11 : {
                    leaf111: {},
                    leaf112: {}
                },
                node12 : {
                    leaf121: {}
                }
            },
            root2: {
                leaf21: {},
                leaf22: {}
            }
        }
    """
    def __init__(self, *args, **kwargs):
        super(AbscreteTree, self).__init__(*args, **kwargs)
        self._by_str = {}

    def _get_parent_node(self, key):
        parent_node = self
        for i in key._abscrete.branch.down:
            parent_node = parent_node[i]
        return parent_node

    def __setitem__(self, key, value, **kwargs):
        parent_node = self._get_parent_node(key)
        
        if parent_node == self:
            super(AbscreteTree, self).__setitem__(key, value, **kwargs)
        else:
            parent_node.__setitem__(key, value, **kwargs)

    def __getitem__(self, item):
        parent_node = self._get_parent_node(item)

        if parent_node == self:
            return super(AbscreteTree, self).__getitem__(item)
        else:
            return parent_node.__getitem__(item)

    def __delitem__(self, key, **kwargs):
        raise NotImplementedError('Cannot delete items from AbscreteTree')

    def add(self, model):
        """
        Add model to the tree

        :param model: self-explanatory
        :return: none
        """
        self[model] = OrderedDict()
        self._by_str[model._abscrete.branch.path_from_root(model)] = model

    def prune(self, model):
        """
        Turn model previously marked as node into leaf, if it doesn't have any
        children nodes.
        This function MUST be called once the whole tree has been built,
        typically when the application is ready.

        :param model: self-explanatory
        :return: none
        """
        if self[model] == OrderedDict():
            model._abscrete.type = AbscreteType.LEAF

    def get_model(self, branch_as_str):
        return self._by_str[branch_as_str]


class AbscreteMeta:
    def __init__(self, model_name, type, branch, tree):
        self.model_name = model_name
        self.type = type
        self.branch = branch
        self.tree = tree

    @property
    def field_name(self):
        if self.type == AbscreteType.NODE or self.type == AbscreteType.LEAF:
            root_model_name = self.branch.root._meta.model_name
        else:
            root_model_name = self.model_name
        return self.to_field_name(root_model_name)

    @property
    def field_value(self):
        if self.type == AbscreteType.LEAF:
            return self.branch.path_from_root(self.model_name)

        raise TypeError(
            'The field_value property can not be determined on {}, because it '
            'is not a leaf but a {}'.format(
                self.model_name, self.type
            )
        )

    @staticmethod
    def to_field_name(model_name):
        return 'abscrete_type_%s' % model_name


class AbscreteModelBase(ModelBase):
    TYPE_FIELD_MAX_LENGTH = 200
    tree = AbscreteTree()

    def __new__(cls, name, bases, attrs):
        model_name = name.lower()
        type = AbscreteType.get_type(bases)

        attrs.update({
            '_abscrete': AbscreteMeta(
                model_name=model_name,
                type=type,
                branch=AbscreteBranch.get(bases),
                tree=cls.tree
            )
        })

        if type == AbscreteType.ROOT:
            attrs.update({
                AbscreteMeta.to_field_name(model_name): models.CharField(
                    max_length=cls.TYPE_FIELD_MAX_LENGTH
                )
            })

        new_class = super(AbscreteModelBase, cls).__new__(cls, name, bases, attrs)
        if type != AbscreteType.GROUND:
            cls.tree.add(new_class)

        if new_class._abscrete.type == AbscreteType.NODE:
            def __init__(self, *args, **kwargs):
                super(new_class, self).__init__(*args, **kwargs)

                abscrete = self._abscrete
                if abscrete.type == AbscreteType.LEAF:
                    field_name = abscrete.field_name
                    field_value = abscrete.field_value

                    if len(field_value) > cls.TYPE_FIELD_MAX_LENGTH:
                        raise ValueError(
                            "Abscrete field value {} for model {} exceeds "
                            "abscrete field's max length ({} > {})".format(
                                field_value, name,
                                len(field_value), cls.TYPE_FIELD_MAX_LENGTH
                            )
                        )
                    setattr(self, field_name, field_value)

            new_class.__init__ = __init__

        return new_class


class AbscreteIterable(ModelIterable):
    #: Type of the model
    type = None

    def __iter__(self):
        if self.type == AbscreteType.LEAF:
            # If the model is a leaf, the iterator of ModelIterable returns
            # instances of the leaf model, which is the actual concrete model,
            # so there's nothing left to do.
            return super(AbscreteIterable, self).__iter__()
        else:
            # If the model is not a leaf, the iterator of ModelIterable returns
            # instances of an intermediate node's or the root's model, so a
            # generator with the concrete instance is returned instead
            return self._abscrete_iterator(super(AbscreteIterable, self).__iter__())

    def _abscrete_iterator(self, base_iter):
        """
        Directly getting the abscrete instance for each object in the base
        iterator would be a nightmare in terms of SQL queries : instead, we
        build for each concrete model a list of the PKs to retrieve, and once
        those lists are built, a single query is made by database table. Then
        the now-correctly typed objects are yield in the same order as they were
        output by the original iterator.

        The principle is shamelessly copied from django-polymorphic
        """
        base_objects = defaultdict(list)
        ordered_pks = []
        ordered_results = {}

        while True:
            try:
                o = next(base_iter)
                concrete_model = o._abscrete.tree.get_model(o.abscrete_branch)
                base_objects[concrete_model].append(o.pk)
                ordered_pks.append(o.pk)
            except StopIteration:
                for o_type, pks in base_objects.items():
                    for r in o_type.objects.filter(pk__in=pks):
                        ordered_results[r.pk] = r

                for pk in ordered_pks:
                    yield ordered_results[pk]

                return


class AbscreteQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        super(AbscreteQuerySet, self).__init__(*args, **kwargs)

        # Overwriting the class responsible for turning database rows into
        # models allows controlling which instances are returned in all methods
        # of the queryset, be it those returning another queryset (all, filter,
        # exclude, ..) or those returning an instance (get, first, ...)
        self._iterable_class = type(
            "{}AbscreteIterable".format(self.model.__name__),
            (AbscreteIterable,),
            {'type': self.model._abscrete.type}
        )

def split_on(string, char, max):
    """
    :return: at most max splits of string using character 'char' (see Python3's
             split function with maxsplit argument)
    """
    if sys.version_info[0] == 2:
        split = string.split(char)
        return split[:max] + [char.join(split[max:])]

    elif sys.version_info[0] == 3:
        return string.split(char, maxsplit=max)


class AbscreteModel(six.with_metaclass(AbscreteModelBase, models.Model)):
    class Meta:
        abstract = True

    objects = AbscreteQuerySet.as_manager()

    @property
    def abscrete_field_name(self):
        """
        :return: the name of the ORM's field used to hold information regarding
        the abscrete model (typically *rootname*_type)
        """
        return self._abscrete.field_name

    @property
    def abscrete_branch(self):
        """
        :return: the branch leading to the concrete model to use for that
        particular instance (in the form
        *roottype*.*node1type*.*node2type*.(...).*leaftype*)
        """
        return getattr(self, self.abscrete_field_name)

    @property
    def abscrete_instance(self):
        """
        Warning ! Using this property is costly on the first call (one database
        hit per intermediate node) and usually not required since the queries
        made on the parent model already returns the object with its correct
        type

        :return: the concrete instance with the proper type, retrieved using
        the chain of fields that Django automatically adds in OneToOneField
        """
        _, model = split_on(self.abscrete_branch, '.', 1)
        return rgetattr(self, model)
