import xml.etree.ElementTree as ET
from entities.car import Car
from entities.card import CreditCard
from entities.customer import Customer

class Sale:

    def __init__(self):
        Sale.counter += 1
        self._id = Sale.counter
        self._customers = []
        self._cars= []
        self._creditCard = []

    def add_car(self, car: Car):
        self._cars.append(car)

    def add_creditCard(self, creditCard: CreditCard):
        self._creditCards.append(creditCard)

    def add_customer(self, customer: Customer): 
        self._customers.append(customer)

    def to_xml(self):
        el = ET.Element("Sale")
        el.set("id", str(self._id))

        cars_el  = ET.Element("Car")
        for car in self._cars:
            cars_el.append(car.to_xml())
        el.append(cars_el)

        customer_el  = ET.Element("Customer")
        for customer in self._customers:
            customer_el.append(customer.to_xml())
        el.append(customer_el)

        creditCard_el  = ET.Element("Credit Card")
        for card in self._creditCard:
            creditCard_el.append(card.to_xml())
        el.append(creditCard_el)

        return el
    
Sale.counter=0
