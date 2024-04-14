# Billing_and_Payment_Processing.py
# Import necessary libraries
import psycopg2
from datetime import datetime
import PySimpleGUI as sg
from db_config import get_db_connection  # Import centralized database connection

# Connect to the database
conn = get_db_connection()  # Use centralized database connection
cur = conn.cursor()

# Function to generate bills for members
def generate_bill(member_id):
    # Enhanced logic for bill generation
    # This now involves querying the database for services used by the member and calculating the total amount due
    print(f"Generating bill for member ID: {member_id}")
    # Query the database for services used
    cur.execute("SELECT service, cost FROM services_used WHERE member_id = %s", (member_id,))
    services = cur.fetchall()
    bill_amount = sum(cost for service, cost in services)  # Calculate total amount due
    return bill_amount

# Function to process payments
def process_payment(member_id, amount):
    # Enhanced logic for payment processing
    # This simulates integrating with a payment service and updates the payment status in the database
    print(f"Processing payment of ${amount} for member ID: {member_id}")
    # Simulate payment processing by updating the database
    cur.execute("UPDATE payments SET status = 'Processed' WHERE member_id = %s", (member_id,))
    conn.commit()
    payment_status = "Processed"
    return payment_status

# GUI layout for billing and payment processing
layout = [
    [sg.Text('Billing and Payment Processing')],
    [sg.Text('Member ID'), sg.InputText()],
    [sg.Text('Amount'), sg.InputText()],
    [sg.Button('Generate Bill'), sg.Button('Process Payment')],
    [sg.Output(size=(60,20))]
]

# Create the window
window = sg.Window('Billing and Payment Processing', layout)

# Event loop
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
