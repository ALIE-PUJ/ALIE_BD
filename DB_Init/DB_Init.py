import psycopg2
import os

def execute_sql_from_file(file_path, conn):

    print(f"Ejecutando script SQL: {file_path}")

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
    userDB = os.getenv('COCKROACHDB_USER', 'root')

    # Busca la variable de entorno PASS; si no existe, asigna una cadena vacía
    passw = os.getenv('COCKROACHDB_PASS', 'pass')

    # Busca la variable de entorno HOST; si no existe, asigna postgres
    cdb_host = os.getenv('COCKROACHDB_HOST', 'postgres')

    # Busca el puerto en la variable de entorno
    cdb_port = os.getenv('COCKROACHDB_PORT', 5432)


    connection = psycopg2.connect(
        host=cdb_host, # docker-compose service name. Use localhost to run locally
        port=cdb_port,
        user=userDB,
        password=passw,
        database='alie_db' # lowercase
    )

    execute_sql_from_file('Create_Tables/Init.sql', connection)
    execute_sql_from_file('Insert_Scripts/Inserts.sql', connection)

    # Scripts de la API
    execute_sql_from_file('Create_Tables/API_Init.sql', connection)
    execute_sql_from_file('Insert_Scripts/API_Inserts.sql', connection)

    print("Available tables: ")
    query_all_tables(connection)


    connection.close()

if __name__ == '__main__':
    main()
