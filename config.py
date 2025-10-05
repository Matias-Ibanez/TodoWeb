import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__)) #Obtenemos el path absoluto en donde nos encontramos
print(basedir)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    TASKS_PER_PAGE = 4

