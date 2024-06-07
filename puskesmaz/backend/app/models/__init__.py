from .users import create_users_table
from .medicine import create_medicine_table

def create_db_tables():
    create_users_table()
    create_medicine_table()
