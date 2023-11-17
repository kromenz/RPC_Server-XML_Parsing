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
    
    server.register_function(queries.list_documents, "list_documents")
    server.register_function(queries.delete_document, "delete_document")
    server.register_function(queries.fetch_brands)
    server.register_function(queries.fetch_car_models)


    db = Database()

    def signal_handler(signum, frame):
        print("received signal")
        server.server_close()

        # perform clean up, etc. here...

        print("exiting, gracefully")
        sys.exit(0)

    csv_archieve = "/data/cars.csv"
    output_file_path = "/data/cars.xml"
    xsd_archieve = "/data/schemas/cars.xsd"

    converter = CSVtoXMLConverter(csv_archieve)

    xml= converter.to_xml_str(output_file_path,xsd_archieve)

    # Insert XML data into the database
    db = Database()
    query = "INSERT INTO public.documents (file_name, xml) VALUES (%s, %s)"
    data = (output_file_path, xml)
    print(db.insert(query, data))
    
    # signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # register both functions
    
    # start the server
    print("Starting the RPC Server...")
    server.serve_forever()
