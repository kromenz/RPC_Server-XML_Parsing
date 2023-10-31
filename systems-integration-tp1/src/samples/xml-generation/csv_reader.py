from csv import DictReader

class CSVReader:

    def __init__(self, path, delimiter=','):
        self._path = path
        self._delimiter = delimiter

    def loop(self):
        with open(self._path, 'r') as file:
            for row in DictReader(file, delimiter=self._delimiter):
                yield row

    def read_entities(self, attr, builder, after_create=None):
        entities = {}
        for row in self.loop():
            e = row[attr]
            if e not in entities:
                entities[e] = builder(row)
                if after_create is not None:
                    after_create(entities[e], row)

        return entities

# Caminho para o arquivo CSV
csv_path = 'docker/volumes/data/cars.csv'

# Exemplo de como usar a classe CSVReader para ler o arquivo CSV
def build_car_entity(row):
    return {
        'First Name': row['First Name'],
        'Last Name': row['Last Name'],
        'Country': row['Country'],
        'Car Brand': row['Car Brand'],
        'Car Model': row['Car Model'],
        'Car Color': row['Car Color'],
        'Year of Manufacture': row['Year of Manufacture'],
        'Credit Card Type': row['Credit Card Type']
    }

reader = CSVReader(csv_path)

# Lê o arquivo CSV e cria as entidades com base no atributo 'First Name'
car_entities = reader.read_entities(attr='First Name', builder=build_car_entity)

# Imprime as entidades
for first_name, car_info in car_entities.items():
    print(f"First Name: {first_name}, Car Model: {car_info['Car Model']}, Car Brand: {car_info['Car Brand']}")
