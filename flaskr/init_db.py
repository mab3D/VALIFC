import os
import psycopg2

# https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application
# In linux use environment variables, cannot be used in windows
#    export DB_USERNAME="postgres"
#    export DB_PASSWORD="password"




conn = psycopg2.connect(
        host="localhost",
        port=5433,
        database="postgres",
        user="postgres",
        password="1nd8er5er")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS meta;')
cur.execute('CREATE TABLE meta (id serial PRIMARY KEY,'
                                 'filename varchar (150) NOT NULL,'
                                 'state integer NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO meta (filename, state)'
            'VALUES (%s, %s)',
            ('Init',
             1)
            )


#cur.execute('INSERT INTO books (title, author, pages_num, review)'
#            'VALUES (%s, %s, %s, %s)',
#            ('Anna Karenina',
#             'Leo Tolstoy',
#             864,
#             'Another great classic!')
#            )

conn.commit()

cur.close()
conn.close()
