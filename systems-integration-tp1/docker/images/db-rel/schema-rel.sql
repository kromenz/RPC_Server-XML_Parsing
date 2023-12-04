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

-- Insert data into Country table
INSERT INTO public.Country (name) VALUES ('United States');

-- Insert data into Brand table
INSERT INTO public.Brand (name) VALUES ('Toyota');

-- Insert data into CreditCard_Type table
INSERT INTO public.CreditCard_Type (name) VALUES ('Visa');

-- Insert data into Model table
INSERT INTO public.Model (name, brand_id) VALUES ('Camry', 1); -- Assuming Toyota has id 1

-- Insert data into Customer table
INSERT INTO public.Customer (first_name, last_name, country_id) VALUES ('John', 'Doe', 1); -- Assuming United States has id 1

-- Insert data into Car table
INSERT INTO public.Car (color, year, model_id) VALUES ('Blue', 2022, 1); -- Assuming Camry has id 1

-- Insert data into Sale table
INSERT INTO public.Sale (car_id, customer_id, credit_card_type_id) VALUES (1, 1, 1); -- Assuming the car, customer, and credit card type have ids 1
