import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# Use db_config for database connection settings
from db_config import get_setup_db_connection

def setup_database():
    try:
        # Connect to the default database using settings from db_config
        con = get_setup_db_connection()
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Check if the target database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'health_and_fitness_club'")
        exists = cur.fetchone()
        
        # Create the database if it does not exist
        if not exists:
            cur.execute("CREATE DATABASE health_and_fitness_club")
            print("Database 'health_and_fitness_club' created successfully.")
            # Execute DDL statements to set up the database schema
            ddl_file_path = 'health_and_fitness_club_ddl.sql'
            with open(ddl_file_path, 'r') as file:
                ddl_statements = file.read()
            con = get_setup_db_connection(dbname='health_and_fitness_club')
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute(ddl_statements)
            con.commit()
            print("DDL statements executed successfully.")
            # Populate the database with initial data
            dml_file_path = 'health_and_fitness_club_dml.sql'
            with open(dml_file_path, 'r') as file:
                dml_statements = file.read()
            cur.execute(dml_statements)
            con.commit()
            print("DML statements executed successfully.")
            cur.close()
            con.close()
        else:
            print("Database 'health_and_fitness_club' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the database connection is closed
        if 'cur' in locals():
            cur.close()
        if 'con' in locals() and con.closed == 0:
            con.close()

# Run the setup_database function to set up the database
setup_database()