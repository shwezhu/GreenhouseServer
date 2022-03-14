import utils


class DatabaseUtils:
    def __init__(self, db):
        self._db = db

    def query(self, sql, params=None):
        results = self._db.query(sql, params)
        row_header = [d[0] for d in self._db.cursor.description]
        return utils.Utils.query_to_json(results, row_header)

    def execute(self, sql, params=None):
        self._db.execute(sql, params)
        self._db.commit()
