# Em queries.py
from models.database import Database
from lxml import etree

db = Database()

def list_documents():
    documents = db.selectAll("SELECT file_name FROM public.documents")
    return documents

def delete_document(file_name):
    db.delete(f"DELETE FROM public.documents WHERE file_name = %s", (file_name,))
    return True

def fetch_brands():
    query = "SELECT xml FROM public.documents WHERE file_name = %s"
    data = ('/data/cars.xml',)
    result = db.select_one(query, data)

    if result is not None:
        xml_data = result[0]
        root = etree.fromstring(xml_data)
        brands = root.xpath('//Brand')
        return [brand.get('name') for brand in brands]
    else:
        return []

def fetch_car_models(brand_name):
    query = "SELECT xml FROM public.documents WHERE file_name = %s"
    data = ('/data/cars.xml',)
    result = db.select_one(query, data)

    if result is not None:
        xml_data = result[0]
        root = etree.fromstring(xml_data)
        models = root.xpath(f'//Brand[@name="{brand_name}"]/Models/Model')
        return [model.get('name') for model in models]
    else:
        return []
