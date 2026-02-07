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
data_crypto = [
        ['ETH', 'https://coin360.com/coin/ethereum-eth'],
        ['SOL', 'https://coin360.com/coin/solana-sol']
    ]

    # Convert the data into a pandas DataFrame
df = pd.DataFrame(data_crypto, columns=['item_name', 'url'])

    # Display the DataFrame
print(df)

response = requests.get('https://coinmarketcap.com/currencies/ethereum/')
#print(response.content)

#soup = BeautifulSoup(response.content, 'html.parser')

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())

# Find the element with class or attribute value "bEBnIS"
element = soup.find("2695")

# Print the element if found
if element:
    print(element)
else:
    print("Element with class or attribute value 'bEBnIS' not found.")