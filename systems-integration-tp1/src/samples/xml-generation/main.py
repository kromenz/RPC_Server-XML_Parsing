from csv_to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":
    converter = CSVtoXMLConverter("/data/cars.csv")
    print(converter.to_xml_str())
    
    output_file_path = "/data/cars.xml"
    converter.save_to_file(output_file_path)

    print(f"XML salvo em: {output_file_path}")
    # Substitua com o caminho do seu arquivo XML e XSD
    arquivo_xml = "/data/cars.xml"
    arquivo_xsd = "/data/schemas/cars.xsd"

    CSVtoXMLConverter.validar_xml_com_xsd(arquivo_xml, arquivo_xsd)