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


print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

sleeping()

while True:
    
    print("1. Listar documentos")
    print("2. Deletar documento")
    print("3. Listar Brands")
    print("4. Listar Modelos por Marca")
    print("5. Listar Número de Vendas por País")
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
    elif choice == '0':
        print("\nIt was a pleasure to have you with us!\nSee you soon!")
        time.sleep(2)
        break