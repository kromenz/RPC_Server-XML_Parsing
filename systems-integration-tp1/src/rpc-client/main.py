from argparse import _AppendAction
import os
import time
import xmlrpc.client 
from xmlrpc.client import Fault

def clean():
    input("\nEnter para avançar")
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('printf "\033c"')  
    
def sleeping():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(1)  

def list_documents():
    documents = server.index()
    if len(documents) > 0:
        print("Listing all documents:")
        for doc in documents:
            print(f"  - {doc[1]}")
        return len(documents)
    else:
        print("Documents list is empty!")
        return 0

def delete_document():
    size = list_documents()

    if size > 0:
        filename = input("\nInsert filename: ")

        if not filename.strip():
            print("No document was selected...")
            return

        try:
            server.delete_document(filename)
            print(f"Document '{filename}' has been deleted successfuly!")
        except Fault as e:
            print(e.faultString)

def insert_document():
    xsd_path = "/data/schemas/cars.xsd"
    try:
        xml_file = input("Introduza o nome do ficheiro XML (introduza o ficheiro em docker/volumes/data/, sem .xml): ")
        xml_file_path = "/data/" + xml_file + ".xml"
        
        if not xml_file_path:
            print("No XML file selected")
            return
        
        with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()
        server.insert_document(xml_file_path, xml_content)
        # if server.validate_xml_with_xsd(xml_content, xsd_path):
        #     server.insert_document(xml_file_path, xml_content)
        # else:
        #     print("Falhou a validação do xml, tente outro ficheiro.")
    except Exception as e:
        print(f"Error: {e}")
        
def list_brands():
    try:
        brands = server.fetch_brands()
        if brands:
            print("\nList of Brands:")
            for brand in brands:
                print(f"- {brand}")
                
        else:
            print("No brands found.")
            
        clean()
    except Exception as e:
        print(f"Error: {e}")
        
def list_car_models():
    brand_name = input("\nDigite o nome da marca para listar os modelos: ")
    sleeping()
    try:
        models = server.fetch_car_models(brand_name)
        if models:
            print(f"\nList of Models for {brand_name}:")
            for model in models:
                print(f"- {model}")
              
        else:
            print(f"\nNo models found for {brand_name}.")
            
        clean() 
    except Exception as e:
        print(f"Error: {e}")
        
def list_countries():
    try:

        sales_per_country = server.sales_per_country()

        if sales_per_country:
            print("\nNumber of Sales per Country:")
            for country, count in sales_per_country.items():
                print(f"- {country} - {count}")
        else:
            print("No sales found.")

        clean()
    except Exception as e:
        print(f"Error: {e}")

def list_oldest_car():
    try:
        oldest_car_details = server.oldest_sold_car_details()
        if oldest_car_details:
            print("Detalhes do carro mais antigo vendido:")
            for key, value in oldest_car_details.items():
                print(f"{key}: {value}")
        else:
            print("Não há informações suficientes para determinar o carro mais antigo vendido.")
    except Exception as e:
        print(f"Error: {e}")
    
    clean()
    
def list_newest_car():
    try:
        newest_car_details = server.newest_sold_car_details()
        if newest_car_details:
            print("Detalhes do carro mais recente vendido:")
            for key, value in newest_car_details.items():
                print(f"{key}: {value}")
        else:
            print("Não há informações suficientes para determinar o carro mais recente vendido.")
    except Exception as e:
        print(f"Error: {e}")
    
    clean()
    
def most_sold_colors():
    try:
        most_sold_colors_data = server.most_sold_colors()
        if most_sold_colors_data:
            print("Cores com maior percentagem de venda:")
            for color, percentage in most_sold_colors_data.items():
                print(f"{color}: {percentage:.2f}%")
        else:
            print("Não há informações suficientes para determinar as cores mais vendidas.")
    except Exception as e:
        print(f"Error: {e}")
    
    clean()   
    
def most_sold_brands():
    try:
        most_sold_brands_data = server.most_sold_brands()
        if most_sold_brands_data:
            print("Marcas com maior percentagem de venda:")
            for brand, percentage in most_sold_brands_data.items():
                print(f"{brand}: {percentage:.2f}%")
        else:
            print("Não há informações suficientes para determinar as marcas mais vendidas.")
    except Exception as e:
        print(f"Error: {e}")

    clean()

def most_sold_models():
    try:
        most_sold_models_data = server.most_sold_models()
        if most_sold_models_data:
            print("Modelos com maior percentagem de venda:")
            for model, percentage in most_sold_models_data.items():
                print(f"{model}: {percentage:.2}%")
        else:
            print("Não há informações suficientes para determinar os modelos mais vendidos.")
    except Exception as e:
        print(f"Error: {e}")

    clean()
  
def car_year():
    try:
        year = input("Enter the year to search for cars: ")
        car_details = server.car_year(year)

        if car_details:
            print(f"\nCar details for the year {year}:\n")
            for detail in car_details:
                print(f"Customer: {detail['Customer']}\nCar: {detail['Brand']} {detail['Model']}\nColor: {detail['Color']}\n")
        else:
            print(f"No car details found for the year {year}.")

    except Exception as e:
        print(f"Error: {e}")

    clean()

def file_exists(file):
    try:

        result = server.file_exists(file)
        
        return result

    except Exception as e:
        print(f"Error calling file_exists RPC: {e}")
        return False

def file_exists_loop():

    while True:
        list_documents()
        ficheiro = input("Por favor introduza o nome do ficheiro que pretende trabalhar: ")
        
        if file_exists(ficheiro):
            os.system('printf "\033c"')  
            menu()
            break
        else:
            print("O ficheiro não existe. Tente novamente.")
            clean()

def menu():
    while True:
        print("1. Documentos")
        print("2. Listagens")
        print("3. Curiosidades ")
        print("4. Estatísticas")
        print("0. Sair")
        choice = input("Escolha uma opção: ")
        os.system('printf "\033c"')
        if choice == '1':
            while True:
                os.system('printf "\033c"')
                print("\nDocumentos:")
                print("1. Listar documentos")
                print("2. Inserir documento")
                print("3. Apagar documento")
                print("0. Voltar ao menu principal")

                sub_choice = input("Escolha uma opção: ")
                os.system('printf "\033c"')

                if sub_choice == '1':
                    list_documents()
                    clean()
                if sub_choice == '2':
                    insert_document()
                    clean()
                elif sub_choice == '3':
                    delete_document()
                    clean()
                elif sub_choice == '0':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                    
        elif choice == '2':
            while True:
                print("\nListagens:")
                print("1. Listar Brands")
                print("2. Pesquisar Modelos")
                print("3. Pesquisar Carros Através do Ano")
                print("4. Listar Número de Vendas Por País")
                print("0. Voltar ao menu principal")

                sub_choice = input("Escolha uma opção: ")
                os.system('printf "\033c"')

                if sub_choice == '1':
                    list_brands()
                elif sub_choice == '2':
                    list_car_models()
                elif sub_choice == '3':
                    car_year()
                elif sub_choice == '4':
                    list_countries()
                elif sub_choice == '0':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        
        elif choice == '3':
            while True:
                print("\nCuriosidades:")
                print("1. Listar a venda do carro mais antigo")
                print("2. Listar a venda carro mais recente")
                print("0. Voltar ao menu principal")

                sub_choice = input("Escolha uma opção: ")
                os.system('printf "\033c"')

                if sub_choice == '1':
                    list_oldest_car()
                elif sub_choice == '2':
                    list_newest_car()
                elif sub_choice == '0':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        
        elif choice == '4':
            while True:
                print("\nEstatísticas:")           
                print("1. Listar a cor de carro mais vendida")
                print("2. Listar a Marca mais comprada")
                print("3. Listar o Modelo mais comprado")
                print("0. Voltar ao menu principal")

                sub_choice = input("Escolha uma opção: ")
                os.system('printf "\033c"')
                
                if sub_choice == '1':
                    most_sold_colors()
                if sub_choice == '2':
                    most_sold_brands()
                if sub_choice == '3':
                    most_sold_models()
                elif sub_choice == '0':
                    break
                else:
                    print("Opção inválida. Tente novamente.")


        elif choice == '0':
            print("\nIt was a pleasure to have you with us!\nSee you soon!")
            time.sleep(2)
            break

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

sleeping()

file_exists_loop()