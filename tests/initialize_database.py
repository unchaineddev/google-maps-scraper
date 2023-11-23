import psycopg2


def postgres_db(query, values):
    """establishing DATABASE CONNECTION"""
    try:
        conn = psycopg2.connect(database="google",
                                user='postgres',
                                password='123456789',
                                host='localhost',
                                port='5432'
                                )
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        # print(data)
        # return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        with open("dblog.txt", "a") as er:
            er.write(str(error))
