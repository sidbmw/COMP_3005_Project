import psycopg2  
from datetime import datetime
import PySimpleGUI as sg
from db_config import get_db_connection  

# Connect to the database
conn = get_db_connection()
cur = conn.cursor()

# Add a room booking
def add_booking(room_id, start_time, end_time):
    # Check for booking conflicts
    cur.execute("SELECT * FROM room_bookings WHERE room_id = %s AND NOT (end_time <= %s OR start_time >= %s)", (room_id, start_time, end_time))
    conflicts = cur.fetchall()
    if conflicts:
        return "Booking conflict detected."
    else:
        # Insert booking into database
        cur.execute("INSERT INTO room_bookings (room_id, start_time, end_time) VALUES (%s, %s, %s)", (room_id, start_time, end_time))
        conn.commit()
        return "Booking added successfully."

# Update a room booking
def update_booking(booking_id, new_start_time, new_end_time):
    # Check for update conflicts
    cur.execute("SELECT * FROM room_bookings WHERE booking_id != %s AND room_id = (SELECT room_id FROM room_bookings WHERE booking_id = %s) AND NOT (end_time <= %s OR start_time >= %s)", (booking_id, booking_id, new_end_time, new_start_time))
    conflicts = cur.fetchall()
    if conflicts:
        return "Update conflict detected."
    else:
        # Update booking in database
        cur.execute("UPDATE room_bookings SET start_time = %s, end_time = %s WHERE booking_id = %s", (new_start_time, new_end_time, booking_id))
        conn.commit()
        return "Booking updated successfully."

# View bookings
def view_bookings(room_id=None):
    # Retrieve bookings based on room ID or all bookings
    if room_id:
        cur.execute("SELECT * FROM room_bookings WHERE room_id = %s", (room_id,))
    else:
        cur.execute("SELECT * FROM room_bookings")
    bookings = cur.fetchall()
    return bookings

# Main function for room booking management
def main():
    # Set up GUI layout
    layout = [
        [sg.Text('Room Booking Management')],
        [sg.Text('Room ID'), sg.InputText()],
        [sg.Text('Booking ID (for updates)'), sg.InputText()],
        [sg.Text('Start Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Text('End Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Button('Add Booking'), sg.Button('Update Booking'), sg.Button('View Bookings')],
        [sg.Output(size=(60,20))]
    ]
    
    # Create window
    window = sg.Window('Room Booking Management', layout)
    
    # Event loop for window actions
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Add Booking':
            # Handle 'Add Booking' action
            result = add_booking(values[0], values[2], values[3])
            print(result)
        elif event == 'Update Booking':
            # Handle 'Update Booking' action
            result = update_booking(values[1], values[2], values[3])
            print(result)
        elif event == 'View Bookings':
            # Handle 'View Bookings' action
            if values[0]:  # If Room ID is provided
                bookings = view_bookings(values[0])
            else:  # View all bookings
                bookings = view_bookings()
            for booking in bookings:
                print(booking)
    
    window.close()
