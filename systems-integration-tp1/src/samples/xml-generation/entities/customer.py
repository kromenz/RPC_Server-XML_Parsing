import xml.etree.ElementTree as ET
from entities.country import Country
from lxml import etree

class Customer:

    def __init__(self, first_name, last_name, country):
        Customer.counter += 1
        self._id = Customer.counter
        self._first_name = first_name
        self._last_name = last_name
        self._countrys = []
        
    def add_country(self, country: Country):
        self._countrys.append(country)

    def to_xml_lxml(self):
        el = etree.Element("Customer")
        el.set("id", str(self._id))
        el.set("first_name", self._first_name)
        el.set("last_name", self._last_name)
        
        for country in self._countrys:
            country_el = country.to_xml_lxml()
            el.append(country_el)
        
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"first_name: {self._first_name}, last_name: {self._last_name}, id: {self._id}, country_ref: {self._country_ref}"

Customer.counter = 0
