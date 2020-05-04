import csv
import re

geom_regex = re.compile("'((?:POINT|LINESTRING).*?)'")


def convert_to_csv(filename, table_name, value_function=lambda x: x, table_schema='schema_osm'):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        columns = next(reader)
        query = 'INSERT INTO {0}.{1}({2}) VALUES\n'.format(table_schema, table_name, ', '.join(columns))
        query += ','.join(['(' + ', '.join(map((lambda x: value_function(repr_single(x))), row)) + ')\n' for row in reader])
        return query + ";\n"


def replace_points(string):
    return geom_regex.sub(r"ST_GeomFromText('\1')", string)


# TODO: Escape String
def repr_single(s):
    return "'" + repr('"' + s)[2:]


def write_sql(content, filename="out/full.sql"):
    f = open(filename, 'w', encoding='utf-8')
    f.write(content)
    f.close()


sql = '\n'.join([convert_to_csv("out/osm_types.csv", 'osm_type'),
                 convert_to_csv("out/osm_elements.csv", 'osm_element', replace_points),
                 convert_to_csv("out/tags.csv", 'tag')])
write_sql(sql)

