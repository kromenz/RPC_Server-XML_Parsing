# RPC_Server - XML_Parsing

In this repository you will find code that essentially serves as a data transformation tool, taking information from a CSV file, converting it into XML, and storing it in an PostGres database. The code ensures that the database table structure matches the data being inserted. It's particularly useful for converting structured data from one format (CSV) to another (XML and PostGres) for further analysis or use.

## Functionalities

- Read a CSV file containing car-related data (e.g., first name, last name, country, car brand, car model, car color, year of manufacture, credit card type).

- Convert the data from the CSV file into an XML format.

- Create or connect to an PostGres database named "cars.db."

- If the "cars" table does not exist in the database, it is created with specific column names.

- Parse the generated XML data and insert the information into the "cars" table in the SQLite database.

- Commit the changes to the database and close the database connection.

## Running th program

Create Docker Images and Containers - Navigate to the project's root folder and execute the following command:

```
  docker-compose up --build
```
That command will create and start up the enviroment we will be working in.
The next step is to open a new terminal and run the following command:

```py
  docker-compose run rpc-client
```
This will be running the rpc-client that is the interface created for the user, to execute commands, that will be processed by the rpc-server, and then returned to the client.

## Stacks

![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![PostGres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)

# Authors

- [@RafaelAndré](https://github.com/kromenz) - 28234
- [@DiogoBernardes](https://github.com/DiogoBernardes) - 27984
- [@SérgioBarbosa](https://github.com/Oigres2) - 26211
- [GithubRepo](https://github.com/kromenz/RPC_Server-XML_Parsing)

#### _Engenharia Informática @ipvc/estg, 2023-2024_
