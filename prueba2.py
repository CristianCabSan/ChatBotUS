import requests
import xml.etree.ElementTree as ET

def make_query(parameter):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pmc',
        'term': parameter,
        'maxdate': '2021',
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        # Parse the XML response
        root = ET.fromstring(response.content)

        # Find the IdList element
        id_list_element = root.find(".//IdList")

        # Output the IdList element and its content
        if id_list_element is not None:
            id_list_content = ET.tostring(id_list_element, encoding='unicode')
            print("IdList:\n{}".format(id_list_content))
        else:
            print("IdList not found in the XML response.")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

# Example usage:
user_input = input("Enter the parameter: ")
make_query(user_input)
