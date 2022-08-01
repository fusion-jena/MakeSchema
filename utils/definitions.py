from schema_creation.utils.data_structure import *


class Schema:
    def __init__(self):
        self.all_nodes = []

        # entity
        self.entity = MyClassNode(name=bmo.Entity, exactMatch=schema.Thing, lbl="Entity",
                                  literals=[MyLiteral(name=bmo.title, lbl='title', exactMatch=schema.name),
                                            MyLiteral(name=bmo.abstract, lbl='abstract', exactMatch=schema.abstract)])
        self.all_nodes += [self.entity]

        ## address
        address_lits = [MyLiteral(name=bmo.city, lbl='city'),
                        MyLiteral(name=bmo.street, lbl='street', exactMatch=schema.streetAddress),
                        MyLiteral(name=bmo.county, lbl='country'),
                        MyLiteral(name=bmo.postalCode, lbl='postalCode', exactMatch=schema.postalCode)]
        self.address = MyClassNode(name=bmo.Address, exactMatch=schema.PostalAddress, lbl="Address",
                                   literals=address_lits)
        self.all_nodes += [self.address]

        # person
        person_lits = [MyLiteral(name=bmo.givenName, lbl='givenName', exactMatch=schema.givenName),
                       MyLiteral(name=bmo.surName, lbl='surName', exactMatch=schema.familyName),
                       MyLiteral(name=bmo.electronicMail, lbl='electronicMail', exactMatch=schema.email),
                       MyLiteral(name=bmo.phone, lbl='phone', exactMatch=schema.telephone),
                       MyLiteral(name=bmo.organization, lbl='organization', exactMatch=schema.organization)]
        self.person = MyClassNode(name=bmo.Person, lbl="Person", exactMatch=schema.Person, literals=person_lits)

        self.person.obj_relations = [MyObjRelation("address", self.address)]

        self.all_nodes += [self.person]

        # coverage
        self.coverage = MyClassNode(name=bmo.Coverage, lbl="Coverage")
        self.all_nodes += [self.coverage]

        self.boundingCoordinates = MyClassNode(name=bmo.BoundingCoordinates, lbl="BoundingCoordinates",
                                               literals=[MyLiteral(name=bmo.northBoundingCoordinate, lbl='northBoundingCoordinate', type=XSD.decimal),
                                                         MyLiteral(name=bmo.southBoundingCoordinate, lbl='southBoundingCoordinate', type=XSD.decimal),
                                                         MyLiteral(name=bmo.eastBoundingCoordinate, lbl='eastBoundingCoordinate', type=XSD.decimal),
                                                         MyLiteral(name=bmo.westBoundingCoordinate, lbl='westBoundingCoordinate', type=XSD.decimal)])
        self.all_nodes += [self.boundingCoordinates]

        self.plots = MyClassNode(name=bmo.NumberOfPlots, lbl="Plot",
                                 literals=[MyLiteral(name=bmo.numberOfGp, lbl='numberOfGG' , type=XSD.int),
                                           MyLiteral(name=bmo.numberOfEp, lbl='numberOfEP', type=XSD.int),
                                           MyLiteral(name=bmo.numberOfVip, lbl='numberOfVIP', type=XSD.int),
                                           MyLiteral(name=bmo.numberOfMip, lbl='numberOfMIP', type=XSD.int)])
        self.all_nodes += [self.plots]

        self.geographicCoverage = MyClassNode(name=bmo.GeographicCoverage, lbl="GeographicCoverage",
                                              subclass_of=self.coverage)

        self.geographicCoverage.obj_relations = [MyObjRelation("boundingCoordinates", self.boundingCoordinates),
                                                 MyObjRelation("numberOfPlots", self.plots)]

        self.all_nodes += [self.geographicCoverage]

        self.temporalCoverage = MyClassNode(name=bmo.TemporalCoverage, lbl="TemporalCoverage",
                                            subclass_of=self.coverage,
                                            literals=[MyLiteral(name=bmo.beginDate, lbl="beginDate", type=XSD.date, exactMatch=schema.startDate),
                                                      MyLiteral(name=bmo.endDate, lbl="endDate", type=XSD.date, exactMatch=schema.endDate)])
        self.all_nodes += [self.temporalCoverage]

        self.taxonomicCoverage = MyClassNode(name=bmo.TaxonomicCoverage, lbl="TaxonomicCoverage",
                                             subclass_of=self.coverage,
                                             literals=[MyLiteral(name=bmo.taxonCommonName, lbl="taxonCommonName", exactMatch=wd.P1843),
                                                       MyLiteral(name=bmo.taxonRankName, lbl="taxonRankName", exactMatch=wd.P105)
                                                       ])
        self.all_nodes += [self.taxonomicCoverage]

        # project
        self.project = MyClassNode(name=schema.Project, lbl="Project",
                                   subclass_of=self.entity,
                                   literals=[MyLiteral(name=bmo.funding, lbl="funding", closeMatch=schema.funding),
                                             MyLiteral(name=bmo.startDate, lbl="startDate", type=XSD.date, exactMatch=schema.startDate)])
        self.all_nodes += [self.project]

        # method
        self.method = MyClassNode(name=bmo.Method, lbl="Method",
                                  subclass_of=self.entity,
                                  literals=[MyLiteral(name=bmo.introduction, lbl="introduction"),
                                            MyLiteral(name=bmo.measurement, lbl="measurement"),
                                            MyLiteral(name=bmo.equipment, lbl="equipment")
                                            ])
        self.all_nodes += [self.method]

        # dataset
        dataset_lits = [MyLiteral(name=bmo.language, lbl='language', exactMatch=schema.inLanguage),
                        MyLiteral(name=bmo.description, lbl='description', exactMatch=schema.description),
                        MyLiteral(name=bmo.citation, lbl='citation', exactMatch=schema.citation),
                        MyLiteral(name=bmo.intellectualRights, lbl='intellectualRights', closeMatch=dct.accessRights),
                        MyLiteral(name=bmo.license, lbl='license', closeMatch=dct.license),
                        MyLiteral(name=bmo.dataFormat, lbl='dataFormat'),
                        MyLiteral(name=bmo.version, lbl='version', exactMatch=schema.version),
                        MyLiteral(name=bmo.keywordsSet, lbl='keywordsSet', exactMatch=schema.keywords),
                        MyLiteral(name=bmo.doi, lbl='doi', exactMatch=wd.P356),
                        MyLiteral(name=bmo.alternateIdentifier, lbl='alternateIdentifier', exactMatch=schema.identifier),
                        MyLiteral(name=bmo.numberOfRecords, lbl='numberOfRecords', exactMatch=wd.P4876, type=XSD.int),
                        MyLiteral(name=bmo.publicationDate, lbl='publicationDate',  exactMatch=schema.datePublished, type=XSD.date)
                        ]
        self.dataset = MyClassNode(name=bmo.Dataset, exactMatch=schema.Dataset, lbl="Dataset", subclass_of=self.entity,
                                   literals=dataset_lits)

        # assign relation , all classes must be added first
        self.dataset.obj_relations = [
            MyObjRelation("dataCreator", self.person),
            MyObjRelation("metadataProvider", self.person),
            MyObjRelation("contactPerson", self.person),
            MyObjRelation("projectLeader", self.person),

            MyObjRelation("geographicCoverage", self.geographicCoverage),
            MyObjRelation("temporalCoverage", self.temporalCoverage),
            MyObjRelation("taxonomicCoverage", self.taxonomicCoverage),

            MyObjRelation("project", self.project),
        ]

        self.all_nodes += [self.dataset]
