import xmlrpc.client 

def list_documents():
    documents = server.list_documents()
    for doc in documents:
        print(doc[0])  # Supondo que 'doc' seja uma tupla com o nome do arquivo

def delete_document():
    file_name = input("Digite o nome do arquivo para excluir: ")
    if server.delete_document(file_name):
        print("Documento excluído com sucesso.")
        
def list_brands():
    try:
        brands = server.fetch_brands()
        if brands:
            print("List of Brands:")
            for brand in brands:
                print(f"- {brand}")
        else:
            print("No brands found.")
    except Exception as e:
        print(f"Error: {e}")

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

while True:
    print("1. Listar documentos")
    print("2. Deletar documento")
    print("3. Listar Brands")
    print("0. Sair")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        list_documents()
    elif choice == '2':
        delete_document()
    elif choice == '3':
        list_brands()
    elif choice == '0':
        break