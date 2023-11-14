import xml.etree.ElementTree as ET
from lxml import etree

class Brand:
    def __init__(self, name):
        Brand.counter += 1
        self._id = Brand.counter
        self._name = name
        self._models = []

    def add_model(self, model):
        self._models.append(model)

    def to_xml_lxml(self):
        brand_el = etree.Element("Brand", id=str(self._id), name=self._name)
        
        # Incluindo modelos dentro da marca
        for model in self._models:
            model_el = etree.SubElement(brand_el, "Model", id=str(model._id), name=model._name)
        
        return brand_el

Brand.counter = 0