
from xmlrpc.client import Fault
from models.database import Database
from lxml import etree
from datetime import datetime

db = Database()

def index():
    result = db.selectAll(
        "SELECT id, file_name, xml, created_on, updated_on FROM public.documents WHERE deleted_on IS NULL")

    return result

def insert_document(filename, data):
    result = db.insert(filename, data)

    if result == 0:
        raise Fault(1, f"Failed to insert document '{filename}'!")

    return True

def delete_document(filename):
    result = db.softdelete(
        "public.documents", f"file_name LIKE '{filename}' AND deleted_on IS NULL")

    if result == 0:
        raise Fault(1, f"Failed to delete document '{filename}'!")

    return True

def fetch_brands():
    results = db.selectAll(
        "SELECT unnest(xpath('//Brand/@name', xml)) as brand_name FROM public.documents WHERE deleted_on IS NULL")

    brands = [result[0] for result in results]
    sorted_brands = sorted(brands)

    return sorted_brands

def fetch_car_models(brand_name):
    results = db.selectAll(
        f"SELECT unnest(xpath('//Brand[@name=\"{brand_name}\"]/Models/Model/@name', xml)) as model_name FROM public.documents WHERE deleted_on IS NULL")

    models = [result[0] for result in results]
    sorted_models = sorted(models)

    return sorted_models

def sales_per_country():

    sales_country_refs_query = """
        SELECT unnest(xpath('//Sale/Customer/@country_ref', xml)) as country_ref
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    sales_country_refs = db.selectAll(sales_country_refs_query)

    country_names_query = """
        SELECT unnest(xpath('//Country/@name', xml)) as country_name
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    country_names = db.selectAll(country_names_query)

    country_sales = {}
    for country_ref in sales_country_refs:
        if country_ref[0]:
            country_name = country_names[int(country_ref[0]) - 1][0]
            country_sales[country_name] = country_sales.get(country_name, 0) + 1

    sorted_sales = dict(sorted(country_sales.items(), key=lambda item: item[1], reverse=True))
    return sorted_sales
    
def oldest_sold_car_details():

    brand_names_query = "SELECT unnest(xpath('//Brand/@name', xml)) as brand_name FROM public.documents WHERE deleted_on IS NULL"
    brand_names = {i+1: name[0] for i, name in enumerate(db.selectAll(brand_names_query))}

    model_names_query = "SELECT unnest(xpath('//Model/@name', xml)) as model_name FROM public.documents WHERE deleted_on IS NULL"
    model_names = {i+1: name[0] for i, name in enumerate(db.selectAll(model_names_query))}

    country_names_query = "SELECT unnest(xpath('//Country/@name', xml)) as country_name FROM public.documents WHERE deleted_on IS NULL"
    country_names = {i+1: name[0] for i, name in enumerate(db.selectAll(country_names_query))}

    car_sales_query = """
        SELECT 
            unnest(xpath('//Sale/Car/@year', xml)) as year,
            unnest(xpath('//Sale/Car/@color', xml)) as color,
            unnest(xpath('//Sale/Car/@brand_ref', xml)) as brand_ref,
            unnest(xpath('//Sale/Car/@model_ref', xml)) as model_ref,
            unnest(xpath('//Sale/Customer/@first_name', xml)) as first_name,
            unnest(xpath('//Sale/Customer/@last_name', xml)) as last_name,
            unnest(xpath('//Sale/Customer/@country_ref', xml)) as country_ref,
            unnest(xpath('//Sale/CreditCard_Type/@name', xml)) as credit_card
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    car_sales = db.selectAll(car_sales_query)

    oldest_car = None
    oldest_year = float('inf')

    for car in car_sales:
        year, color, brand_ref, model_ref, first_name, last_name, country_ref, credit_card = car
        if year and int(year) < oldest_year:
            oldest_year = int(year)
            brand_name = brand_names.get(int(brand_ref), "Unknown brand")
            model_name = model_names.get(int(model_ref), "Unknown model")
            country_name = country_names.get(int(country_ref), "Unknown country")

            oldest_car = {
                'Brand': brand_name,
                'Model': model_name,
                'Color': color,
                'Year': year,
                'Customer Name': f'{first_name} {last_name}',
                'Country': country_name,
                'CreditCard': credit_card
            }

    return oldest_car if oldest_car else None

def newest_sold_car_details():

    brand_names_query = "SELECT unnest(xpath('//Brand/@name', xml)) as brand_name FROM public.documents WHERE deleted_on IS NULL"
    brand_names = {i+1: name[0] for i, name in enumerate(db.selectAll(brand_names_query))}

    model_names_query = "SELECT unnest(xpath('//Model/@name', xml)) as model_name FROM public.documents WHERE deleted_on IS NULL"
    model_names = {i+1: name[0] for i, name in enumerate(db.selectAll(model_names_query))}

    country_names_query = "SELECT unnest(xpath('//Country/@name', xml)) as country_name FROM public.documents WHERE deleted_on IS NULL"
    country_names = {i+1: name[0] for i, name in enumerate(db.selectAll(country_names_query))}

    car_sales_query = """
        SELECT 
            unnest(xpath('//Sale/Car/@year', xml)) as year,
            unnest(xpath('//Sale/Car/@color', xml)) as color,
            unnest(xpath('//Sale/Car/@brand_ref', xml)) as brand_ref,
            unnest(xpath('//Sale/Car/@model_ref', xml)) as model_ref,
            unnest(xpath('//Sale/Customer/@first_name', xml)) as first_name,
            unnest(xpath('//Sale/Customer/@last_name', xml)) as last_name,
            unnest(xpath('//Sale/Customer/@country_ref', xml)) as country_ref,
            unnest(xpath('//Sale/CreditCard_Type/@name', xml)) as credit_card
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    car_sales = db.selectAll(car_sales_query)

    newest_car = None
    newest_year = 0

    for car in car_sales:
        year, color, brand_ref, model_ref, first_name, last_name, country_ref, credit_card = car
        if year and int(year) > newest_year:
            newest_year = int(year)
            brand_name = brand_names.get(int(brand_ref), "Unknown brand")
            model_name = model_names.get(int(model_ref), "Unknown model")
            country_name = country_names.get(int(country_ref), "Unknown country")

            newest_car = {
                'Brand': brand_name,
                'Model': model_name,
                'Color': color,
                'Year': year,
                'Customer Name': f'{first_name} {last_name}',
                'Country': country_name,
                'CreditCard': credit_card
            }

    return newest_car if newest_car else None

def most_sold_colors():

    car_colors_query = """
        SELECT unnest(xpath('//Sale/Car/@color', xml)) as car_color
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    car_colors = db.selectAll(car_colors_query)

    if not car_colors:
        return None

    color_counts = {}
    for color in car_colors:
        if color[0]:
            color_counts[color[0]] = color_counts.get(color[0], 0) + 1

    total_sales = sum(color_counts.values())

    if total_sales > 0:
        color_percentages = {color: count / total_sales * 100 for color, count in color_counts.items()}
        sorted_colors = dict(sorted(color_percentages.items(), key=lambda item: item[1], reverse=True))
        return sorted_colors
    else:
        return None

def most_sold_brands():

    brand_refs_query = """
        SELECT unnest(xpath('//Sale/Car/@brand_ref', xml)) as brand_ref
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    brand_refs = db.selectAll(brand_refs_query)

    brand_names_query = """
        SELECT unnest(xpath('//Brand/@name', xml)) as brand_name
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    brand_names = db.selectAll(brand_names_query)

    if not brand_refs or not brand_names:
        return None

    brand_counts = {}
    for brand_ref in brand_refs:
        if brand_ref[0]: 
            brand_name = brand_names[int(brand_ref[0]) - 1][0]
            brand_counts[brand_name] = brand_counts.get(brand_name, 0) + 1

    total_sales = sum(brand_counts.values())

    if total_sales > 0:
        brand_percentages = {brand: count / total_sales * 100 for brand, count in brand_counts.items()}
        sorted_brands = dict(sorted(brand_percentages.items(), key=lambda item: item[1], reverse=True))
        return sorted_brands
    else:
        return None

def most_sold_models():

    model_refs_query = """
        SELECT unnest(xpath('//Sale/Car/@model_ref', xml)) as model_ref
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    model_refs = db.selectAll(model_refs_query)

    model_names_query = """
        SELECT unnest(xpath('//Model/@name', xml)) as model_name
        FROM public.documents
        WHERE deleted_on IS NULL
    """
    model_names = db.selectAll(model_names_query)

    if not model_refs or not model_names:
        return None

    model_counts = {}
    for model_ref in model_refs:
        if model_ref[0]:
            model_name = model_names[int(model_ref[0]) - 1][0]
            model_counts[model_name] = model_counts.get(model_name, 0) + 1

    total_sales = sum(model_counts.values())

    if total_sales > 0:
        model_percentages = {model: count / total_sales * 100 for model, count in model_counts.items()}
        sorted_models = dict(sorted(model_percentages.items(), key=lambda item: item[1], reverse=True))
        return sorted_models
    else:
        return None
    
def file_exists(file):
    try:
        
        query = "SELECT COUNT(*) FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
        
        # Using select_one to get a single value (the count of matching records)
        result = db.select_one(query, (file,))

        # Check if the count is greater than 0, indicating that the file exists
        return result[0] > 0 if result else False

    except Exception as e:
        print(f"Error checking if the file exists: {e}")
        return False