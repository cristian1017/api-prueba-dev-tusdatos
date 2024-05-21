from app.utils.utils import Utils
from concurrent.futures import ThreadPoolExecutor
import requests


class FetchServices:
    def __init__(self):
        self.url = "https://api.funcionjudicial.gob.ec"

    def fetch_actuaciones_judiciales(self, payload):
        """
        Fetches judicial acts based on the given payload.

        Args:
            payload (dict): The payload containing the necessary information for the request.

        Returns:
            dict: A dictionary containing the judicial acts data. If the request is successful, the dictionary will have the format:
                {
                    'idJudicatura': format_data
                }
                where 'idJudicatura' is the ID of the judicial court and 'format_data' is the formatted data of the judicial acts.
            dict: If the request fails, a dictionary with the following keys will be returned:
                {
                    'error': 'Failed to fetch case data',
                    'status_code': response.status_code
                }
                where 'status_code' is the HTTP status code of the response.
            dict: If an exception occurs during the execution of the function, a dictionary with the following key will be returned:
                {
                    'error': str(e)
                }
                where 'str(e)' is the string representation of the exception 'e'.
        """
        try:
            format_payload = Utils.format_data_payload(payload)
            url = f"{self.url}/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/actuacionesJudiciales"
            response = requests.post(url, json=format_payload)
            if response.status_code == 200:
                data = response.json()
                format_data = Utils.format_data_actuaciones_judiciales(data)
                return {payload['idJudicatura']: format_data}
            else:
                return {'error': 'Failed to fetch case data', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}

    def fetch_incidente_judicatura(self, case_id):
        """
        Fetches incident data for a given judicial court case.

        Args:
            case_id (str): The ID of the judicial court case.

        Returns:
            dict: A dictionary containing the formatted incident data if the request is successful. The dictionary has the following keys:
                - 'error' (str): A message indicating the failure to fetch incident data.
                - 'status_code' (int): The HTTP status code of the response.
            dict: If an exception occurs during the execution of the function, a dictionary with the following key will be returned:
                - 'error' (str): The string representation of the exception 'e'.
        """

        try:
            url = f"{self.url}/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/{case_id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                format_data = Utils.format_data_sub_process(data)
                return format_data
            else:
                return {'error': 'Failed to fetch incident data', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}

    def fetch_case_details(self, case_id):
        """
        Fetches details of a judicial case based on its ID.

        Args:
            case_id (str): The ID of the judicial case.

        Returns:
            dict: A dictionary containing the details of the judicial case. If the request is successful, the dictionary will have the following keys:
                - 'nombreTipoAccion' (str): The name of the judicial action type.
                - 'nombreMateria' (str): The name of the judicial subject matter.
                - 'subProcess' (dict): The incident data fetched from the fetch_incidente_judicatura method.
            dict: If the request fails, a dictionary with the following keys will be returned:
                - 'error' (str): A message indicating the failure to fetch data for the case.
                - 'status_code' (int): The HTTP status code of the response.
            dict: If an exception occurs during the execution of the function, a dictionary with the following key will be returned:
                - 'error' (str): The string representation of the exception 'e'.
        """
        try:
            url = f"{self.url}/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/getInformacionJuicio/{case_id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()[0]
                incident_data = self.fetch_incidente_judicatura(case_id)
                extracted_data = {
                    'nombreTipoAccion': data.get('nombreTipoAccion', 'No disponible'),
                    'nombreMateria': data.get('nombreMateria', 'No disponible'),
                    'subProcess': incident_data
                }
                return extracted_data
            else:
                return {'error': f'Failed to fetch data for case {case_id}', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}
