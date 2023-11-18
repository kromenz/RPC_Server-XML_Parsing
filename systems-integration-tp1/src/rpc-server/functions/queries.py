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
        sorted_brands = sorted([brand.get('name') for brand in brands])
        return sorted_brands
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
        sorted_models = sorted([model.get('name') for model in models])
        return sorted_models
    else:
        return []


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
        sorted_brands = sorted([brand.get('name') for brand in brands])
        return sorted_brands
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
        sorted_models = sorted([model.get('name') for model in models])
        return sorted_models
    else:
        return []

def sales_per_country():
    try:
        query = "SELECT xml FROM public.documents WHERE file_name = %s"
        data = ('/data/cars.xml',)
        result = db.select_one(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)

            countries = root.xpath('//Country/@name')
            sales = root.xpath('//Sale[Customer/@country_ref]')

            sales_per_country = {country: 0 for country in countries}
            for sale in sales:
                country_ref = sale.xpath('Customer/@country_ref')[0]
                country_name = countries[int(country_ref) - 1]
                sales_per_country[country_name] += 1

            sorted_sales = dict(sorted(sales_per_country.items(), key=lambda item: item[1], reverse=True))

            return sorted_sales
        else:
            return {}

    except Exception as e:
        print(f"Error: {e}")
        return {}


