import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(60) NOT NULL,
        last_name VARCHAR(60),
        email VARCHAR(250) UNIQUE
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS phone_number(
        id_pnumber SERIAL PRIMARY KEY,
        client_phone_number VARCHAR(60),
        id_client INTEGER REFERENCES clients(id)           
        );
        ''')


def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO clients(name, last_name, email) VALUES(%s, %s, %s);
        ''', (first_name, last_name, email))


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO phone_number(client_phone_number, id_client) VALUES(%s, %s)
        ''', (phone, client_id))


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute('''
                        UPDATE clients
                        SET name = %s 
                        WHERE id = %s;
                        ''', (first_name, client_id,))
        if last_name:
            cur.execute('''
                        UPDATE clients
                        SET last_name = %s
                        WHERE id = %s;
                        ''', (last_name, client_id,))
        if email:
            cur.execute('''
                        UPDATE clients
                        email = %s
                        WHERE id = %s;
                        ''', (email, client_id,))


def delete_phone(conn, pnumber_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM phone_number
        WHERE id_pnumber = %s;
        ''', (pnumber_id,))


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE from clients
        WHERE id = %s;
        ''', (client_id,))


def find_client(conn, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM clients
        WHERE name = %s OR  last_name = %s OR email = %s;
        ''', (first_name, last_name, email))
        return print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="rusarm77") as conn:
        create_db(conn)
        add_client(conn, 'Vladimir', 'Saakyan', 'saakya2001@gmail.com')
        add_phone(conn, 1, '7-909-66-55')
        change_client(conn, 1, last_name='kosoyan')
        delete_phone(conn, 2)
        delete_client(conn, 2)
        find_client(conn, email='saakyan2001@gmail.com')

conn.close()
