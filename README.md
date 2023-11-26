# RPC_Server - XML_Parsing

In this repository you will find code that essentially serves as a data transformation tool, taking information from a CSV file, converting it into XML, and storing it in an PostGres database. The code ensures that the database table structure matches the data being inserted. It's particularly useful for converting structured data from one format (CSV) to another (XML and PostGres) for further analysis or use.

## Functionalities

- Read a CSV file containing car-related data (first name, last name, country, car brand, car model, car color, year of manufacture, credit card type).

- Convert the data from the CSV file into an XML format.

- Validate the XML format according to a XSD file.

- Connect to an PostGres database, sending the XML created to the database.

- Queries using xpath to search in the XML file.

- The user can put another XML file in the database.

## Running the program

Create Docker Images and Containers - Navigate to the project's root folder (systems-integration-tp1) and execute the following command:

```
  docker-compose up --build
```
That command will create and start up the enviroment we will be working in.
The next step is to open a new terminal and run the following command:

```
  docker-compose run rpc-client
```
This will be running the rpc-client that is the interface created for the user, to execute commands, that will be processed by the rpc-server, and then returned to the client.

### WARNING

If errors appear, do the following command:
```
docker-compose down
```
And then just do the first command again, after that use the second command to created the enviroment used by the client to execute the program.

## Stacks

![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![PostGres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)

# Authors

- [@DiogoBernardes](https://github.com/DiogoBernardes) - 27984
- [@RafaelAndré](https://github.com/kromenz) - 28234
- [@SérgioBarbosa](https://github.com/Oigres2) - 26211
- [GithubRepo](https://github.com/kromenz/RPC_Server-XML_Parsing)

#### _Engenharia Informática @ipvc/estg, 2023-2024_
