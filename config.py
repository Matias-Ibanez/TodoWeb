import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__)) #Obtenemos el path absoluto en donde nos encontramos
print(basedir)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or 'you-will-never-guess'
    instance_path = os.path.join(basedir, 'instance')
    db_path = os.path.join(instance_path, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{db_path}"
    TASKS_PER_PAGE = 4

