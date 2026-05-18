import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="price_comparator",
        user="*****",       
        password="*****", 
        port="5432" #esa es la por defecto de postgreSQL
    )
