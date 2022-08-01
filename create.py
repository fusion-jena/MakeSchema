from utils.definitions import *
from rdflib.namespace import RDF, SKOS
from rdflib import Literal
import meta_config


def add_class(node, created, g):
    """
    Add the given node as an RDFS class
    """
    # get subject
    s = node.name

    # add lbl
    g.add((s, RDFS.label, Literal(node.lbl)))

    # add class type
    g.add((s, RDF.type, RDFS.Class))

    # add exactMatch if exists
    if node.exactMatch:
        g.add((s, SKOS.exactMatch, node.exactMatch))

    # add closeMatch if exists
    if node.closeMatch:
        g.add((s, SKOS.closeMatch, node.closeMatch))

    # add it to the created nodes dict.
    created[node.lbl] = s


def add_literals(node, created, g):
    """
    Add node literals to the given graph instance
    """

    # get subject
    s = created[node.lbl]

    # short cut, if no literals return
    if not node.literals:
        return

    # adds literal by literal
    for lit in node.literals:

        # starts with predicate name that is derived from the literal name
        p = rdflib.URIRef('{}'.format(lit.name))

        # assign owl Datatype Property to the predicate
        g.add((p, RDF.type, owl.DatatypeProperty))

        # adds label
        g.add((p, RDFS.label, Literal(lit.lbl.lower())))

        # assign domain and range
        g.add((p, RDFS.domain, s))
        g.add((p, RDFS.range, rdflib.URIRef(f'{lit.type}')))

        # vocab re-usability
        if lit.exactMatch:
            g.add((p, SKOS.exactMatch, lit.exactMatch))
        if lit.closeMatch:
            g.add((p, SKOS.closeMatch, lit.closeMatch))


def add_obj_relations(node, created, g):
    """
    Assign object relations for a given node
    """

    # get the subject and short cut if no object_relations
    s = created[node.lbl]
    if not node.obj_relations:
        return

    for obj in node.obj_relations:

        # init predicate
        p = rdflib.URIRef('{}{}'.format(bmo, obj.lbl))

        # mark it as owl Object property
        g.add((p, RDF.type, owl.ObjectProperty))

        # adds label
        g.add((p, RDFS.label, Literal(obj.lbl)))

        # adds domain and range
        g.add((p, RDFS.domain, s))
        g.add((p, RDFS.range, created[obj.range.lbl]))


def add_subclass_of(node, created, g):
    """
    Add sub_class relations among nodes
    """
    s = created[node.lbl]

    if not node.subclass_of:
        return

    parent_node = created[node.subclass_of.lbl]
    g.add((s, RDFS.subClassOf, parent_node))


def add_schema_metadata(g):
    """
    Add corresponding metadata from the meta_config file to the created schema
    """
    g.add((onto, RDF.type, SKOS.ConceptScheme))
    g.add((onto, dct.title, Literal(meta_config.schema_title, lang="en")))
    g.add((onto, dct.description, Literal(meta_config.schema_description, lang="en")))
    g.add((onto, dct.license, Literal(meta_config.license_url)))
    g.add((onto, dct.created, Literal(meta_config.created_at, datatype=XSD.date)))
    creator = rdflib.BNode()
    g.add((creator, schema.name, Literal(meta_config.author)))
    g.add((creator, schema.identifier, Literal(meta_config.orcid)))
    affiliation = rdflib.BNode()
    g.add((affiliation, schema.name,
           Literal(meta_config.institute)))
    g.add((affiliation, schema.url, Literal(meta_config.institute_url)))
    g.add((creator, schema.affiliation, affiliation))
    g.add((onto, dct.creator, creator))


if __name__ == '__main__':
    # init new schema instance
    my_schema = Schema()
    # adds corresponding metadata based on the meta_config.py
    add_schema_metadata(g)

    # A dictionary that holds the current progress of the created nodes {node.lbl: rdflib(node)}
    created = {}
    # add all nodes as classes first to ensure that everything is initialized
    for node in my_schema.all_nodes:
        add_class(node, created, g)

    # for each created node assign its literals, objects props and the subclasses relations.
    for node in my_schema.all_nodes:
        add_literals(node, created, g)
        add_obj_relations(node, created, g)
        add_subclass_of(node, created, g)

    # for debugging
    s = g.serialize(format="ttl")
    print(s)

    # exports to three formats Turtle, RDF and n-triples.
    g.serialize(destination="BMO.ttl", format="ttl", encoding="utf-8")
    g.serialize(destination="BMO.rdf", format="pretty-xml", encoding="utf-8")
    g.serialize(destination="BMO.nt", format="ntriples", encoding="utf-8")
