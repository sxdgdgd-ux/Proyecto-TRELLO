from peewee import MySQLDatabase, Model

# Una única conexión compartida para todas las tablas
database = MySQLDatabase(
    'trello_db',
    host='localhost',
    port=8080,
    user='Ale',
    password='ale',
    charset='utf8mb4'
)

class BaseModel(Model):
    class Meta:
        database = database