# Trainer_Schedule_Management.py
# Import necessary libraries
import psycopg2  # Changed from sqlite3 to psycopg2
from datetime import datetime
import PySimpleGUI as sg
from db_config import get_db_connection  # Import centralized database connection

# Connect to the database
conn = get_db_connection()  # Use centralized database connection
cur = conn.cursor()

# Function to add availability slot for a trainer
def add_availability(trainer_id, start_time, end_time):
    # Check for conflicts before adding a new slot
    cur.execute("SELECT * FROM trainer_schedule WHERE trainer_id = %s AND (start_time < %s AND end_time > %s) OR (start_time < %s AND end_time > %s)", (trainer_id, end_time, start_time, start_time, end_time))  # Changed ? to %s for PostgreSQL
    conflicts = cur.fetchall()
    if conflicts:
        return "Conflict detected with existing slots."
    else:
        cur.execute("INSERT INTO trainer_schedule (trainer_id, start_time, end_time) VALUES (%s, %s, %s)", (trainer_id, start_time, end_time))  # Changed ? to %s for PostgreSQL
        conn.commit()
        return "Availability slot added successfully."

# Function to update availability slot for a trainer
def update_availability(slot_id, new_start_time, new_end_time):
    # Update availability slot logic
    cur.execute("UPDATE trainer_schedule SET start_time = %s, end_time = %s WHERE slot_id = %s", (new_start_time, new_end_time, slot_id))  # Changed ? to %s for PostgreSQL
    conn.commit()
    return "Availability slot updated successfully."

# Function to delete availability slot for a trainer
def delete_availability(slot_id):
    # Delete availability slot logic
    cur.execute("DELETE FROM trainer_schedule WHERE slot_id = %s", (slot_id,))  # Changed ? to %s for PostgreSQL
    conn.commit()
    return "Availability slot deleted successfully."

# Function to view member profiles for trainers
def view_member_profile(member_name):
    # Logic to view member profiles by name
    cur.execute("SELECT * FROM member_profiles WHERE name = %s", (member_name,))
    member_profile = cur.fetchall()
    if member_profile:
        return member_profile
    else:
        return "No member profile found."

# Main function to run the schedule management interface
def main():
    # GUI layout for schedule management
    layout = [
        [sg.Text('Trainer Schedule Management')],
        [sg.Text('Trainer ID'), sg.InputText()],
        [sg.Text('Start Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Text('End Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Button('Add Availability'), sg.Button('Update Availability'), sg.Button('Delete Availability'), sg.Button('View Member Profile')],
        [sg.Text('Member Name'), sg.InputText()],
        [sg.Output(size=(60,20))]
    ]

    # Create the window
    window = sg.Window('Trainer Schedule Management', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Add Availability':
            result = add_availability(values[0], values[1], values[2])
            print(result)
        elif event == 'Update Availability':
            # Assuming a slot ID input field is added for update/delete operations
            result = update_availability(values[3], values[1], values[2])
            print(result)
        elif event == 'Delete Availability':
            result = delete_availability(values[3])
            print(result)
        elif event == 'View Member Profile':
            profile = view_member_profile(values[4])
            print(profile)

    window.close()

if __name__ == "__main__":
    main()
