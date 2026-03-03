import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="analytics",
        user="postgres",
        password="786687",
        host="localhost",
        port="5432"
    )