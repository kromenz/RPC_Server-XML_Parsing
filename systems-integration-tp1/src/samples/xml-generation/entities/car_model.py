import xml.etree.ElementTree as ET
from entities.brand import Brand
from lxml import etree

class CarModel:

    def __init__(self, brand, name):
        CarModel.counter += 1
        self._id = CarModel.counter
        self._brand = brand
        self._name = name

    def to_xml_lxml(self):
        el = etree.Element("CarModel")
        el.set("id", str(self._id))
        el.set("name", self._name)


        brand_el = self._brand.to_xml_lxml()
        el.append(brand_el)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"brand: {self._brand._name}, name: {self._name}, id: {self._id}"

CarModel.counter = 0