# Trainer_Schedule_Management.py
# Import necessary libraries
import sqlite3
from datetime import datetime
import PySimpleGUI as sg

# Connect to the database
conn = sqlite3.connect('health_and_fitness_club.db')
cur = conn.cursor()

# Function to add availability slot for a trainer
def add_availability(trainer_id, start_time, end_time):
    # Check for conflicts before adding a new slot
    cur.execute("SELECT * FROM trainer_schedule WHERE trainer_id = ? AND (start_time < ? AND end_time > ?) OR (start_time < ? AND end_time > ?)", (trainer_id, end_time, start_time, start_time, end_time))
    conflicts = cur.fetchall()
    if conflicts:
        return "Conflict detected with existing slots."
    else:
        cur.execute("INSERT INTO trainer_schedule (trainer_id, start_time, end_time) VALUES (?, ?, ?)", (trainer_id, start_time, end_time))
        conn.commit()
        return "Availability slot added successfully."

# Function to update availability slot for a trainer
def update_availability(slot_id, new_start_time, new_end_time):
    # Update availability slot logic
    cur.execute("UPDATE trainer_schedule SET start_time = ?, end_time = ? WHERE slot_id = ?", (new_start_time, new_end_time, slot_id))
    conn.commit()
    return "Availability slot updated successfully."

# Function to delete availability slot for a trainer
def delete_availability(slot_id):
    # Delete availability slot logic
    cur.execute("DELETE FROM trainer_schedule WHERE slot_id = ?", (slot_id,))
    conn.commit()
    return "Availability slot deleted successfully."

# Main function to run the schedule management interface
def main():
    # GUI layout for schedule management
    layout = [
        [sg.Text('Trainer Schedule Management')],
        [sg.Text('Trainer ID'), sg.InputText()],
        [sg.Text('Start Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Text('End Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Button('Add Availability'), sg.Button('Update Availability'), sg.Button('Delete Availability')],
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

    window.close()

if __name__ == "__main__":
    main()

