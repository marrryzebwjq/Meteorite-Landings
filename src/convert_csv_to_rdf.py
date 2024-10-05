import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD

def csv_to_rdf(csv_file, rdf_file):
    data = pd.read_csv(csv_file)
    g = Graph()

    GEONAMES = Namespace("https://www.geonames.org/ontology#")
    DBO = Namespace("https://dbpedia.org/ontology/")
    SCHEMA = Namespace("https://schema.org/")
    EX = Namespace("https://example.org/meteorite/")
    g.bind("ex", EX)

    for index, row in data.iterrows():
        meteorite_uri = EX[str(row['id'])]

        g.add((meteorite_uri, SCHEMA.name, Literal(row['name'], datatype=XSD.string)))
        g.add((meteorite_uri, DBO.recclass, Literal(row['recclass'], datatype=XSD.string)))

        mass = row['mass (g)']
        mass = float(mass) if not pd.isna(mass) else 0.0

        g.add((meteorite_uri, SCHEMA.weight, Literal(mass, datatype=XSD.float)))
        g.add((meteorite_uri, SCHEMA.Event, Literal(row['fall'], datatype=XSD.string)))
        g.add((meteorite_uri, SCHEMA.year, Literal(row['year'], datatype=XSD.gYear)))
        g.add((meteorite_uri, GEONAMES.latitude, Literal(row['reclat'], datatype=XSD.float)))
        g.add((meteorite_uri, GEONAMES.longitude, Literal(row['reclong'], datatype=XSD.float)))

    g.serialize(destination=rdf_file, format="turtle")

csv_to_rdf('../data/Meteorite_Landings_20240924.csv', '../output/meteorite_landings.ttl')
