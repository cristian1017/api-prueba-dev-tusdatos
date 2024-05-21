from selenium.webdriver.common.by import By
from datetime import datetime
from app.config import is_get_activity_for_actuaciones_judiciales


class Utils:
    @staticmethod
    def format_init(data, process_id, process_type):
        """
        Formats the given data into a dictionary with the process ID as the key and a list of process details as the value.

        Args:
            data (list): A list of web elements representing processes.
            process_id (str): The ID of the process.
            process_type (str): The type of the process. Can be either "demandado" or "demandante".

        Returns:
            dict: A dictionary with the process ID as the key and a list of process details as the value. Each process detail is a dictionary with the following keys:
                - type (str): The type of the process. Can be either "demandado" or "demandante".
                - fechaIngreso (str): The date of the process.
                - idJuicio (str): The ID of the process.
                - details (dict): A dictionary with the following key:
                    - nombreDelito (str): The name of the crime.

        """
        datos_procesos = []
        for process in data:
            try:
                id_juicio = process.find_element(
                    By.CSS_SELECTOR, ".numero-proceso").text or ""
                fecha = process.find_element(
                    By.CSS_SELECTOR, ".fecha").text.strip() or ""
                accion = process.find_element(
                    By.CSS_SELECTOR, ".accion-infraccion").text.strip() or ""

                datos_procesos.append({
                    'type': 'demandado' if process_type == 'demandado' else 'demandante',
                    'fechaIngreso': fecha,
                    'idJuicio': id_juicio,
                    'details': {
                        'nombreDelito': accion,
                    }
                })
            except:
                continue

        return {process_id: datos_procesos}

    @staticmethod
    def format_data_sub_process(data):
        """
        Formats the given data into a list of dictionaries with the process information.

        Args:
            data (list): A list of dictionaries representing processes.

        Returns:
            list: A list of dictionaries with the following keys:
                - ciudad (str): The city of the process. Defaults to 'No disponible' if not available.
                - demandantes (list): A list of the names of the demandants. Defaults to a list with 'No disponible' if not available.
                - demandados (list): A list of the names of the defendants. Defaults to a list with 'No disponible' if not available.
                - idJudicatura (str): The ID of the judicial court. Defaults to 'No disponible' if not available.
                - idIncidenteJudicatura (str): The ID of the incident in the judicial court. Defaults to 'No disponible' if not available.
                - idMovimientoJuicioIncidente (str): The ID of the court process incident. Defaults to 'No disponible' if not available.
                - incidente (str): The name of the incident. Defaults to 'No disponible' if not available.
                - nombreJudicatura (str): The name of the judicial court. Defaults to 'No disponible' if not available.
        """
        extracted_data = []
        for process in data:
            format_data = {
                'ciudad': process.get('ciudad', 'No disponible'),
                'demandantes': [demandante.get('nombresLitigante', 'No disponible') for demandante in process['lstIncidenteJudicatura'][0]['lstLitiganteActor'] or []],
                'demandados': [demandado.get('nombresLitigante', 'No disponible') for demandado in process['lstIncidenteJudicatura'][0]['lstLitiganteDemandado'] or []],
                'idJudicatura': process.get('idJudicatura', 'No disponible'),
                'idIncidenteJudicatura': process['lstIncidenteJudicatura'][0].get('idIncidenteJudicatura', 'No disponible'),
                'idMovimientoJuicioIncidente': process['lstIncidenteJudicatura'][0].get('idMovimientoJuicioIncidente', 'No disponible'),
                'incidente': process['lstIncidenteJudicatura'][0].get('incidente', 'No disponible'),
                'nombreJudicatura': process.get('nombreJudicatura', 'No disponible'),
            }

            extracted_data.append(format_data)

        return extracted_data

    @staticmethod
    def format_data_actuaciones_judiciales(data):
        """
        Formats the given data into a list of dictionaries with the information of judicial acts.

        Parameters:
            data (list): A list of dictionaries representing judicial acts.

        Returns:
            list: A list of dictionaries with the following keys:
                - 'codigo' (str): The code of the judicial act.
                - 'fecha' (str): The date of the judicial act in ISO format.
                - 'hour' (str): The time of the judicial act in ISO format.
                - 'idJudicatura' (str): The ID of the judicial court.
                - 'nombreArchivo' (str): The name of the file.
                - 'tipo' (str): The type of the judicial act.
                - 'actividad' (str, optional): The activity of the judicial act (only if is_get_activity_for_actuaciones_judiciales is True).

        """
        extracted_data = []
        for act_jud in data:
            dt = datetime.fromisoformat(act_jud.get(
                'fecha', 'No disponible').replace('Z', '+00:00'))
            format_data = {
                'codigo': act_jud.get('codigo', 'No disponible'),
                'fecha': dt.date().isoformat(),
                'hour': dt.time().isoformat(),
                'idJudicatura': act_jud.get('idJudicatura', 'No disponible'),
                'nombreArchivo': act_jud.get('nombreArchivo', 'No disponible').strip(),
                'tipo': act_jud.get('tipo', 'No disponible').strip(),
            }

            if is_get_activity_for_actuaciones_judiciales:
                format_data['actividad'] = act_jud.get(
                    'actividad', 'No disponible')

            extracted_data.append(format_data)
        return extracted_data

    @staticmethod
    def format_data_payload(data):
        """
        Formats the given data into a dictionary with specific key-value pairs excluded.

        Args:
            data (dict): The dictionary containing the data to be formatted.

        Returns:
            dict: A formatted dictionary with the excluded key-value pairs removed and an additional key-value pair added.

        """
        format = {key: value for key, value in data.items() if key not in [
            'ciudad', 'demandantes', 'demandados']}
        format['aplicativo'] = 'web'
        return format

    @staticmethod
    def extract_info_sub_process(data):
        """
        Extracts information from a list of processes and returns a list of subprocesses with an added 'idJuicio' field.

        Args:
            data (list): A list of dictionaries representing processes. Each dictionary should have the following keys:
                - 'idJuicio' (str): The ID of the process.
                - 'details' (dict): A dictionary containing the details of the process. It should have the following keys:
                    - 'subProcess' (list): A list of dictionaries representing subprocesses. Each dictionary should have the following keys:
                        - Any key-value pairs representing the details of the subprocess.

        Returns:
            list: A list of dictionaries representing subprocesses. Each dictionary will have an additional key:
                - 'idJuicio' (str): The ID of the process.
        """
        subprocess_list = []
        for process in data:
            id_juicio = process.get("idJuicio")
            for subprocess in process["details"]["subProcess"]:
                subprocess_with_id = subprocess.copy()
                subprocess_with_id["idJuicio"] = id_juicio
                subprocess_list.append(subprocess_with_id)
        return subprocess_list

    @staticmethod
    def count_demandante_demandado(data):
        """
        Counts the number of items in the given data list that have a 'type' field equal to 'demandante' and 'demandado'.

        :param data: A list of dictionaries. Each dictionary should have a 'type' field.
        :type data: list[dict[str, Any]]
        :return: A dictionary with the counts of 'demandante' and 'demandado' items.
        :rtype: dict[str, int]
        """
        count_demandante = sum(
            1 for item in data if item['type'] == 'demandante')
        count_demandado = sum(
            1 for item in data if item['type'] == 'demandado')

        return {"count_demandante": count_demandante, "count_demandado": count_demandado}
