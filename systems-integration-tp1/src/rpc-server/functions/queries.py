from models.database import Database
from lxml import etree
from datetime import datetime

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
    
    
def oldest_sold_car_details():
    try:
        query = "SELECT xml FROM public.documents WHERE file_name = %s"
        data = ('/data/cars.xml',)
        result = db.select_one(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)

            sales = root.xpath('//Sale[Car/@year]')

            if not sales:
                return None  # No sales with year information

            oldest_car_details = None
            oldest_year = datetime.now().year

            for sale in sales:
                car_year_str = sale.xpath('Car/@year')[0]
                car_year = int(car_year_str)

                if car_year < oldest_year:
                    oldest_year = car_year
                    country_id = sale.xpath('Customer/@country_ref')[0]
                    country_name = root.xpath(f'//Countries/Country[@id="{country_id}"]/@name')[0]
                    
                    brand_ref = sale.xpath('Car/@brand_ref')[0]
                    model_ref = sale.xpath('Car/@model_ref')[0]

                    brand_name = root.xpath(f'//Brands/Brand[@id="{brand_ref}"]/@name')[0]
                    model_name = root.xpath(f'//Models/Model[@id="{model_ref}"]/@name')[0]

                    oldest_car_details = {
                        'Brand': str(brand_name),
                        'Model': str(model_name),
                        'Color': str(sale.xpath('Car/@color')[0]),
                        'Year': str(car_year_str),
                        'Customer Name': str(sale.xpath('Customer/@first_name')[0] +' ' +  sale.xpath('Customer/@last_name')[0]),
                        'Country': str(country_name),
                        'CreditCard': str(sale.xpath('CreditCard_Type/@name')[0])
                    }

            return oldest_car_details if oldest_car_details else None
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None



def newest_sold_car_details():
    try:
        query = "SELECT xml FROM public.documents WHERE file_name = %s"
        data = ('/data/cars.xml',)
        result = db.select_one(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)

            sales = root.xpath('//Sale[Car/@year]')

            if not sales:
                return None  # No sales with year information

            newest_car_details = None
            newest_year = 0

            for sale in sales:
                car_year_str = sale.xpath('Car/@year')[0]
                car_year = int(car_year_str)

                if car_year > newest_year:
                    newest_year = car_year
                    country_id = sale.xpath('Customer/@country_ref')[0]
                    country_name = root.xpath(f'//Countries/Country[@id="{country_id}"]/@name')[0]
                    
                    brand_ref = sale.xpath('Car/@brand_ref')[0]
                    model_ref = sale.xpath('Car/@model_ref')[0]

                    brand_name = root.xpath(f'//Brands/Brand[@id="{brand_ref}"]/@name')[0]
                    model_name = root.xpath(f'//Models/Model[@id="{model_ref}"]/@name')[0]

                    newest_car_details = {
                        'Brand': str(brand_name),
                        'Model': str(model_name),
                        'Color': str(sale.xpath('Car/@color')[0]),
                        'Year': str(car_year_str),
                        'Customer Name': str(sale.xpath('Customer/@first_name')[0] +' ' +  sale.xpath('Customer/@last_name')[0]),
                        'Country': str(country_name),
                        'CreditCard': str(sale.xpath('CreditCard_Type/@name')[0])
                    }

            return newest_car_details if newest_car_details else None
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def most_sold_colors():
    try:
        query = "SELECT xml FROM public.documents WHERE file_name = %s"
        data = ('/data/cars.xml',)
        result = db.select_one(query, data)

        if result is not None:
            xml_data = result[0]
            root = etree.fromstring(xml_data)

            sales = root.xpath('//Sale[Car/@color]')

            if not sales:
                return None  # No sales with color information

            color_counts = {}

            for sale in sales:
                car_color = sale.xpath('Car/@color')[0]
                color_counts[car_color] = color_counts.get(car_color, 0) + 1

            total_sales = len(sales)

            if total_sales > 0:
                color_percentages = {color: count / total_sales * 100 for color, count in color_counts.items()}
                sorted_colors = dict(sorted(color_percentages.items(), key=lambda item: item[1], reverse=True))
                return sorted_colors
            else:
                return None

        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
