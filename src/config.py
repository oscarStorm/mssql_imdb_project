# import os gives acces to .env variables
import os
# import the load_dotenv function from the dotenv package (which loads the .env)
from dotenv import load_dotenv
#loads the .env 
load_dotenv()
#database config
DB = {
    "server": os.getenv("DB_SERVER"),
    "port": os.getenv("DB_PORT"),
    "name": os.getenv("DB_NAME"),
    "driver": os.getenv("DB_DRIVER"),
}
#super admin config
SA = {
    "user": os.getenv("SA_USER"),
    "password": os.getenv("SA_PASSWORD"),
}
#admin config
ADMIN = {
    "user": os.getenv("ADMIN_USER"),
    "password": os.getenv("ADMIN_PASSWORD"),
}
#user config
APP = {
    "user": os.getenv("APP_USER"),
    "password": os.getenv("APP_PASSWORD"),
}
