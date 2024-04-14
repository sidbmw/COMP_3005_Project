import psycopg2 
from datetime import datetime
import PySimpleGUI as sg
from db_config import get_db_connection  

# Connect to the database
conn = get_db_connection()  
cur = conn.cursor()

# Add availability slot
def add_availability(trainer_id, start_time, end_time):
    # Check for conflicts
    cur.execute("SELECT * FROM trainer_schedule WHERE trainer_id = %s AND (start_time < %s AND end_time > %s) OR (start_time < %s AND end_time > %s)", (trainer_id, end_time, start_time, start_time, end_time))  
    conflicts = cur.fetchall()
    if conflicts:
        return "Conflict detected with existing slots."
    else:
        cur.execute("INSERT INTO trainer_schedule (trainer_id, start_time, end_time) VALUES (%s, %s, %s)", (trainer_id, start_time, end_time))  
        conn.commit()
        return "Availability slot added successfully."

# Update availability slot
def update_availability(slot_id, new_start_time, new_end_time):
    # Update slot
    cur.execute("UPDATE trainer_schedule SET start_time = %s, end_time = %s WHERE slot_id = %s", (new_start_time, new_end_time, slot_id))  
    conn.commit()
    return "Availability slot updated successfully."

# Delete availability slot
def delete_availability(slot_id):
    # Delete slot
    cur.execute("DELETE FROM trainer_schedule WHERE slot_id = %s", (slot_id,))  
    conn.commit()
    return "Availability slot deleted successfully."

# View member profiles
def view_member_profile(member_name):
    # View profiles by name
    cur.execute("SELECT * FROM member_profiles WHERE name = %s", (member_name,))
    member_profile = cur.fetchall()
    if member_profile:
        return member_profile
    else:
        return "No member profile found."

# Schedule sessions
def schedule_session(member_id, session_type, trainer_id=None, class_id=None, start_time=None, end_time=None):
    # Validate parameters
    if trainer_id is None or start_time is None or end_time is None:
        print("Invalid parameters: trainer_id, start_time, and end_time cannot be None.")
        return "Invalid parameters: trainer_id, start_time, and end_time cannot be None."
    print(f"Attempting to register session. Type: {session_type}, Member ID: {member_id}, Trainer ID: {trainer_id}, Class ID: {class_id}, Start Time: {start_time}, End Time: {end_time}")
    if session_type == "personal_training":
        print("Checking trainer availability for personal training session.")
        sql_query = "SELECT * FROM trainer_schedule WHERE trainer_id = %s AND (start_time <= %s AND end_time >= %s)"
        sql_params = (trainer_id, start_time, end_time)
        print(f"Executing SQL for session registration: {sql_query} with params {sql_params}")
        try:
            cur.execute(sql_query, sql_params)
            availability = cur.fetchone()
            if availability:
                print("Trainer is not available at the selected time.")
                return "Trainer is not available at the selected time."
            else:
                cur.execute("INSERT INTO schedule (member_id, trainer_id, start_time, end_time) VALUES (%s, %s, %s, %s)", (member_id, trainer_id, start_time, end_time))
                conn.commit()
                print("Session registration successful.")
                sg.Popup("Personal training session scheduled successfully.", title="Success")
                return "Personal training session scheduled successfully."
        except Exception as e:
            print(f"Error during session registration: {e}")
            conn.rollback()
    elif session_type == "group_fitness":
        print("Checking class availability for group fitness session.")
        sql_query = "SELECT count(*) FROM class_registrations WHERE class_id = %s"
        sql_params = (class_id,)
        print(f"Executing SQL for session registration: {sql_query} with params {sql_params}")
        try:
            cur.execute(sql_query, sql_params)
            registrations = cur.fetchone()[0]
            cur.execute("SELECT capacity FROM class_schedule WHERE class_id = %s", (class_id,))
            capacity = cur.fetchone()[0]
            if registrations >= capacity:
                print("Class is fully booked.")
                return "Class is fully booked."
            else:
                cur.execute("INSERT INTO class_registrations (member_id, class_id) VALUES (%s, %s)", (member_id, class_id))
                conn.commit()
                print("Session registration successful.")
                sg.Popup("Registered for group fitness class successfully.", title="Success")
                return "Registered for group fitness class successfully."
        except Exception as e:
            print(f"Error during session registration: {e}")
            conn.rollback()

# View scheduled sessions
def view_scheduled_sessions(member_id):
    print(f"Attempting to retrieve scheduled sessions for Member ID={member_id}")
    # Retrieve sessions
    cur.execute("SELECT start_time, end_time, t.name FROM schedule JOIN trainers t ON schedule.trainer_id = t.trainer_id WHERE schedule.member_id = %s", (member_id,))
    personal_training_sessions = cur.fetchall()
    
    cur.execute("SELECT c.class_id, c.name, c.start_time, c.end_time FROM class_registrations r JOIN class_schedule c ON r.class_id = c.class_id WHERE r.member_id = %s", (member_id,))
    group_fitness_classes = cur.fetchall()
    
    # Format session information
    sessions = []
    for session in personal_training_sessions:
        sessions.append({"type": "Personal Training", "trainer": session[2], "start_time": session[0], "end_time": session[1]})
    for class_ in group_fitness_classes:
        sessions.append({"type": "Group Fitness Class", "class_id": class_[0], "name": class_[1], "start_time": class_[2], "end_time": class_[3]})
    
    if sessions:
        return sessions
    else:
        return "You have no scheduled sessions."

# Main function
def main():
    # GUI layout
    layout = [
        [sg.Text('Trainer Schedule Management')],
        [sg.Text('Trainer ID'), sg.InputText()],
        [sg.Text('Start Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Text('End Time (YYYY-MM-DD HH:MM)'), sg.InputText()],
        [sg.Button('Add Availability'), sg.Button('Update Availability'), sg.Button('Delete Availability'), sg.Button('View Member Profile')],
        [sg.Text('Member Name'), sg.InputText()],
        [sg.Output(size=(60,20))]
    ]

    # Create window
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
