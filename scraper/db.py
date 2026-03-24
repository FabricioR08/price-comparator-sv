import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="price_comparator",
        user="postgres",        # cámbialo por tu usuario
        password="postgres", # cámbialo por tu password
        port="5432"
    )