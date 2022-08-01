from schema_creation.utils.namespaces import *


class MyObjRelation:
    def __init__(self, lbl, range_node):
        self.lbl = lbl
        self.range = range_node


class MyLiteral:
    def __init__(self, name, lbl, type=XSD.string, exactMatch=None, closeMatch=None):
        self.name = name
        self.lbl = lbl
        self.type = type
        self.exactMatch = exactMatch
        self.closeMatch = closeMatch


class MyClassNode:
    def __init__(self, name=None, lbl=None, exactMatch=None, closeMatch=None, subclass_of=None, literals=None,
                 obj_relations=None):
        self.name = name
        self.lbl = lbl
        self.subclass_of = subclass_of
        self.exactMatch = exactMatch
        self.closeMatch = closeMatch
        self.literals = literals  # list of tuples (namespace, lbl) e.g., [(schema, "title")]
        self.obj_relations = obj_relations
