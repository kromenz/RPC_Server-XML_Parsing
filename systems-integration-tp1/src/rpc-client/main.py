from argparse import _AppendAction
import os
import time
import xmlrpc.client 
from xmlrpc.client import Fault

current_file = None

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
        print("Lista de documentos:")
        for doc in documents:
            print(f"  - {doc[1]}")
        return len(documents)
    else:
        print("A lista de documento está vazia!")
        return 0

def delete_document():
    size = list_documents()

    if size > 0:
        filename = input("\nIntroduza o nome do ficheiro que pretende apagar: ")

        if not filename.strip():
            print("Não foi selecionado nenhum documento...")
            return

        try:
            server.delete_document(filename)
            print(f"O documento '{filename}' foi apagado com sucesso!")
        except Fault as e:
            print(e.faultString)

def insert_document():
    
        xml_file = input("Introduza o nome do ficheiro XML (introduza o ficheiro em docker/volumes/data/, sem .xml): ")
        xml_file_path = "/data/" + xml_file + ".xml"
        
        if not xml_file_path:
            print("No XML file selected")
            return
        
        with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()
            
        try:
            server.insert_document(xml_file_path, xml_content)
            print(f"O ficheiro {xml_file}, foi inserido com sucesso!")
            
        except Exception as e:
            print(f"Ocorreu um erro ao inserir o ficheiro {xml_file}...")
            print(f"Error: {e}")
        
def list_brands():
    try:
        if current_file:
            brands = server.fetch_brands(current_file)
            print("\nLista de Marcas:")
            for brand in brands:
                print(f"- {brand}")
                
        else:
            print("No brands found.")
            
    except Exception as e:
        print(f"Error: {e}")
        
def list_car_models():
    brand_name = input("\nDigite o nome da marca para listar os modelos: ")
    sleeping()
    try:
        if current_file:
            models = server.fetch_car_models(current_file, brand_name)
            if models:
                print(f"\nLista dos Modelos da {brand_name}:")
                for model in models:
                    print(f"- {model}")
            else:
                print(f"\nNão foram encontrados modelos da {brand_name}.")
        else:
            print("Nenhum arquivo selecionado.")
    except Exception as e:
        print(f"Error: {e}")

def list_countries():
    try:
        if current_file:
            sales_per_country = server.sales_per_country(current_file)
            if sales_per_country:
                print("\nNúmero de vendas por país:")
                for country, count in sales_per_country.items():
                    print(f"- {country} - {count}")
            else:
                print("Não foram encontradas vendas.")
        else:
            print("Nenhum arquivo selecionado.")

    except Exception as e:
        print(f"Error: {e}")

def list_oldest_car():
    try:
        if current_file:
            oldest_car_details = server.oldest_sold_car_details(current_file)
            if oldest_car_details:
                print("Detalhes do carro mais antigo vendido:")
                for key, value in oldest_car_details.items():
                    print(f"{key}: {value}")
            else:
                print("Não há informações suficientes para determinar o carro mais antigo vendido.")
        else:
            print("Nenhum arquivo selecionado.")

    except Exception as e:
        print(f"Error: {e}")

def list_newest_car():
    try:
        if current_file:
            newest_car_details = server.newest_sold_car_details(current_file)
            if newest_car_details:
                print("Detalhes do carro mais recente vendido:")
                for key, value in newest_car_details.items():
                    print(f"{key}: {value}")
            else:
                print("Não há informações suficientes para determinar o carro mais recente vendido.")
        else:
            print("Nenhum arquivo selecionado.")

    except Exception as e:
        print(f"Error: {e}")
    
def most_sold_colors():
    try:
        if current_file:
            most_sold_colors_data = server.most_sold_colors(current_file)
            if most_sold_colors_data:
                print("Cores com maior percentagem de venda:")
                for color, percentage in most_sold_colors_data.items():
                    print(f"{color}: {percentage:.2f}%")
            else:
                print("Não há informações suficientes para determinar as cores mais vendidas.")
        else:
            print("Nenhum arquivo selecionado.")

    except Exception as e:
        print(f"Error: {e}")   
    
def most_sold_brands():
    try:
        if current_file:
            most_sold_brands_data = server.most_sold_brands(current_file)
            if most_sold_brands_data:
                print("Marcas com maior percentagem de venda:")
                for brand, percentage in most_sold_brands_data.items():
                    print(f"{brand}: {percentage:.2f}%")
            else:
                print("Não há informações suficientes para determinar as marcas mais vendidas.")
        else:
            print("Nenhum arquivo selecionado.")

    except Exception as e:
        print(f"Error: {e}")

def most_sold_models():
    try:
        if current_file:
            most_sold_models_data = server.most_sold_models(current_file)
            if most_sold_models_data:
                print("Modelos com maior percentagem de venda:")
                for model, percentage in most_sold_models_data.items():
                    print(f"{model}: {percentage:.2}%")
            else:
                print("Não há informações suficientes para determinar os modelos mais vendidos.")
        else:
            print("Nenhum arquivo selecionado.")

    except Exception as e:
        print(f"Error: {e}")
  
def car_year():
    try:
        if current_file:
            year = input("Introduza o ano que pretende procurar: ")
            car_details = server.car_year(year, current_file)

            if isinstance(car_details, list):
                if not car_details:
                    print(f"Não foram encontrados detalhes para o ano {year}.")
                    return

                page_size = 20  # Número de registros por página
                total_records = len(car_details)
                total_pages = (total_records + page_size - 1) // page_size

                current_page = 1

                while True:
                    start_index = (current_page - 1) * page_size
                    end_index = start_index + page_size
                    current_page_details = car_details[start_index:end_index]
                    os.system('printf "\033c"') 
                    print(f"\nDetalhes das compras cujos carros têm o ano {year} (Página {current_page} de {total_pages}):\n")
                    for detail in current_page_details:
                        print(f"Client: {detail['Customer']}\nCarro: {detail['Brand']} {detail['Model']}\nCor: {detail['Color']}\n")

                    user_input = input("\nDigite 'n' para próxima página, 'p' para página anterior, '0' para sair: ")
                    if user_input == 'n':
                        current_page = min(current_page + 1, total_pages)
                    elif user_input == 'p':
                        current_page = max(current_page - 1, 1)
                    elif user_input == '0':
                        print("A sair...")
                        break
                    else:
                        print("Comando inválido. Tente novamente.")
            else:
                print(car_details)

        else:
            print("Nenhum arquivo selecionado.")
    except Exception as e:
        print(f"Error: {e}")

def file_exists(file):
    try:
        result = server.file_exists(file)
        return result

    except Exception as e:
        print(f"Error calling file_exists RPC: {e}")
        return False

def file_exists_loop():
    global current_file
    while True:
        list_documents()
        filename = input("Por favor introduza o nome do ficheiro que pretende trabalhar: ")
        if server.file_exists(filename):
            current_file = filename
            os.system('printf "\033c"')
            menu()
            break
        else:
            print("O ficheiro não existe. Tente novamente.")

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
                os.system('printf "\033c"')
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
                    clean()
                elif sub_choice == '2':
                    list_car_models()
                    clean()
                elif sub_choice == '3':
                    car_year()
                    clean()
                elif sub_choice == '4':
                    list_countries()
                    clean()
                elif sub_choice == '0':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        
        elif choice == '3':
            while True:
                os.system('printf "\033c"')
                print("\nCuriosidades:")
                print("1. Listar a venda do carro mais antigo")
                print("2. Listar a venda carro mais recente")
                print("0. Voltar ao menu principal")

                sub_choice = input("Escolha uma opção: ")
                os.system('printf "\033c"')

                if sub_choice == '1':
                    list_oldest_car()
                    clean()
                elif sub_choice == '2':
                    list_newest_car()
                    clean()
                elif sub_choice == '0':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        
        elif choice == '4':
            while True:
                os.system('printf "\033c"')
                print("\nEstatísticas:")           
                print("1. Listar a cor de carro mais vendida")
                print("2. Listar a Marca mais comprada")
                print("3. Listar o Modelo mais comprado")
                print("0. Voltar ao menu principal")

                sub_choice = input("Escolha uma opção: ")
                os.system('printf "\033c"')
                
                if sub_choice == '1':
                    most_sold_colors()
                    clean()
                if sub_choice == '2':
                    most_sold_brands()
                    clean()
                if sub_choice == '3':
                    most_sold_models()
                    clean()
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