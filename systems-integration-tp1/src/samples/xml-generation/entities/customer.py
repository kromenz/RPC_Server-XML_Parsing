import xml.etree.ElementTree as ET
from entities.country import Country

class Customer:

    def __init__(self, first_name, last_name, country):
        Customer.counter += 1
        self._id = Customer.counter
        self._first_name = first_name
        self._last_name = last_name
        self._country = country

    def to_xml(self):
        el = ET.Element("Customer")
        el.set("id", str(self._id))
        el.set("first_name", self._first_name)
        el.set("last_name", self._last_name)
        el.set("countryRef", self._country_ref)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"first_name: {self._first_name}, last_name: {self._last_name}, id: {self._id}, country_ref: {self._country_ref}"

Customer.counter = 0
