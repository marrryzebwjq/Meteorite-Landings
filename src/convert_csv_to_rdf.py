import pandas as pd
from rdflib import Graph, Literal, Namespace, XSD

def csv_to_rdf_normalized_year(csv_file, rdf_file, max_rows=70000):
    data = pd.read_csv(csv_file)

    filtered_data = data.dropna(subset=['reclat', 'reclong']).head(max_rows)

    g = Graph()

    GEONAMES = Namespace("https://www.geonames.org/ontology#")
    DBO = Namespace("https://dbpedia.org/ontology/")
    SCHEMA = Namespace("https://schema.org/")
    EX = Namespace("https://example.org/meteorite/")
    g.bind("ex", EX)

    count = 0
    for index, row in filtered_data.iterrows():
        meteorite_uri = EX[str(row['id'])]

        mass = float(row['mass (g)']) if not pd.isna(row['mass (g)']) else None
        year = int(row['year']) if not pd.isna(row['year']) else None

        if year and mass:
            if(mass>10.0):
                g.add((meteorite_uri, SCHEMA.name, Literal(row['name'], datatype=XSD.string)))
                g.add((meteorite_uri, DBO.recclass, Literal(row['recclass'], datatype=XSD.string)))
                g.add((meteorite_uri, SCHEMA.weight, Literal(mass, datatype=XSD.float)))
                g.add((meteorite_uri, SCHEMA.year, Literal(year, datatype=XSD.gYear)))
                g.add((meteorite_uri, SCHEMA.Event, Literal(row['fall'], datatype=XSD.string)))
                g.add((meteorite_uri, GEONAMES.latitude, Literal(row['reclat'], datatype=XSD.float)))
                g.add((meteorite_uri, GEONAMES.longitude, Literal(row['reclong'], datatype=XSD.float)))
            else:
                count += 1
        else:
            count+=1

    g.serialize(destination=rdf_file, format="turtle")

    print(count)

csv_to_rdf_normalized_year('C:/Users/Lucas/PycharmProjects/projet_dana_web_semantique/data/Meteorite_Landings_20240924.csv',
                           'C:/Users/Lucas/PycharmProjects/projet_dana_web_semantique/output/meteorite_landings.ttl',
                           max_rows=20000)
