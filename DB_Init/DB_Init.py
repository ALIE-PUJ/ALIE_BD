import psycopg2
import os

def execute_sql_from_file(file_path, conn):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql = file.read()
    
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()

def get_all_tables(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
        """)
        tables = cursor.fetchall()
    return [table[0] for table in tables]

def query_all_tables(conn):
    tables = get_all_tables(conn)
    with conn.cursor() as cursor:
        for table in tables:
            print(f"Table: {table}")
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print("\n")

def main():

    # Busca la variable de entorno USER; si no existe, asigna "root"
    userDB = os.getenv('USER', 'root')

    # Busca la variable de entorno PASS; si no existe, asigna una cadena vacía
    passw = os.getenv('PASS', '')

    connection = psycopg2.connect(
        host='cockroachdb', # docker-compose service name
        port=26257,
        user=userDB,
        password=passw,
        database='ALIE_DB'
    )

    execute_sql_from_file('Create_Tables/Init.sql', connection)
    execute_sql_from_file('Insert_Scripts/Inserts.sql', connection)

    print("Available tables: ")
    query_all_tables(connection)


    connection.close()

if __name__ == '__main__':
    main()
