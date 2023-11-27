import requests
import xml.etree.ElementTree as ET

def listarIDs(list_content):
    try:
        root = ET.fromstring(list_content)
        id_elements = root.findall(".//Id")

        # Extract and return the ids as an array
        IDs = [id_element.text for id_element in id_elements]
        return IDs

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

def make_query(parameter):
    #Makes the initial query to get the ID of the related papers using the esearch function
    urlEsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    paramsEsearch = {
        'db': 'pmc',
        'term': parameter,
        'maxdate': '2021',
    }

    try:
        response = requests.get(urlEsearch, params=paramsEsearch)
        response.raise_for_status() #Error control

        # Parse the XML response
        xmlEsearch = ET.fromstring(response.content)

        # Find the IdList element
        id_list_element = xmlEsearch.find(".//IdList")

        # Output the IdList element and its content
        if id_list_element is not None:
            id_list_content = ET.tostring(id_list_element, encoding='unicode')
            IDs = listarIDs(id_list_content)
            urlIDs = [f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC{pmc_id}/unicode"for pmc_id in IDs]
            
        else:
            print("IdList not found in the XML response.")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
# Example usage:
user_input = input("Enter the parameter: ")
make_query(user_input)




