import xml.etree.ElementTree as ET
from models.database import Database
from models.databaserel import DatabaseRel

class RelacionalDB:

    def __init__(self):
        self.db_rel = DatabaseRel()
        self.db = Database()

    def extract_data_from_xml(self, filename):
        self.db.connect()
        try:
            # Retrieve XML content from the database based on the file name
            result = self.db.select_one("SELECT xml FROM public.documents WHERE file_name = %s AND deleted_on IS NULL", (filename,))
            # Add this print statement after retrieving the data
            print(f"Result from the database: {result}")

            if result is None:
                print(f"The file '{filename}' does not exist in the database.")
                return None
            
            # Assuming result is a tuple and the first element is the dictionary with 'xml' key
            xml_data = result[0]
            root = ET.fromstring(xml_data['xml'])  # Assuming xml_data is a dictionary with a key 'xml'

            # Extract data from XML
            countries = {country.text for country in root.findall('.//Country')}
            brands = {brand.text for brand in root.findall('.//Brand')}
            credit_card_types = {card_type.text for card_type in root.findall('.//CreditCard_Type')}
            models = {(model.findtext('Brand'), model.findtext('Name')) for model in root.findall('.//Model')}
            customers = [{'first_name': customer.findtext('FirstName'), 'last_name': customer.findtext('LastName'),
                          'country_name': customer.findtext('Country')} for customer in root.findall('.//Customer')]
            cars = [{'color': car.findtext('Color'), 'year': int(car.findtext('Year')),
                     'model_name': car.findtext('Model')} for car in root.findall('.//Car')]
            sales = [{'customer_first_name': sale.findtext('Customer/FirstName'),
                      'customer_last_name': sale.findtext('Customer/LastName'),
                      'car_color': sale.findtext('Car/Color'),
                      'car_year': int(sale.findtext('Car/Year')),
                      'credit_card_type': sale.findtext('CreditCard/Name')} for sale in root.findall('.//Sale')]

            return {
                'countries': countries,
                'brands': brands,
                'credit_card_types': credit_card_types,
                'models': models,
                'customers': customers,
                'cars': cars,
                'sales': sales
            }

        except Exception as e:
            print(f"Error extracting data from XML: {e}")
            return None
        finally:
            # Ensure to disconnect from the database
            self.db.disconnect()
    # def verify_data_existence(self, data):
    #     try:
    #         for country_name in data['countries']:
    #             if not self.db.select_one("SELECT id FROM public.Country WHERE name = %s", (country_name,)):
    #                 return False

    #         for brand_name in data['brands']:
    #             if not self.db.select_one("SELECT id FROM public.Brand WHERE name = %s", (brand_name,)):
    #                 return False

    #         for card_type in data['credit_card_types']:
    #             if not self.db.select_one("SELECT id FROM public.CreditCard_Type WHERE name = %s", (card_type,)):
    #                 return False

    #         for brand_name, model_name in data['models']:
    #             if not self.db.select_one("SELECT id FROM public.Model WHERE name = %s AND brand_id = (SELECT id FROM public.Brand WHERE name = %s)",
    #                                         (model_name, brand_name)):
    #                 return False

    #         for customer_data in data['customers']:
    #             if not self.db.select_one("SELECT id FROM public.Customer WHERE first_name = %s AND last_name = %s AND country_id = (SELECT id FROM public.Country WHERE name = %s)",
    #                                         (customer_data['first_name'], customer_data['last_name'], customer_data['country_name'])):
    #                 return False

    #         for car_data in data['cars']:
    #             if not self.db.select_one("SELECT id FROM public.Car WHERE color = %s AND year = %s AND model_id = (SELECT id FROM public.Model WHERE name = %s)",
    #                                         (car_data['color'], car_data['year'], car_data['model_name'])):
    #                 return False

    #         for sale_data in data['sales']:
    #             if not self.db.select_one("SELECT id FROM public.Sale WHERE car_id = (SELECT id FROM public.Car WHERE color = %s AND year = %s) AND customer_id = (SELECT id FROM public.Customer WHERE first_name = %s AND last_name = %s) AND credit_card_type_id = (SELECT id FROM public.CreditCard_Type WHERE name = %s)",
    #                                         (sale_data['car_color'], sale_data['car_year'], sale_data['customer_first_name'], sale_data['customer_last_name'], sale_data['credit_card_type'])):
    #                 return False

    #         return True

    #     except Exception as e:
    #         print(f"Error verifying data existence: {e}")
    #         return False

    def insert_data_into_relational_db(self, extracted_data):
        if extracted_data:
            try:
                # Perform verification before insertion
                # if self.verify_data_existence(extracted_data):
                    # Insert data into respective tables in the relational database
                    for country_name in extracted_data['countries']:
                        self.db_rel.insert("INSERT INTO public.Country (name) VALUES (%s)", (country_name,))

                    for brand_name in extracted_data['brands']:
                        self.db_rel.insert("INSERT INTO public.Brand (name) VALUES (%s)", (brand_name,))

                    for card_type in extracted_data['credit_card_types']:
                        self.db_rel.insert("INSERT INTO public.CreditCard_Type (name) VALUES (%s)", (card_type,))

                    for brand_name, model_name in extracted_data['models']:
                        self.db_rel.insert("INSERT INTO public.Model (name, brand_id) VALUES (%s, %s)",
                                           (model_name,
                                            self.db_rel.select_one("SELECT id FROM public.Brand WHERE name = %s",
                                                                  (brand_name,))['id']))

                    for customer_data in extracted_data['customers']:
                        self.db_rel.insert("INSERT INTO public.Customer (first_name, last_name, country_id) VALUES (%s, %s, %s)",
                                           (customer_data['first_name'], customer_data['last_name'],
                                            self.db_rel.select_one("SELECT id FROM public.Country WHERE name = %s",
                                                                   (customer_data['country_name'],))['id']))

                    for car_data in extracted_data['cars']:
                        self.db_rel.insert("INSERT INTO public.Car (color, year, model_id) VALUES (%s, %s, %s)",
                                           (car_data['color'], car_data['year'],
                                            self.db_rel.select_one("SELECT id FROM public.Model WHERE name = %s",
                                                                   (car_data['model_name'],))['id']))

                    for sale_data in extracted_data['sales']:
                        self.db_rel.insert("INSERT INTO public.Sale (car_id, customer_id, credit_card_type_id) VALUES (%s, %s, %s)",
                                           (self.db_rel.select_one("SELECT id FROM public.Car WHERE color = %s AND year = %s",
                                                                  (sale_data['car_color'], sale_data['car_year']))['id'],
                                            self.db_rel.select_one("SELECT id FROM public.Customer WHERE first_name = %s AND last_name = %s",
                                                                  (sale_data['customer_first_name'], sale_data['customer_last_name']))['id'],
                                            self.db_rel.select_one("SELECT id FROM public.CreditCard_Type WHERE name = %s",
                                                                  (sale_data['credit_card_type'],))['id']))

                    print("Data inserted into the relational database.")
                # else:
                #     print("Data verification failed. No data was inserted.")

            except Exception as e:
                print(f"Error inserting data into the relational database: {e}")

    def process_and_insert_data(self):
        try:
            self.db_rel.connect()
            extracted_data = self.extract_data_from_xml()

            if extracted_data:
                # Insert data into the relational database
                self.insert_data_into_relational_db(extracted_data)

        except Exception as e:
            print(f"Error processing and inserting data: {e}")

        finally:
            # Ensure to disconnect from the database
            self.db_rel.disconnect()
