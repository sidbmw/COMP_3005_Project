import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# Import the new get_setup_db_connection function for setup
from db_config import get_setup_db_connection

def setup_database():
    try:
        # Use the get_setup_db_connection function to connect to the default database
        con = get_setup_db_connection()
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Check if the target database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'health_and_fitness_club'")
        exists = cur.fetchone()
        
        # If the database does not exist, create it
        if not exists:
            cur.execute("CREATE DATABASE health_and_fitness_club")
            print("Database 'health_and_fitness_club' created successfully.")
            # After creating the database, execute DDL statements
            ddl_file_path = 'health_and_fitness_club_ddl.sql'
            with open(ddl_file_path, 'r') as file:
                ddl_statements = file.read()
            # Connect to the newly created database to execute DDL statements
            con = psycopg2.connect(
                dbname='health_and_fitness_club',
                user='siddharthnatamai', 
                password='postgres',  
                host='localhost'
            )
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute(ddl_statements)
            con.commit()
            print("DDL statements executed successfully.")
            cur.close()
            con.close()
        else:
            print("Database 'health_and_fitness_club' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if 'cur' in locals():
            cur.close()
        if 'con' in locals() and con.closed == 0:
            con.close()

# Call the setup_database function to ensure the database is set up
setup_database()