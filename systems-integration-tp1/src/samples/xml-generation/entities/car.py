import xml.etree.ElementTree as ET


class Car:

    def __init__(self, brand, model, year):
        Car.counter += 1
        self._id = Car.counter
        self._brand = brand
        self._model = model
        self._country = country
        self._year = year

    def to_xml(self):
        el = ET.Element("Car")
        el.set("id", str(self._id))
        el.set("brand", self._name)
        el.set("model", self._model)
        el.set("year", self._year)
        return el

    def __str__(self):
        return f"{self._brand}, model:{self._model}, year:{self._year}"


Car.counter = 0
