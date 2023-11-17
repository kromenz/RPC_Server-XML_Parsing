import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from functions.csv_to_xml import CSVtoXMLConverter
from models.database import Database
from lxml import etree

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
    
def list_documents():
    db = Database()
    documents = db.selectAll("SELECT file_name FROM public.documents")
    db.disconnect()
    return documents

def delete_document(file_name):
    db = Database()
    db.delete(f"DELETE FROM public.documents WHERE file_name = %s", (file_name,))
    db.disconnect()
    return True

def fetch_brands():
    database = Database()
    query = "SELECT xml FROM public.documents WHERE file_name = %s"
    data = ('/data/cars.xml',)  # Substitua pelo nome correto do arquivo, se necessário
    result = database.select_one(query, data)
    database.disconnect()

    if result is not None:
        xml_data = result[0]
        root = etree.fromstring(xml_data)
        brands = root.xpath('//Brand')
        return [brand.get('name') for brand in brands]
    else:
        return []


with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    
    server.register_function(list_documents, "list_documents")
    server.register_function(delete_document, "delete_document")
    server.register_function(fetch_brands)


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
