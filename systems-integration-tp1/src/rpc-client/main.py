import os
import time
import xmlrpc.client 

def clean():
    input("\nEnter para avançar")
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('printf "\033c"')  
    
def sleeping():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(1) 
    
def list_documents():
    documents = server.list_documents()
    for doc in documents:
        print("\nDocumentos: \n")
        print(doc[0])  # Supondo que 'doc' seja uma tupla com o nome do arquivo
        clean()

def delete_document():
    file_name = input("\nDigite o nome do arquivo para excluir: ")
    if server.delete_document(file_name):
        print("Documento excluído com sucesso.")
        clean()
        
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
    
    
print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

sleeping()

while True:
    
    print("1. Listar documentos")
    print("2. Deletar documento")
    print("3. Listar Brands")
    print("4. Listar Modelos por Marca")
    print("5. Listar vendas por país")
    print("6. Estatisticas ")
    print("0. Sair")
    choice = input("Escolha uma opção: ")
    os.system('printf "\033c"')
    if choice == '1':
        list_documents()
    elif choice == '2':
        delete_document()
    elif choice == '3':
        list_brands()
    elif choice == '4':
        list_car_models()
    elif choice == '5':
        list_countries()
    elif choice == '6':
        while True:
            print("\nEstatísticas:")
            print("1. Listar a venda do carro mais antigo")
            print("2. Listar a venda carro mais recente")
            print("3. Listar a cor de carro mais vendida")
            print("0. Voltar ao menu principal")

            sub_choice = input("Escolha uma opção de estatística: ")
            os.system('printf "\033c"')

            if sub_choice == '1':
                list_oldest_car()
            elif sub_choice == '2':
                list_newest_car()
            elif sub_choice == '3':
                most_sold_colors()
            elif sub_choice == '0':
                break
            else:
                print("Opção inválida. Tente novamente.")


    elif choice == '0':
        print("\nIt was a pleasure to have you with us!\nSee you soon!")
        time.sleep(2)
        break