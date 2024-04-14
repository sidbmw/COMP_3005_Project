import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname='health_and_fitness_club',
        user='siddharthnatamai',
        password='postgres',
        host='localhost'
    )

def get_setup_db_connection():
    return psycopg2.connect(
        dbname='postgres',  # Connect to the default database for setup
        user='siddharthnatamai',
        password='postgres',
        host='localhost'
    )
