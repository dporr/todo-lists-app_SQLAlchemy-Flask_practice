import psycopg2

try:
    connection = psycopg2.connect('host=localhost dbname=example user={secret} password={secret}')
    print(connection)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE table1(
            id INTEGER PRIMARY KEY,
            completed BOOLEAN DEFAULT False
        );
    ''')
    cursor.execute('''
        INSERT INTO table1 (id, completed) VALUES (4, True);
    ''')
    cursor.execute('''
        INSERT INTO table1 (id) VALUES (5);
    ''')

    SQL = 'INSERT INTO table1 (id, completed) VALUES (%(id)s, %(completed)s);'

    data = {
    'id': 10
    'completed': True
    }
    result = cursor.execute(SQL, data)
    connection.commit()
    print(result)
except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()