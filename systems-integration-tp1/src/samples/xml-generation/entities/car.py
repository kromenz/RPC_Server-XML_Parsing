import xml.etree.ElementTree as ET
from entities.car_model import CarModel

class Car:
    
    def __init__(self, model, color, year):
        Car.counter += 1
        self._id = Car.counter
        self._models = []
        self._color = color
        self._year = year

    def add_model(self, model: CarModel):
        self._models.append(model)

    def to_xml(self):
        el = ET.Element("Car")
        el.set("id", str(self._id))
        el.set("color", self._color)
        el.set("year", str(self._year))

        models_el = ET.Element("Models")
        for model in self._models:
            models_el.append(model.to_xml())

        el.append(models_el)
        
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"modelRef: {self._modelRef}, color: {self._color}, year: {self._year}, id: {self._id}"

Car.counter = 0