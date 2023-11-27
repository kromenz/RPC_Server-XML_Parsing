CREATE TABLE public.Country (
    id serial PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE public.Brand (
    id serial PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE public.CreditCard_Type (
    id serial PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE public.Model (
    id serial PRIMARY KEY,
    name VARCHAR(50),
    brand_id integer REFERENCES Brand(id)
);

CREATE TABLE public.Customer (
    id serial PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    country_id integer REFERENCES Country(id)
);

CREATE TABLE public.Car (
    id serial PRIMARY KEY,
    color VARCHAR(50),
    year INTEGER,
    model_id integer REFERENCES Model(id)
);

CREATE TABLE public.Sale (
    id serial PRIMARY KEY,
    car_id integer REFERENCES Car(id),
    customer_id integer REFERENCES Customer(id),
    credit_card_type_id integer REFERENCES CreditCard_Type(id)
);