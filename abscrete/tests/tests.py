from collections import OrderedDict

from django.test import TestCase

from model_mommy import mommy

from abscrete.models import (AbscreteMeta, AbscreteType, AbscreteTree)
import abscrete.tests.models as tm


for m in [tm.PlainRoot, tm.PlainLeaf1, tm.PlainLeaf2, tm.PlainLeaf3,
          tm.RootWithOneNode, tm.IntermediateNode,
          tm.LeafWithIntermediate1, tm.LeafWithIntermediate2,
          tm.LeafWithIntermediate3, tm.LeafWithIntermediate4]:
    m._abscrete.tree.prune(m)


class AbscreteTestCase(TestCase):
    #: A list of the root models for the test case
    roots = None
    #: The part of the tree that is immediately below the root models, in the
    # form of a dictionnary of OrderedDict()
    tree = None
    #: A dictionary of the leaves of the test case, with the leaf class as key
    # and the branch leading up to the root as value
    leaves = None
    #: A dictionary of the nodes of the test case, with the node class as key
    # and the branch leading up to the root as value
    nodes = None


# Definition of all the test cases data

class OnePlainRoot(AbscreteTestCase):
    """
    In those tests, there is a single root which has a couple of leafs. This is
    the simplest setup.
    """
    @classmethod
    def setUpTestData(cls):
        cls.roots = [tm.PlainRoot]
        cls.tree = {
            tm.PlainRoot: OrderedDict(
                [(tm.PlainLeaf1, OrderedDict()),
                 (tm.PlainLeaf2, OrderedDict()),
                 (tm.PlainLeaf3, OrderedDict())]
            )
        }
        cls.leaves = {
            tm.PlainLeaf1: [tm.PlainRoot],
            tm.PlainLeaf2: [tm.PlainRoot],
            tm.PlainLeaf3: [tm.PlainRoot],
        }
        cls.nodes = {}


class SeveralPlainRoots(AbscreteTestCase):
    """
    In those tests, there are several roots, each of them having a couple of
    leaves directly below them
    """
    @classmethod
    def setUpTestData(cls):
        cls.roots = [tm.SeveralPlainRoot1,
                     tm.SeveralPlainRoot2,
                     tm.SeveralPlainRoot3]
        cls.tree = {
            tm.SeveralPlainRoot1: OrderedDict(
                [(tm.SeveralPlainLeaf11, OrderedDict()),
                 (tm.SeveralPlainLeaf12, OrderedDict())]
            ),
            tm.SeveralPlainRoot2: OrderedDict(
                [(tm.SeveralPlainLeaf21, OrderedDict()),
                 (tm.SeveralPlainLeaf22, OrderedDict())]
            ),
            tm.SeveralPlainRoot3: OrderedDict(
                [(tm.SeveralPlainLeaf31, OrderedDict()),
                 (tm.SeveralPlainLeaf32, OrderedDict())]
            )
        }
        cls.leaves = {
            tm.SeveralPlainLeaf11: [tm.SeveralPlainRoot1],
            tm.SeveralPlainLeaf12: [tm.SeveralPlainRoot1],
            tm.SeveralPlainLeaf21: [tm.SeveralPlainRoot2],
            tm.SeveralPlainLeaf22: [tm.SeveralPlainRoot2],
            tm.SeveralPlainLeaf31: [tm.SeveralPlainRoot3],
            tm.SeveralPlainLeaf32: [tm.SeveralPlainRoot3]
        }
        cls.nodes = {}


class OneIntermediateNode(AbscreteTestCase):
    """
    Those tests feature an intermediate node, which has several leafs below it.
    """
    @classmethod
    def setUpTestData(cls):
        cls.roots = [tm.RootWithOneNode]
        cls.tree = {
            tm.RootWithOneNode: OrderedDict(
                [(tm.IntermediateNode, OrderedDict(
                    [(tm.LeafWithIntermediate1, OrderedDict()),
                     (tm.LeafWithIntermediate2, OrderedDict()),
                     (tm.LeafWithIntermediate3, OrderedDict()),
                     (tm.LeafWithIntermediate4, OrderedDict())]
                ))]
            )
        }
        cls.leaves = {
            tm.LeafWithIntermediate1: [tm.IntermediateNode, tm.RootWithOneNode],
            tm.LeafWithIntermediate2: [tm.IntermediateNode, tm.RootWithOneNode],
            tm.LeafWithIntermediate3: [tm.IntermediateNode, tm.RootWithOneNode],
            tm.LeafWithIntermediate4: [tm.IntermediateNode, tm.RootWithOneNode]
        }
        cls.nodes = {
            tm.IntermediateNode: [tm.RootWithOneNode]
        }


class SeveralIntermediateNodes(AbscreteTestCase):
    """
    Those tests have a cascade of intermediate nodes, with a single leaf at the
    end.
    """
    @classmethod
    def setUpTestData(cls):
        cls.roots = [tm.RootWithSeveralNodes]
        cls.tree = {
            tm.RootWithSeveralNodes: OrderedDict(
                [(tm.IntermediateNode1, OrderedDict(
                    [(tm.IntermediateNode2, OrderedDict(
                        [(tm.IntermediateNode3, OrderedDict(
                            [(tm.LeafWithSeveralIntermediate, OrderedDict())]
                        ))]
                    ))]
                ))]
            )
        }
        cls.leaves = {
            tm.LeafWithSeveralIntermediate: [tm.IntermediateNode3,
                                             tm.IntermediateNode2,
                                             tm.IntermediateNode1,
                                             tm.RootWithSeveralNodes]
        }
        cls.nodes = {
            tm.IntermediateNode3: [tm.IntermediateNode2,
                                   tm.IntermediateNode1,
                                   tm.RootWithSeveralNodes],
            tm.IntermediateNode2: [tm.IntermediateNode1,
                                   tm.RootWithSeveralNodes],
            tm.IntermediateNode1: [tm.RootWithSeveralNodes],
        }


class RandomTree(AbscreteTestCase):
    """
    This test has no particular logic but mixes all kinds of tree structures to
    see if everything goes well.
    """
    @classmethod
    def setUpTestData(cls):
        cls.roots = [tm.Root1,
                     tm.Root2]
        cls.tree = {
            tm.Root1: OrderedDict(
                [(tm.Leaf11, OrderedDict()),
                 (tm.Node11, OrderedDict(
                     [(tm.Leaf111, OrderedDict()),
                      (tm.Leaf112, OrderedDict())]
                 ))]
            ),
            tm.Root2: OrderedDict(
                [(tm.Node21, OrderedDict(
                    [(tm.Node211, OrderedDict(
                            [(tm.Leaf2111, OrderedDict())]
                    )),
                     (tm.Leaf211, OrderedDict())]
                ))]
            )
        }
        cls.leaves = {
            tm.Leaf11: [tm.Root1],
            tm.Leaf111: [tm.Node11, tm.Root1],
            tm.Leaf112: [tm.Node11, tm.Root1],
            tm.Leaf2111: [tm.Node211, tm.Node21, tm.Root2],
            tm.Leaf211: [tm.Node21, tm.Root2]
        }
        cls.nodes = {
            tm.Node11: [tm.Root1],
            tm.Node21: [tm.Root2],
            tm.Node211: [tm.Node21, tm.Root2]
        }


# Definition of the actual test functions

class AbscreteMetaTest:
    def _test_common_attributes(self, model):
        self.assertTrue(hasattr(model, '_abscrete'))

        abscrete = model._abscrete
        self.assertTrue(isinstance(abscrete, AbscreteMeta))
        self.assertIsNotNone(abscrete.type)
        self.assertIsNotNone(abscrete.tree)
        self.assertTrue(isinstance(abscrete.tree, AbscreteTree))

    def _test_non_root_attributes(self, abscrete, branch):
        self.assertEqual(abscrete.branch, branch)
        self.assertEqual(abscrete.branch.parent, branch[0] if branch else None)
        self.assertEqual(abscrete.branch.root, branch[-1] if branch else None)

        for r in self.roots:
            self.assertEqual(abscrete.tree[r], self.tree[r])

    def test_roots(self):
        for r in self.roots:
            self._test_common_attributes(r)

            abscrete = r._abscrete
            self.assertEqual(abscrete.type, AbscreteType.ROOT)
            self.assertIsNone(abscrete.branch.root)
            self.assertEqual(abscrete.branch, [])

    def test_nodes(self):
        for n, branch in self.nodes.items():
            self._test_common_attributes(n)

            abscrete = n._abscrete
            self.assertEqual(abscrete.type, AbscreteType.NODE)
            self._test_non_root_attributes(abscrete, branch)

    def test_leaves(self):
        for l, branch in self.leaves.items():
            self._test_common_attributes(l)

            abscrete = l._abscrete
            self.assertEqual(abscrete.type, AbscreteType.LEAF)
            self._test_non_root_attributes(abscrete, branch)


class AbscreteModelTest(object):
    @classmethod
    def setUpTestData(cls):
        super(AbscreteModelTest, cls).setUpTestData()
        cls.leaf_instances = [
            (mommy.make(kls), branch) for kls, branch in cls.leaves.items()
        ]

    def test_abscrete_branch(self):
        for l, branch in self.leaf_instances:
            root = branch[-1]
            self.assertTrue(
                hasattr(l, 'abscrete_field_name'),
                'leaves should have a abscrete_field_name attribute'
            )
            self.assertEqual(
                l.abscrete_field_name,
                'abscrete_type_%s' % root.__name__.lower()
            )
            self.assertTrue(
                hasattr(l, 'abscrete_branch'),
                'leaves should have a abscrete_branch attribute'
            )
            self.assertEqual(
                l.abscrete_branch,
                '.'.join(
                    [n.__name__.lower() for n in reversed(l._abscrete.branch)]
                    + [l.__class__.__name__.lower()]
                )
            )

    def test_abscrete_instance(self):
        for l, branch in self.leaf_instances:
            root = branch[-1]
            root_instance = getattr(l, '%s_ptr' % root.__name__.lower())

            self.assertTrue(isinstance(root_instance, branch[-1]))
            self.assertEqual(root_instance.abscrete_instance, l)


class AbstractQuerySetTest(object):
    @classmethod
    def setUpTestData(cls):
        super(AbstractQuerySetTest, cls).setUpTestData()
        cls.leaves_instances = [
            (kls, branch[-1], mommy.make(kls, _quantity=5))
            for kls, branch in cls.leaves.items()
        ]

    def _test_root_queryset(self, root, leaves_list):
        qs = root.objects.all()
        self.assertSetEqual(set(leaves_list), set(qs))
        self.assertSequenceEqual(leaves_list, qs)

    def _test_leaf_queryset(self, leaf, leaves_list):
        qs = leaf.objects.all()
        self.assertSetEqual(set(qs), set(leaves_list))
        self.assertSequenceEqual(leaves_list, qs)

    def test_root_queryset(self):
        leaves_by_root = {
            r: [l for _, l_root, list in self.leaves_instances
                if l_root == r for l in list]
            for r in self.roots
        }
        for root, leaves_list in leaves_by_root.items():
            self._test_root_queryset(root, leaves_list)

    def test_leaves_queryset(self):
        for kls, _, list in self.leaves_instances:
            self._test_leaf_queryset(kls, list)


# Concrete implementation of the tests which combine some standard data set-up
# and the actual test functions

class AbscreteMetaTestPlain(AbscreteMetaTest, OnePlainRoot):
    pass
class AbscreteMetaSeveralPlainTest(AbscreteMetaTest, SeveralPlainRoots):
    pass
class AbscreteMetaOneIntermediateNodeTest(AbscreteMetaTest, OneIntermediateNode):
    pass
class AbscreteMetaSeveralIntermediateNodesTest(AbscreteMetaTest, SeveralIntermediateNodes):
    pass
class AbscreteMetaRandomTreeTest(AbscreteMetaTest, RandomTree):
    pass

class AbscreteModelTestPlain(AbscreteModelTest, OnePlainRoot):
    pass
class AbscreteModelTestSeveralPlain(AbscreteModelTest, SeveralPlainRoots):
    pass
class AbscreteModelTestOneIntermediateNode(AbscreteModelTest, OneIntermediateNode):
    pass
class AbscreteModelTestSeveralIntermediateNodes(AbscreteModelTest, SeveralIntermediateNodes):
    pass
class AbscreteModelTestRandomTree(AbscreteModelTest, RandomTree):
    pass

class AbscreteQuerySetTestPlain(AbstractQuerySetTest, OnePlainRoot):
    pass
class AbscreteQuerySetTestSeveralPlain(AbstractQuerySetTest, SeveralPlainRoots):
    pass
class AbscreteQuerySetTestOneIntermediateNode(AbstractQuerySetTest, OneIntermediateNode):
    pass
class AbscreteQuerySetTestSeveralIntermediateNodes(AbstractQuerySetTest, SeveralIntermediateNodes):
    pass
class AbscreteQuerySetTestRandomTree(AbstractQuerySetTest, RandomTree):
    pass


class OneToOneRelationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root1_instances = {
            tm.O2ORelationLeaf11: mommy.make(tm.O2ORelationLeaf11, _quantity=2),
            tm.O2ORelationLeaf12: mommy.make(tm.O2ORelationLeaf12, _quantity=2),
        }
        cls.root2_instances = {
            tm.O2ORelationLeaf21: {
                tm.O2ORelationLeaf11: mommy.make(
                    tm.O2ORelationLeaf21,
                    o2orelationroot1=cls.root1_instances[tm.O2ORelationLeaf11][0]
                ),
                tm.O2ORelationLeaf12: mommy.make(
                    tm.O2ORelationLeaf21,
                    o2orelationroot1=cls.root1_instances[tm.O2ORelationLeaf12][0]
                ),
            },
            tm.O2ORelationLeaf22: {
                tm.O2ORelationLeaf11: mommy.make(
                    tm.O2ORelationLeaf22,
                    o2orelationroot1=cls.root1_instances[tm.O2ORelationLeaf11][1]
                ),
                tm.O2ORelationLeaf12: mommy.make(
                    tm.O2ORelationLeaf22,
                    o2orelationroot1=cls.root1_instances[tm.O2ORelationLeaf12][1]
                ),
            },
        }

    def test_subclassing(self):
        for kls, instances in self.root2_instances.items():
            for related_class, i in instances.items():
                self.assertTrue(isinstance(i.o2orelationroot1, related_class))

        for kls, list in self.root1_instances.items():
            for i in list:
                related_to = i.o2orelationroot2
                self.assertNotEqual(related_to.__class__, tm.O2ORelationRoot2)
                self.assertIn(related_to.__class__,
                              [tm.O2ORelationLeaf21, tm.O2ORelationLeaf22])


class ForeignRelationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root1_instances = {
            tm.ForeignRelationLeaf11: mommy.make(tm.ForeignRelationLeaf11),
            tm.ForeignRelationLeaf12: mommy.make(tm.ForeignRelationLeaf12),
        }
        cls.root2_instances = {
            tm.ForeignRelationLeaf21: {
                tm.ForeignRelationLeaf11: mommy.make(
                    tm.ForeignRelationLeaf21,
                    foreignrelationroot1=cls.root1_instances[tm.ForeignRelationLeaf11]
                ),
                tm.ForeignRelationLeaf12: mommy.make(
                    tm.ForeignRelationLeaf21,
                    foreignrelationroot1=cls.root1_instances[tm.ForeignRelationLeaf12]
                ),
            },
            tm.ForeignRelationLeaf22: {
                tm.ForeignRelationLeaf11: mommy.make(
                    tm.ForeignRelationLeaf22,
                    foreignrelationroot1=cls.root1_instances[tm.ForeignRelationLeaf11]
                ),
                tm.ForeignRelationLeaf12: mommy.make(
                    tm.ForeignRelationLeaf22,
                    foreignrelationroot1=cls.root1_instances[tm.ForeignRelationLeaf12]
                ),
            },
        }

    def test_subclassing(self):
        for kls, instances in self.root2_instances.items():
            for related_class, i in instances.items():
                self.assertTrue(isinstance(i.foreignrelationroot1, related_class))

        for kls, i in self.root1_instances.items():
            for related_to in i.foreignrelationroot2_set.all():
                self.assertNotEqual(related_to.__class__, tm.ForeignRelationRoot2)
                self.assertIn(related_to.__class__,
                              [tm.ForeignRelationLeaf21, tm.ForeignRelationLeaf22])


class M2MRelationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root1_instances = {
            tm.M2MRelationLeaf11: mommy.make(tm.M2MRelationLeaf11),
            tm.M2MRelationLeaf12: mommy.make(tm.M2MRelationLeaf12),
        }
        cls.root2_instances = {
            tm.M2MRelationLeaf21: mommy.make(tm.M2MRelationLeaf21),
            tm.M2MRelationLeaf22: mommy.make(tm.M2MRelationLeaf22),
        }
        cls.root2_instances[tm.M2MRelationLeaf21].m2mrelationroot1_set.add(
            cls.root1_instances[tm.M2MRelationLeaf11]
        )
        cls.root2_instances[tm.M2MRelationLeaf21].m2mrelationroot1_set.add(
            cls.root1_instances[tm.M2MRelationLeaf12]
        )
        cls.root2_instances[tm.M2MRelationLeaf22].m2mrelationroot1_set.add(
            cls.root1_instances[tm.M2MRelationLeaf11]
        )
        cls.root2_instances[tm.M2MRelationLeaf22].m2mrelationroot1_set.add(
            cls.root1_instances[tm.M2MRelationLeaf12]
        )

    def test_subclassing(self):
        for kls, i in self.root1_instances.items():
            for related in i.m2mrelationroot2_set.all():
                self.assertNotEqual(related.__class__, tm.M2MRelationRoot2)
                self.assertIn(related.__class__,
                              [tm.M2MRelationLeaf21, tm.M2MRelationLeaf22])

        for kls, i in self.root2_instances.items():
            for related in i.m2mrelationroot1_set.all():
                self.assertNotEqual(related.__class__, tm.M2MRelationRoot1)
                self.assertIn(related.__class__,
                              [tm.M2MRelationLeaf11, tm.M2MRelationLeaf12])
