import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from functions.csv_to_xml import CSVtoXMLConverter
from models.database import Database

import functions.queries as queries

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
    

with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    db = Database()

    csv_archieve = "/data/cars.csv"
    output_file_path = "/data/cars.xml"
    xsd_archieve = "/data/schemas/cars.xsd"

    converter = CSVtoXMLConverter(csv_archieve)

    xml= converter.to_xml_str(output_file_path,xsd_archieve)

    # Insert XML data into the database
    db = Database()
    query = "INSERT INTO public.documents (file_name, xml) VALUES (%s, %s)"
    data = (output_file_path, xml)
    db.insert(query, data)
 
    # register functions
    server.register_function(queries.delete_document)
    server.register_function(queries.index)
    server.register_function(queries.fetch_brands)
    server.register_function(queries.fetch_car_models)
    server.register_function(queries.sales_per_country)
    server.register_function(queries.oldest_sold_car_details)
    server.register_function(queries.newest_sold_car_details)
    server.register_function(queries.most_sold_colors)
    server.register_function(queries.most_sold_brands)
    server.register_function(queries.most_sold_models)
    server.register_function(queries.file_exists)
    
    # start the server
    print("Starting the RPC Server...")
    server.serve_forever()
