import json


class DatabaseUtils:
    def __init__(self, db):
        self._db = db

    def query(self, sql, params=None):
        raw_results = self._db.query(sql, params)
        row_header = [d[0] for d in self._db.cursor.description]
        data = []
        for r in raw_results:
            data.append(dict(zip(row_header, r)))
        json.dumps(data, indent=4, sort_keys=True, default=str)
        results = json.dumps({'results': data})
        return results

    def execute(self, sql, params=None):
        self._db.execute(sql, params)
        self._db.commit()
