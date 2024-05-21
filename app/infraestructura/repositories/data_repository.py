import json
import os


class DataRepository:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'data.json')

    def get_data(self):
        """
        Retrieves the data from the JSON file at the specified path.

        Returns:
            list: A list of keys from the JSON data if the file exists, an empty list otherwise.
            Exception: If there is an error while reading the JSON file.
        """
        try:
            if not os.path.exists(self.path):
                return []

            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return list(data.keys()) or []
        except Exception as e:
            return e

    def reset_data(self):
        """
        Resets the data by removing the file at the specified path if it exists.

        This function checks if the file at the path specified by the `path` attribute of the class exists. If it does, the function removes the file using the `os.remove()` function.

        Parameters:
            self (DataRepository): The instance of the `DataRepository` class.

        Returns:
            None
        """
        if os.path.exists(self.path):
            os.remove(self.path)

    def update_data(self, data, key):
        """
        Updates the data in the JSON file at the specified path with the given key-value pair.

        Args:
            data (dict): A dictionary containing the key-value pair to be updated.
            key (str): The key to be updated in the JSON file.

        Returns:
            None

        This function checks if the JSON file at the specified path exists. If it does not exist, the function creates an empty dictionary and writes it to the file. If the file exists, the function reads the existing JSON data and updates it with the given key-value pair. If the key already exists in the JSON data, the function appends the value to the existing list. If the key does not exist, the function adds the key-value pair to the JSON data. Finally, the function writes the updated JSON data back to the file.
        """
        if not os.path.exists(self.path):
            data_json = {}
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(data_json, file, ensure_ascii=False, indent=4)
        else:
            try:
                with open(self.path, 'r', encoding='utf-8') as file:
                    data_json = json.load(file)
            except json.JSONDecodeError:
                pass

        if key in data_json:
            data_json[key].extend(data[key])
        else:
            data_json[key] = data[key]

        # Guardar el archivo JSON actualizado
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data_json, file, ensure_ascii=False, indent=4)

    def get_data_id(self, id):
        """
        Retrieves the data associated with the given ID from the JSON file.

        Parameters:
            id (str): The ID of the data to retrieve.

        Returns:
            dict or bool: The data associated with the given ID if it exists, False otherwise.

        Raises:
            Exception: If there is an error while reading the JSON file.
        """
        try:
            if not os.path.exists(self.path):
                return False
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if id in data:
                return data[id]
            else:
                return False
        except Exception as e:
            return e
