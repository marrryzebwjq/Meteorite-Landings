import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import FOAF, XSD

def csv_to_rdf(csv_file, rdf_file):

    data = pd.read_csv(csv_file)
    g = Graph()

    EX = Namespace("https://example.org/meteorite/")
    g.bind("ex", EX)

    for index, row in data.iterrows():

        meteorite_uri = EX[str(row['id'])]

        g.add((meteorite_uri, FOAF.name, Literal(row['name'], datatype=XSD.string)))
        g.add((meteorite_uri, EX.recclass, Literal(row['recclass'], datatype=XSD.string)))
        g.add((meteorite_uri, EX.mass, Literal(row['mass (g)'], datatype=XSD.float)))
        g.add((meteorite_uri, EX.fall, Literal(row['fall'], datatype=XSD.string)))
        g.add((meteorite_uri, EX.year, Literal(row['year'], datatype=XSD.gYear)))
        g.add((meteorite_uri, EX.reclat, Literal(row['reclat'], datatype=XSD.float)))
        g.add((meteorite_uri, EX.reclong, Literal(row['reclong'], datatype=XSD.float)))

    g.serialize(destination=rdf_file, format="turtle")

csv_to_rdf('../data/Meteorite_Landings_20240924.csv', '../output/meteorite_landings.ttl')
