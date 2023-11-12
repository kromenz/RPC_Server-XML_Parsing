import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from csv_reader import CSVReader
from lxml import etree
from entities.country import Country
from entities.car import Car
from entities.brand import Brand
from entities.car_model import CarModel
from entities.card import CreditCard
from entities.customer import Customer
from entities.sales import Sale

class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        countries = {}
        brands = {}
        car_models = {}
        credit_cards = {}
        sales = []

        for row in self._reader.loop():
            # Processar e armazenar países
            country_name = row["Country"]
            if country_name not in countries:
                countries[country_name] = Country(country_name)

            # Processar e armazenar marcas
            brand_name = row["Car Brand"]
            if brand_name not in brands:
                brands[brand_name] = Brand(brand_name)

            # Processar e armazenar modelos de carros
            model_name = row["Car Model"]
            model_key = (brand_name, model_name)
            if model_key not in car_models:
                brand = brands[brand_name]
                model = CarModel(model_name, brand)
                car_models[model_key] = model
                brand.add_model(model)

            # Processar e armazenar tipos de cartões de crédito
            credit_card_type = row["Credit Card Type"]
            if credit_card_type not in credit_cards:
                credit_cards[credit_card_type] = CreditCard(credit_card_type)

            # Criação e armazenamento de vendas
            country = countries[country_name]
            customer = Customer(row["First Name"], row["Last Name"], country)
            car = Car(car_models[model_key], row["Car Color"], row["Year of Manufacture"])
            sale = Sale()
            sale.add_customer(customer)
            sale.add_car(car)
            sale.add_creditCard(credit_cards[credit_card_type])
            sales.append(sale)

        # Geração do XML
        dealership_el = etree.Element("Dealership")

        # Seção de vendas
        sales_el = etree.SubElement(dealership_el, "sales")
        for sale in sales:
            sales_el.append(sale.to_xml_lxml())

        # Seção de países
        countries_el = etree.SubElement(dealership_el, "Countries")
        for country in countries.values():
            countries_el.append(country.to_xml_lxml())

        # Seção de marcas
        brands_el = etree.SubElement(dealership_el, "Brands")
        for brand in brands.values():
            brands_el.append(brand.to_xml_lxml())

        # Seção de modelos de carros
        #car_models_el = etree.SubElement(dealership_el, "CarModels")
        #for model_key, model in car_models.items():
            #car_models_el.append(model.to_xml_lxml())

        # Seção de tipos de cartões de crédito
        card_types_el = etree.SubElement(dealership_el, "CardTypes")
        for card_type, card in credit_cards.items():
            card_types_el.append(card.to_xml_lxml())

        return dealership_el

    def to_xml_str(self, file_path, xsd_path=None):
        xml_tree = self.to_xml()

        if xsd_path:
            xml_str = etree.tostring(xml_tree, pretty_print=True, encoding='utf-8').decode('utf-8')
            if self.validate_xml_with_xsd(xml_str, xsd_path):
                with open(file_path, 'wb') as file:
                    file.write(etree.tostring(xml_tree, pretty_print=True, encoding='utf-8'))
                print(f" Validação bem sucedida! O arquivo '{file_path}' foi criado com sucesso.")
                return xml_str
            else:
                print("A validação falhou. O XML não será gerado.")
                return None
        else:
            xml_str = etree.tostring(xml_tree, pretty_print=True, encoding='utf-8').decode('utf-8')
            return xml_str

    def validate_xml_with_xsd(self, xml_str, xsd_path):
        try:
            xsd_tree = etree.parse(xsd_path)
            schema = etree.XMLSchema(xsd_tree)

            # Carrega o XML a partir da string
            xml_doc = etree.fromstring(xml_str)

            # Valida o XML através do XSD
            schema.assertValid(xml_doc)
            
            print("A validação foi bem-sucedida!")
            return True
        except etree.DocumentInvalid as e:
            print(f"Erro de validação: {e}")
            return False

           


