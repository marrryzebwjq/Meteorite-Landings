import pandas as pd
from rdflib import Graph, Literal, Namespace, XSD
import reverse_geocode
import math

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
        country = str(row['country']) if not row['country'] == "" else None

        if year and mass and country:
            if(mass>10.0):
                g.add((meteorite_uri, SCHEMA.name, Literal(row['name'], datatype=XSD.string)))
                g.add((meteorite_uri, DBO.recclass, Literal(row['recclass'], datatype=XSD.string)))
                g.add((meteorite_uri, SCHEMA.weight, Literal(mass, datatype=XSD.float)))
                g.add((meteorite_uri, SCHEMA.year, Literal(year, datatype=XSD.gYear)))
                g.add((meteorite_uri, SCHEMA.Event, Literal(row['fall'], datatype=XSD.string)))
                g.add((meteorite_uri, GEONAMES.latitude, Literal(row['reclat'], datatype=XSD.float)))
                g.add((meteorite_uri, GEONAMES.longitude, Literal(row['reclong'], datatype=XSD.float)))
                g.add((meteorite_uri, SCHEMA.country, Literal(row['country'], datatype=XSD.string)))
            else:
                count += 1
        else:
            count+=1

    g.serialize(destination=rdf_file, format="turtle")

    print(count)

def get_country_code(lat, lon):
    if not math.isnan(lon) and not math.isnan(lat):
        location = reverse_geocode.search([(lat, lon)])
        return location[0]['country_code'] if location else None
    return None

def get_countries_meteorite():
    file_path = '../data/Meteorite_Landings_20240924.csv'
    meteorite_data = pd.read_csv(file_path)

    meteorite_data['country'] = meteorite_data.apply(
        lambda row: get_country_code(row['reclat'], row['reclong']), axis=1
    )

    output_path = '../data/Meteorite_Landings_with_country.csv'  # Remplace avec le chemin de sortie
    meteorite_data.to_csv(output_path, index=False)

# get_countries_meteorite()

csv_to_rdf_normalized_year('../data/Meteorite_Landings_with_country.csv',
                           '../output/meteorite_landings.ttl',
                           max_rows=20000)
