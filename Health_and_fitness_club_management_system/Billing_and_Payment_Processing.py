import psycopg2
from datetime import datetime
import PySimpleGUI as sg
from db_config import get_db_connection  # Get database connection from configuration.

# Establish database connection.
conn = get_db_connection()
cur = conn.cursor()

# Generate bills for club members.
def generate_bill(member_id):
    print(f"Generating bill for member ID: {member_id}")
    # Retrieve services used by the member.
    cur.execute("SELECT service, cost FROM services_used WHERE member_id = %s", (member_id,))
    services = cur.fetchall()
    # Sum up the total cost.
    bill_amount = sum(cost for service, cost in services)
    return bill_amount

# Handle payment processing.
def process_payment(member_id, amount):
    print(f"Processing payment of ${amount} for member ID: {member_id}")
    # Update payment status in the database.
    cur.execute("UPDATE payments SET status = 'Processed' WHERE member_id = %s", (member_id,))
    conn.commit()
    payment_status = "Processed"
    return payment_status

# Setup the GUI layout.
layout = [
    [sg.Text('Billing and Payment Processing')],
    [sg.Text('Member ID'), sg.InputText()],
    [sg.Text('Amount'), sg.InputText()],
    [sg.Button('Generate Bill'), sg.Button('Process Payment')],
    [sg.Output(size=(60,20))]
]

# Initialize the window.
window = sg.Window('Billing and Payment Processing', layout)

# Handle window events.
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Generate Bill':
        bill_amount = generate_bill(values[0])
        print(f"Bill generated. Total amount due: ${bill_amount}")
    elif event == 'Process Payment':
        payment_status = process_payment(values[0], values[1])
        print(f"Payment status: {payment_status}")

window.close()
