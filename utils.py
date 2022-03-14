import json


class Utils:
    @staticmethod
    def query_to_json(results, row_header):
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_header, result)))
        json.dumps(json_data, indent=4, sort_keys=True, default=str)
        return json_data
