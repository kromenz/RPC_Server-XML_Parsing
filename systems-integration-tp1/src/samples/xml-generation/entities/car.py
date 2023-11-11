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
        el = etree.Element("Car")
        el.set("id", str(self._id))
        el.set("color", self._color)
        el.set("year", str(self._year))

    
        if self._model is not None:
            model_el = self._model.to_xml_lxml()
            el.append(model_el)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"model: {self._model._name}, color: {self._color}, year: {self._year}, id: {self._id}"

Car.counter = 0
