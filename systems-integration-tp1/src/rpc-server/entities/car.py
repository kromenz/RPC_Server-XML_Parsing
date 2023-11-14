import xml.etree.ElementTree as ET
from entities.car_model import CarModel
from lxml import etree

class Car:
    
    def __init__(self, model, color, year):
        Car.counter += 1
        self._id = Car.counter
        self._model = model
        self._color = color
        self._year = year

    def to_xml_lxml(self):
        car_el = etree.Element("Car", id=str(self._id), color=self._color, year=str(self._year))

        if self._model and self._model._brand:
            brand_el = etree.SubElement(car_el, "Brand", id=str(self._model._brand._id), name=self._model._brand._name)
            etree.SubElement(brand_el, "Model", id=str(self._model._id) ,name=self._model._name)

        return car_el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"model: {self._model._name}, color: {self._color}, year: {self._year}, id: {self._id}"

Car.counter = 0
