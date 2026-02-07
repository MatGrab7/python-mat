import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox
output_file='C:/Users/refll/OneDrive/Pulpit/codeprices.csv'

    # Create a new table with the specified values
data = [
        ['drzwi_szafy', 'https://www.agatameble.pl/akcesoria-meblowe/fronty-meblowe/front-pelny-ben-dab-artisan'],
        ['regal_ben_pokoj_celi', 'https://www.agatameble.pl/meble/przechowywanie/regaly/regal-zamkniety-ben-dab-artisan']
    ]

    # Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=['item_name', 'url'])

    # Display the DataFrame
print(df)

# Function to get the price from a given URL
def get_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    parent = soup.find("div", class_=["m-priceBox_price", "m-priceBox_promo"])
    if parent:
        price_text = parent.get_text(strip=True)
        price_match = re.search(r'\d+', price_text)
        if price_match:
            return int(price_match.group())
    return None

# Add a new column for prices
df['price'] = df['url'].apply(get_price)

# Add a new column for the datetime of execution
# Add a new column for the datetime of execution


# Add a new column for the date of execution
df['execution_date'] = datetime.now().strftime('%Y-%m-%d')

# Initialize the is_change variable
is_change = False

# Read the existing data from the CSV file if it exists
try:
    existing_df = pd.read_csv(output_file)
    if 'item_name' not in existing_df.columns or 'price' not in existing_df.columns:
        existing_df = pd.DataFrame(columns=['item_name', 'price', 'execution_date'])
except FileNotFoundError:
    existing_df = pd.DataFrame(columns=['item_name', 'price', 'execution_date'])

# Check if the price has changed compared to the previous date
if not existing_df.empty:
    for index, row in df.iterrows():
        previous_entry = existing_df[(existing_df['item_name'] == row['item_name']) & 
                                     (existing_df['execution_date'] == (datetime.now() - pd.Timedelta(days=1)).strftime('%Y-%m-%d'))]
        if not previous_entry.empty and previous_entry['price'].values[0] != row['price']:
            is_change = True
            break
print("czy zmiana: ", is_change)
email_message = "brak zmian cen od wczoraj dla" +  "\n\n" + str(data)


if is_change:
    email_message = "Price changes detected:\n\n"
    for index, row in df.iterrows():
        previous_entry = existing_df[(existing_df['item_name'] == row['item_name']) & 
                                     (existing_df['execution_date'] == (datetime.now() - pd.Timedelta(days=1)).strftime('%Y-%m-%d'))]
        if not previous_entry.empty and previous_entry['price'].values[0] != row['price']:
            previous_price = previous_entry['price'].values[0]
            current_price = row['price']
            price_change = current_price - previous_price
            price_change_percentage = (price_change / previous_price) * 100
            email_message += (f"Item: {row['item_name']}\n"
                              f"Previous Price: {previous_price}\n"
                              f"Current Price: {current_price}\n"
                              f"Price Change: {price_change} ({price_change_percentage:.2f}%)\n\n")

print(email_message)
# Append the new data to the existing data without the header row
df.to_csv(output_file, mode='a', header=False, index=False)

#sending mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = "mateusgrabowski@gmail.com"
    from_password = "rrxp uppg ljgl gmjy"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the Gmail server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)

    # Send the email
    server.send_message(msg)
    server.quit()

# Example usage
send_email("daily monitoring", email_message,"refllecto@gmail.com")