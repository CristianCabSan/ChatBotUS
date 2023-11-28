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
        #Others params such as date, or authors goes here
        'db': 'pmc',
        'maxdate': '2021',
        'term': parameter, # term=parameter
    }

    try:
        response = requests.get(urlEsearch, params=paramsEsearch)
        response.raise_for_status() #Error control

        # Parse the XML response
        xmlEsearch = ET.fromstring(response.content)

        # Get the IdList field
        id_list_element = xmlEsearch.find(".//IdList")

        # Output the IdList element and its content
        id_list_content = ET.tostring(id_list_element, encoding='unicode')
        IDs = listarIDs(id_list_content)
        urlIDs = [f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC{pmc_id}/unicode"for pmc_id in IDs]
        for url in urlIDs:
            file = requests.get(url)
            file.raise_for_status()

            xmlID = ET.fromstring(file.content)
            xmlID2 = xmlID.find("./document/passage")
            xmlID3 = ET.tostring(xmlID2, encoding='unicode')
            print("-----------------PAPER:", url, "----------------\n", xmlID3)


    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")



def buscar_url(parameter):
    #Makes the initial query to get the ID of the related papers using the esearch function
    urlEsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    paramsEsearch = {
        #Others params such as date, or authors goes here
        'db': 'pmc',
        'retmax' : 5 ,
        'term': parameter, # term=parameter
        'field': 'abstract',
        'field': 'title'
    }

    try:
        response = requests.get(urlEsearch, params=paramsEsearch)
        response.raise_for_status() #Error control

        # Parse the XML response
        xmlEsearch = ET.fromstring(response.content)

        # Get the IdList field
        id_list_element = xmlEsearch.find(".//IdList")

        # Output the IdList element and its content
        id_list_content = ET.tostring(id_list_element, encoding='unicode')
        IDs = listarIDs(id_list_content)
        urlIDs = [f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC{pmc_id}/unicode"for pmc_id in IDs]
        i = 0
        for url in urlIDs:
            print(i,": ", url)
            i += 1
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")