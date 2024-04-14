import psycopg2  
from datetime import datetime
import PySimpleGUI as sg
from db_config import get_db_connection  # Get database connection from configuration.

# Connect to the database
conn = get_db_connection()
cur = conn.cursor()

# Log maintenance activities
def log_maintenance_activity(equipment_id, maintenance_date, maintenance_activities, status):
    # Insert new maintenance records into the database
    cur.execute("INSERT INTO equipment_maintenance (equipment_id, maintenance_date, maintenance_activities, status) VALUES (%s, %s, %s, %s)", (equipment_id, maintenance_date, maintenance_activities, status))
    conn.commit()
    return "Maintenance activity logged successfully."

# Schedule future maintenance
def schedule_future_maintenance(equipment_id, future_maintenance_date, planned_activities):
    # Update the database with future maintenance activities
    cur.execute("UPDATE equipment_maintenance SET maintenance_date = %s, maintenance_activities = %s WHERE equipment_id = %s AND status = 'scheduled'", (future_maintenance_date, planned_activities, equipment_id))
    conn.commit()
    return "Future maintenance scheduled successfully."

# View maintenance history
def view_maintenance_history(equipment_id=None):
    # Retrieve and display maintenance history
    if equipment_id:
        cur.execute("SELECT * FROM equipment_maintenance WHERE equipment_id = %s", (equipment_id,))
    else:
        cur.execute("SELECT * FROM equipment_maintenance")
    maintenance_records = cur.fetchall()
    for record in maintenance_records:
        print(record)
    return maintenance_records
