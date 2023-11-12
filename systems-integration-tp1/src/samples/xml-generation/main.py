from csv_to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":

    csv_archieve = "/data/cars.csv"
    output_file_path = "/data/cars.xml"
    xsd_archieve = "/data/schemas/cars.xsd"

    converter = CSVtoXMLConverter(csv_archieve)
    print(converter.to_xml_str(output_file_path,xsd_archieve))
    

  