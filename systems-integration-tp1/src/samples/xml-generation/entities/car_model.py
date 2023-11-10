import xml.etree.ElementTree as ET
from entities.brand import Brand

class CarModel:

    def __init__(self, brand, name):
        CarModel.counter += 1
        self._id = CarModel.counter
        self._brands =  brand
        self._name = name

    def add_brand(self, brand: Brand):
        self._brands.append(brand)
    
    def to_xml(self):
        el = ET.Element("CarModel")
        el.set("id", str(self._id))
        el.set("brand", self._brands)
        el.set("name", self._name)

        brands_el  = ET.Element("<Brand")
        for brand in self.brands:
            brands_el.append(brand.to_xml())
        el.append(brands_el.to)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"brand: {self._brands}, name: {self._name}, id: {self._id}"

CarModel.counter = 0



