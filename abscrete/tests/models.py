from django.db import models

# Create your models here.
from abscrete.models import AbscreteModel

# Test with just a root and a few leaves

class PlainRoot(AbscreteModel):
    field1 = models.IntegerField()

class PlainLeaf1(PlainRoot):
    field11 = models.PositiveIntegerField()

class PlainLeaf2(PlainRoot):
    field12 = models.TextField()

class PlainLeaf3(PlainRoot):
    field13 = models.CharField(max_length=10)

# Test with several roots

class SeveralPlainRoot1(AbscreteModel):
    pass

class SeveralPlainLeaf11(SeveralPlainRoot1):
    pass
class SeveralPlainLeaf12(SeveralPlainRoot1):
    pass

class SeveralPlainRoot2(AbscreteModel):
    pass

class SeveralPlainLeaf21(SeveralPlainRoot2):
    pass
class SeveralPlainLeaf22(SeveralPlainRoot2):
    pass

class SeveralPlainRoot3(AbscreteModel):
    pass

class SeveralPlainLeaf31(SeveralPlainRoot3):
    pass
class SeveralPlainLeaf32(SeveralPlainRoot3):
    pass

# Test with one intermediate node

class RootWithOneNode(AbscreteModel):
    field2 = models.URLField()

class IntermediateNode(RootWithOneNode):
    pass

class LeafWithIntermediate1(IntermediateNode):
    pass
class LeafWithIntermediate2(IntermediateNode):
    pass
class LeafWithIntermediate3(IntermediateNode):
    pass
class LeafWithIntermediate4(IntermediateNode):
    pass

# Test with several intermediate nodes

class RootWithSeveralNodes(AbscreteModel):
    pass
class IntermediateNode1(RootWithSeveralNodes):
    pass
class IntermediateNode2(IntermediateNode1):
    pass
class IntermediateNode3(IntermediateNode2):
    pass
class LeafWithSeveralIntermediate(IntermediateNode3):
    pass

# Test with no particular structure, but all kinds of tree structures

class Root1(AbscreteModel):
    pass
class Leaf11(Root1):
    pass
class Node11(Root1):
    pass
class Leaf111(Node11):
    pass
class Leaf112(Node11):
    pass

class Root2(AbscreteModel):
    pass
class Node21(Root2):
    pass
class Node211(Node21):
    pass
class Leaf2111(Node211):
    pass
class Leaf211(Node21):
    pass

# Test with one-to-one relations between models

class O2ORelationRoot1(AbscreteModel):
    pass
class O2ORelationLeaf11(O2ORelationRoot1):
    pass
class O2ORelationLeaf12(O2ORelationRoot1):
    pass

class O2ORelationRoot2(AbscreteModel):
    o2orelationroot1 = models.OneToOneField(O2ORelationRoot1,
                                            on_delete=models.CASCADE)
class O2ORelationLeaf21(O2ORelationRoot2):
    pass
class O2ORelationLeaf22(O2ORelationRoot2):
    pass

# Test with foreign relations between models

class ForeignRelationRoot1(AbscreteModel):
    pass
class ForeignRelationLeaf11(ForeignRelationRoot1):
    pass
class ForeignRelationLeaf12(ForeignRelationRoot1):
    pass

class ForeignRelationRoot2(AbscreteModel):
    foreignrelationroot1 = models.ForeignKey(ForeignRelationRoot1,
                                             on_delete=models.CASCADE)
class ForeignRelationLeaf21(ForeignRelationRoot2):
    pass
class ForeignRelationLeaf22(ForeignRelationRoot2):
    pass

# Test with many-to-many relations between models

class M2MRelationRoot1(AbscreteModel):
    pass
class M2MRelationLeaf11(M2MRelationRoot1):
    pass
class M2MRelationLeaf12(M2MRelationRoot1):
    pass

class M2MRelationRoot2(AbscreteModel):
    m2mrelationroot1_set = models.ManyToManyField(M2MRelationRoot1)
class M2MRelationLeaf21(M2MRelationRoot2):
    pass
class M2MRelationLeaf22(M2MRelationRoot2):
    pass
