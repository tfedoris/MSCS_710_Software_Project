from sqlalchemy import create_engine


class MYSQLConnector:
    def __init__(self, db_settings):
        self.type = db_settings["type"]
        self.user = db_settings["user"]
        self.host = db_settings["host"]
        self.db_name = db_settings["db_name"]

    def get_engine(self):
        db_uri = "{}://{}@{}/{}".format(self.type, self.user, self.host, self.db_name)
        db_engine = create_engine(db_uri)
        return db_engine
