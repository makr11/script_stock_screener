import time
import requests
import sqlite3
from settings import API_URL, FUNCTION, STOCK_QUOTES_TABLE
import av_db
from quote import Quote


def sleep_time():
    """generator for script pause between api calls"""

    t = time.time()
    count = 0
    while True:
        count += 1
        yield max(t + count*15 - time.time(), 0)


def get_api_data(quote, date_range):
    """request to API with error check
    Error message if any of query params are invaild
    Note if API call limit is reached"""
    print(API_URL.format(date_range, quote))
    data = requests.get(API_URL.format(date_range, quote)).json()

    if "Error Message" in data:
        raise ValueError(data["Error Message"])
    elif "Information" in data:
        raise ValueError(data["Information"])
    elif "Note" in data:
        print(data["Note"])
        return False
    for i in data:
        if "Time Series" in i:
            return data[i]


def run_script(quotes, date_range):
    """runs script for selected date range
    (intraday, daily, weekly, monthly)"""

    # check if database is empty
    if len(quotes) == 0:
        print("Database empty! Add stock quotes with 'create-tables <quote>'")
        return None

    api_function = FUNCTION[date_range]
    sleep = sleep_time()
    store_end_exception = None

    while True:
        try:
            # terminate script with ctrl+c
            if store_end_exception:
                break

            for quote in quotes:
                print("quote: ", quote)
                print("api called: ", time.ctime())
                data = get_api_data(quote[1], api_function)
                if data:
                    tb_name = date_range
                    av_db.save_data_to_db(quote[0], data, tb_name, date_range)
                print("api call pause started: ", time.ctime())
                time.sleep(next(sleep))

        except KeyboardInterrupt:
            store_end_exception = True


def add_quote(quote_list, quotes):
    api_function = FUNCTION["daily"]

    for quote in quote_list:
        if quote not in quotes:
            try:
                # Check if quote is available in API or already in database
                data = get_api_data(quote, api_function)
                quote = quote.upper()
                # insert quote in quotes table
                av_db.insert("quotes", STOCK_QUOTES_TABLE, data=[(quote,)])
                quote_id = av_db.query("quotes", "*", condition=f"quote='{quote}'")[0][0]
                print(f"{quote}, is added to database")
                tb_name="daily"
                date_range="daily"
                av_db.save_data_to_db(quote_id, data, tb_name, date_range)
                return True
            except ValueError as error:
                print("Quote: " + quote, error)
                return False
        else:
            print(f"{quote} is already in database")
            

def search_quote(stock):
    stock = stock.lower()
    search = requests.get(API_SEARCH.format(stock.split(" ")[0])).json()

    matches = []
    if len(search["bestMatches"])==0:
        return None
    else:
        for stock_data in search["bestMatches"]:
            name = stock_data["2. name"].lower()
            if stock in name:
                matches.append(stock_data) 
        matches.append(search["bestMatches"][0])
    return matches
