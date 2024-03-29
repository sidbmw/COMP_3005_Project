import psycopg2
import PySimpleGUI as sg

def main():
    # Attempt to connect to the database
    try:
        con = psycopg2.connect(
            dbname='your_dbname',
            user='your_username',
            password='your_password',
            host='localhost'
        )
        print("Connected to the database successfully")
    except psycopg2.DatabaseError as e:
        sg.Popup("Database Connection Error", f"An error occurred while connecting to the database: {e}")
        return

    # Initial user interface layout
    layout = [
        [sg.Text('Welcome to the Health and Fitness Club Management System', size=(30, 2), justification='center', font=("Helvetica", 16))],
        [sg.Button('Login'), sg.Button('Register'), sg.Button('Exit')]
    ]
    
    window = sg.Window('Main Menu', layout)
    
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Login':
            # Placeholder for login functionality
            sg.Popup("Login", "Login functionality not yet implemented.")
        elif event == 'Register':
            # Placeholder for registration functionality
            sg.Popup("Register", "Registration functionality not yet implemented.")
    
    window.close()

if __name__ == "__main__":
    main()
