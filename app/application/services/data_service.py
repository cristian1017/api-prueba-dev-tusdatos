from app.infraestructura.repositories.data_repository import DataRepository
from app.utils.utils import Utils


class DataService:
    def __init__(self):
        self.data_repository = DataRepository()

    def get_info_data(self):
        data = self.data_repository.get_data()
        return data

    def get_data_id(self, id):
        """
        Retrieves data associated with a given ID from the data repository and returns it in a JSON response.

        :param id: The ID of the data to retrieve.
        :type id: str

        :return: A JSON response containing the data associated with the given ID, including the ID itself, the total number of data items, and either the entire data list or separate lists for demandados and demandantes, along with the counts of each. If the ID is not found, a JSON response with a message and a status code of 404 is returned.
        """
        data = self.data_repository.get_data_id(id)
        if not data:
            return {"msg": "ID not found"}, 404

        counts = Utils.count_demandante_demandado(data)

        any_zero = any(value == 0 for value in counts.values())
        resp = {
            'id': id,
            'total': len(data),
        }
        if any_zero:
            resp['data'] = data
        else:
            resp['data_demandados'] = [
                item for item in data if item['type'] == 'demandado']
            resp['data_demandantes'] = [
                item for item in data if item['type'] == 'demandante']
            resp['count_demandados'] = counts['count_demandado']
            resp['count_demandante'] = counts['count_demandante']

        return resp
