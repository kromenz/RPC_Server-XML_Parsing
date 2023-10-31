import xml.etree.ElementTree as ET
from csv_reader import CSVReader

class CSVtoXMLConverter:

    def __init__(self, csv_path):
        self._reader = CSVReader(csv_path)
        self.xml_path = csv_path.replace('.csv', '.xml')
        self.people_ids = {}
        self.country_ids = {}
        self.car_ids = {}

    def get_person_id(self, first_name, last_name):
        full_name = f"{first_name} {last_name}"
        if full_name in self.people_ids:
            return self.people_ids[full_name]
        else:
            person_id = len(self.people_ids) + 1
            self.people_ids[full_name] = person_id
            return person_id

    def get_country_id(self, country):
        if country in self.country_ids:
            return self.country_ids[country]
        else:
            country_id = len(self.country_ids) + 1
            self.country_ids[country] = country_id
            return country_id

    def get_car_id(self, brand, model):
        car_identifier = f"{brand} {model}"
        if car_identifier in self.car_ids:
            return self.car_ids[car_identifier]
        else:
            car_id = len(self.car_ids) + 1
            self.car_ids[car_identifier] = car_id
            return car_id

    def to_xml(self):
        root_el = ET.Element("Data")

        for row in self._reader.loop():
            # Create person element
            person_id = self.get_person_id(row["First Name"], row["Last Name"])
            person_el = ET.Element("Person", id=str(person_id))
            person_el.set("FirstName", row["First Name"])
            person_el.set("LastName", row["Last Name"])

            # Create country element
            country_id = self.get_country_id(row["Country"])
            country_el = ET.Element("Country", id=str(country_id))
            country_el.text = row["Country"]

            # Create car element
            car_id = self.get_car_id(row["Car Brand"], row["Car Model"])
            car_el = ET.Element("Car", id=str(car_id))
            car_el.set("Brand", row["Car Brand"])
            car_el.set("Model", row["Car Model"])
            car_el.set("Color", row["Car Color"])
            car_el.set("Year", row["Year of Manufacture"])
            car_el.set("CreditCardType", row["Credit Card Type"])

            # Add elements to the root
            root_el.append(person_el)
            root_el.append(country_el)
            root_el.append(car_el)

        return ET.ElementTree(root_el)

    def save_xml(self):
        tree = self.to_xml()
        tree.write(self.xml_path, encoding="utf-8", xml_declaration=True)

# Caminho para o arquivo CSV
csv_path = 'docker/volumes/data/cars.csv'

# Exemplo de como usar a classe CSVtoXMLConverter para converter o CSV para XML com IDs baseados em valores únicos
converter = CSVtoXMLConverter(csv_path)
converter.save_xml()

# O arquivo XML hierárquico com IDs baseados em valores únicos será criado na mesma pasta que o arquivo CSV com o mesmo nome, mas com extensão .xml
print(f'Arquivo XML criado em: {converter.xml_path}')
