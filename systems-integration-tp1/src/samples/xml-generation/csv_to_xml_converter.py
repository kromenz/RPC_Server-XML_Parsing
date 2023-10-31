import xml.etree.ElementTree as ET
from csv_reader import CSVReader

class CSVtoXMLConverter:

    def __init__(self, csv_path):
        self._reader = CSVReader(csv_path)
        self.xml_path = csv_path.replace('.csv', '.xml')
        self.people_ids = {}
        self.car_ids = {}
        self.country_ids = {}
        self.payment_ids = {}
        self.car_model_ids = {}

    def get_unique_id(self, id_dict, value):
        if value not in id_dict:
            id_dict[value] = len(id_dict) + 1
        return id_dict[value]

    def to_xml(self):
        root_el = ET.Element("Data")

        for row in self._reader.loop():
            # Create person element
            person_id = self.get_unique_id(self.people_ids, f"{row['First Name']} {row['Last Name']}")
            person_el = ET.Element("Person", id=str(person_id))
            person_el.set("FirstName", row["First Name"])
            person_el.set("LastName", row["Last Name"])

            # Create car element
            car_id = self.get_unique_id(self.car_ids, row["Car Brand"])
            car_el = ET.Element("Car", id=str(car_id))
            car_el.set("Brand", row["Car Brand"])

            # Create car model element
            car_model_id = self.get_unique_id(self.car_model_ids, f"{row['Car Brand']} {row['Car Model']}")
            car_model_el = ET.Element("Model", id=str(car_model_id))
            car_model_el.set("Name", row["Car Model"])
            car_model_el.set("Color", row["Car Color"])
            car_model_el.set("Year", row["Year of Manufacture"])

            car_el.append(car_model_el)

            # Create country element
            country_id = self.get_unique_id(self.country_ids, row["Country"])
            country_el = ET.Element("Country", id=str(country_id))
            country_el.text = row["Country"]

            # Create payment element
            payment_id = self.get_unique_id(self.payment_ids, row["Credit Card Type"])
            payment_el = ET.Element("Payment", id=str(payment_id))
            payment_el.text = row["Credit Card Type"]

            # Organize the hierarchy
            person_el.append(country_el)
            person_el.append(car_el)
            person_el.append(payment_el)

            root_el.append(person_el)

        return ET.ElementTree(root_el)

    def save_xml(self):
        tree = self.to_xml()
        tree.write(self.xml_path, encoding="utf-8", xml_declaration=True)

# Caminho para o arquivo CSV
csv_path = 'docker/volumes/data/cars.csv'

# Exemplo de como usar a classe CSVtoXMLConverter para converter o CSV para XML com hierarquias e IDs únicos organizados
converter = CSVtoXMLConverter(csv_path)
converter.save_xml()

# O arquivo XML com hierarquias e IDs únicos será criado na mesma pasta que o arquivo CSV com o mesmo nome, mas com extensão .xml
print(f'Arquivo XML criado em: {converter.xml_path}')
