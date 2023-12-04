
from xmlrpc.client import Fault
from models.database import Database
from models.databaserel import DatabaseRel
from functions.csv_to_xml import CSVtoXMLConverter as converter

db = Database()
db_rel = DatabaseRel()

def index():
    result = db.selectAll(
        "SELECT id, file_name, xml, created_on, updated_on FROM public.documents WHERE deleted_on IS NULL")

    return result

def insert_document(filename, data):
    try:
        query = "INSERT INTO public.documents (file_name, xml) VALUES (%s, %s)"
        data = (filename, data)
        
        converter
        
        db.insert(query, data)
        return True
    except Exception as e:
        print(f"Error inserting document into the database: {e}")
        return False

def delete_document(filename):
    result = db.softdelete(
        "public.documents", f"file_name LIKE '{filename}' AND deleted_on IS NULL")

    if result == 0:
        raise Fault(1, f"Failed to delete document '{filename}'!")

    return True

def fetch_brands(filename):
    results = db.selectAll(
        "SELECT unnest(xpath('//Brand/@name', xml)) as brand_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL", (filename,))
    
    brands = [result[0] for result in results]
    sorted_brands = sorted(brands)
    
    return sorted_brands

def fetch_car_models(filename, brand_name):
    query = "SELECT unnest(xpath('//Brand[@name=\"{}\"]//Model/@name', xml)) as model_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL".format(brand_name)
    results = db.selectAll(query, (filename,))

    models = [result[0] for result in results]
    sorted_models = sorted(models)

    return sorted_models

def sales_per_country(filename):
    sales_country_refs_query = """
        SELECT unnest(xpath('//Sale/Customer/@country_ref', xml)) as country_ref
        FROM public.documents
        WHERE file_name = %s AND deleted_on IS NULL
    """
    sales_country_refs = db.selectAll(sales_country_refs_query, (filename,))

    country_names_query = """
        SELECT unnest(xpath('//Country/@name', xml)) as country_name
        FROM public.documents
        WHERE file_name = %s AND deleted_on IS NULL
    """
    country_names = db.selectAll(country_names_query, (filename,))

    country_sales = {}
    for country_ref in sales_country_refs:
        if country_ref[0]:
            country_name = country_names[int(country_ref[0]) - 1][0]
            country_sales[country_name] = country_sales.get(country_name, 0) + 1

    sorted_sales = dict(sorted(country_sales.items(), key=lambda item: item[1], reverse=True))
    return sorted_sales
    
def oldest_sold_car_details(filename):
    brand_names_query = "SELECT unnest(xpath('//Brand/@name', xml)) as brand_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
    brand_names = {i+1: name[0] for i, name in enumerate(db.selectAll(brand_names_query, (filename,)))}

    model_names_query = "SELECT unnest(xpath('//Model/@name', xml)) as model_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
    model_names = {i+1: name[0] for i, name in enumerate(db.selectAll(model_names_query, (filename,)))}

    country_names_query = "SELECT unnest(xpath('//Country/@name', xml)) as country_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
    country_names = {i+1: name[0] for i, name in enumerate(db.selectAll(country_names_query, (filename,)))}

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
        WHERE file_name = %s AND deleted_on IS NULL
    """
    car_sales = db.selectAll(car_sales_query, (filename,))

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

def newest_sold_car_details(filename):
    brand_names_query = "SELECT unnest(xpath('//Brand/@name', xml)) as brand_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
    brand_names = {i+1: name[0] for i, name in enumerate(db.selectAll(brand_names_query, (filename,)))}

    model_names_query = "SELECT unnest(xpath('//Model/@name', xml)) as model_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
    model_names = {i+1: name[0] for i, name in enumerate(db.selectAll(model_names_query, (filename,)))}

    country_names_query = "SELECT unnest(xpath('//Country/@name', xml)) as country_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
    country_names = {i+1: name[0] for i, name in enumerate(db.selectAll(country_names_query, (filename,)))}

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
        WHERE file_name = %s AND deleted_on IS NULL
    """
    car_sales = db.selectAll(car_sales_query, (filename,))

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

def most_sold_colors(filename):
    car_colors_query = """
        SELECT unnest(xpath('//Sale/Car/@color', xml)) as car_color
        FROM public.documents
        WHERE file_name = %s AND deleted_on IS NULL
    """
    car_colors = db.selectAll(car_colors_query, (filename,))

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

def most_sold_brands(filename):
    brand_refs_query = """
        SELECT unnest(xpath('//Sale/Car/@brand_ref', xml)) as brand_ref
        FROM public.documents
        WHERE file_name = %s AND deleted_on IS NULL
    """
    brand_refs = db.selectAll(brand_refs_query, (filename,))

    brand_names_query = """
        SELECT unnest(xpath('//Brand/@name', xml)) as brand_name
        FROM public.documents
        WHERE file_name = %s AND deleted_on IS NULL
    """
    brand_names = db.selectAll(brand_names_query, (filename,))

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

def most_sold_models(filename):
    model_refs_query = """
        SELECT unnest(xpath('//Sale/Car/@model_ref', xml)) as model_ref
        FROM public.documents
        WHERE file_name = %s AND deleted_on IS NULL
    """
    model_refs = db.selectAll(model_refs_query, (filename,))

    model_names_query = """
        SELECT unnest(xpath('//Model/@name', xml)) as model_name
        FROM public.documents
        WHERE file_name = %s AND deleted_on IS NULL
    """
    model_names = db.selectAll(model_names_query, (filename,))

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

def car_year(year, filename):
    try:
        brand_names_query = "SELECT unnest(xpath('//Brand/@name', xml)) as brand_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
        brand_names = {i+1: name[0] for i, name in enumerate(db.selectAll(brand_names_query, (filename,)))}

        model_names_query = "SELECT unnest(xpath('//Model/@name', xml)) as model_name FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
        model_names = {i+1: name[0] for i, name in enumerate(db.selectAll(model_names_query, (filename,)))}

        car_sales_query = f"""
            SELECT 
                unnest(xpath('//Sale[Car/@year=\"{year}\"]/Car/@brand_ref', xml)) as brand_ref,
                unnest(xpath('//Sale[Car/@year=\"{year}\"]/Car/@model_ref', xml)) as model_ref,
                unnest(xpath('//Sale[Car/@year=\"{year}\"]/Car/@color', xml)) as car_color,
                unnest(xpath('//Sale[Car/@year=\"{year}\"]/Customer/@first_name', xml)) as first_name,
                unnest(xpath('//Sale[Car/@year=\"{year}\"]/Customer/@last_name', xml)) as last_name
            FROM public.documents
            WHERE file_name = %s AND deleted_on IS NULL
        """
        car_sales = db.selectAll(car_sales_query, (filename,))

        car_data = []
        for brand_ref, model_ref, car_color, first_name, last_name in car_sales:
            if brand_ref and model_ref:
                brand_name = brand_names.get(int(brand_ref), "Unknown brand")
                model_name = model_names.get(int(model_ref), "Unknown model")
                customer_name = f"{first_name} {last_name}" if first_name and last_name else "Unknown customer"
                car_data.append({
                    "Brand": brand_name,
                    "Model": model_name,
                    "Color": car_color,
                    "Customer": customer_name
                })

        return car_data if car_data else "No car details found for the year."

    except Exception as e:
        return f"Error in car_year(): {e}"

def file_exists(file):
    try:
        
        query = "SELECT COUNT(*) FROM public.documents WHERE file_name = %s AND deleted_on IS NULL"
        
        result = db.select_one(query, (file,))

        return result[0] > 0 if result else False

    except Exception as e:
        print(f"Error checking if the file exists: {e}")
        return False
    
    data = converter.extract_data_from_xml(xml_data)

    # Insert data into respective tables in the relational database
    for country_name in data['countries']:
        db.insert("INSERT INTO public.Country (name) VALUES (%s)", (country_name,))

    for brand_name in data['brands']:
        db.insert("INSERT INTO public.Brand (name) VALUES (%s)", (brand_name,))

    for card_type in data['credit_card_types']:
        db.insert("INSERT INTO public.CreditCard_Type (name) VALUES (%s)", (card_type,))

    for brand_name, model_name in data['models']:
        db.insert("INSERT INTO public.Model (name, brand_id) VALUES (%s, %s)",
                  (model_name, db.select_one("SELECT id FROM public.Brand WHERE name = %s", (brand_name,))['id']))

    for customer_data in data['customers']:
        db.insert("INSERT INTO public.Customer (first_name, last_name, country_id) VALUES (%s, %s, %s)",
                  (customer_data['first_name'], customer_data['last_name'],
                   db.select_one("SELECT id FROM public.Country WHERE name = %s", (customer_data['country_name'],))['id']))

    for car_data in data['cars']:
        db.insert("INSERT INTO public.Car (color, year, model_id) VALUES (%s, %s, %s)",
                  (car_data['color'], car_data['year'],
                   db.select_one("SELECT id FROM public.Model WHERE name = %s", (car_data['model_name'],))['id']))

    for sale_data in data['sales']:
        db.insert("INSERT INTO public.Sale (car_id, customer_id, credit_card_type_id) VALUES (%s, %s, %s)",
                  (db.select_one("SELECT id FROM public.Car WHERE color = %s AND year = %s",
                                 (sale_data['car_color'], sale_data['car_year']))['id'],
                   db.select_one("SELECT id FROM public.Customer WHERE first_name = %s AND last_name = %s",
                                 (sale_data['customer_first_name'], sale_data['customer_last_name']))['id'],
                   db.select_one("SELECT id FROM public.CreditCard_Type WHERE name = %s",
                                 (sale_data['credit_card_type'],))['id']))