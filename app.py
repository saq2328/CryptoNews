import pandas as pd
import requests
import spacy
import streamlit as st
from bs4 import BeautifulSoup
import yfinance as yf

st.title('Buzzing Stocks :zap:')


# create a sample stocks dataframe
#pd.options.display.max_rows = 9999
stocks_df = pd.read_csv("./data/ind_nifty500list.csv")

companies = []

resp = requests.get("https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms")

soup = BeautifulSoup(resp.content, features="xml")
headlines = soup.find_all('title')

nlp = spacy.load("en_core_web_sm")


processed_hline = nlp(headlines[4].text)
for token in processed_hline:
  print(token.text, "-----", token.dep_)

if processed_hline.ents:
    for ent in processed_hline.ents:
        print(ent.text, ent.label_)
else:
    print("No named entities found in the input text.")
#spacy.displacy.render(processed_hline, style='ent', jupyter=True, options={'distance': 120})


# Loop over the headlines and extract named entities of type 'ORG'
for title in headlines:
    doc = nlp(title.text)
    if doc.ents:
        for token in doc.ents:
            if token.label_ == 'ORG':
                companies.append(token.text)

# Print the extracted company names
if companies:
    pass    
else:
    print("No companies were mentioned in the headlines.")





# Create an empty list to store the stock information
stock_dict = {
    'Org': [],
    'Symbol': [],
    'currentPrice': [],
    'dayHigh': [],
    'dayLow': [],
    'forwardPE': [],
    'dividendRate': []
}

# For each company in the list, look up the stock information and add it to the dictionary
for company in companies:
    try:
        # Check if the company name contains the specified string
        if stocks_df['Company Name'].str.contains(company).sum():
            # Get the symbol and organization name for the company
            symbol = stocks_df[stocks_df['Company Name'].str.contains(company)]['Symbol'].values[0]
            org_name = stocks_df[stocks_df['Company Name'].str.contains(company)]['Company Name'].values[0]
            # Look up the stock information using the Yahoo Finance API
            stock_info = yf.Ticker(symbol+".NS").info
            
            # Add the stock information to the dictionary
            stock_dict['Org'].append(org_name)
            stock_dict['Symbol'].append(symbol)
            stock_dict['currentPrice'].append(stock_info.get('regularMarketPrice', None))
            stock_dict['dayHigh'].append(stock_info.get('dayHigh', None))
            stock_dict['dayLow'].append(stock_info.get('dayLow', None))
            stock_dict['forwardPE'].append(stock_info.get('forwardPE', None))
            stock_dict['dividendRate'].append(stock_info.get('dividendRate', None))
        else:
            pass
    except:
        pass

# Convert the dictionary to a pandas dataframe
stock = pd.DataFrame(stock_dict)
#stocks = stock.drop_duplicates(stock_dict)
# Round the floating-point values to 2 decimal places
stock

## add an input field to pass the RSS link
user_input = st.text_input("Add your RSS link here!", "https://www.moneycontrol.com/rss/buzzingstocks.xml")

