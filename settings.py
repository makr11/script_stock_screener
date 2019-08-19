import os

# api defaults
ADRESS = "https://www.alphavantage.co/query?"
API_KEY = "KOSKZLNCLMKK88OT"
API_URL = ADRESS + "&function={}&symbol={}&interval=5min&apikey=" + API_KEY
FUNCTION = {
    "intraday": "TIME_SERIES_INTRADAY",
    "intraday_adjusted": "TIME_SERIES_INTRADAY_ADJUSTED",
    "daily": "TIME_SERIES_DAILY",
    "daily_adjusted": "TIME_SERIES_DAILY_ADJUSTED",
    "weekly": "TIME_SERIES_WEEKLY",
    "weekly_adjusted": "TIME_SERIES_WEEKLY_ADJUSTED",
    "monthly": "TIME_SERIES_MONTHLY",
    "monthly_adjusted": "TIME_SERIES_MONTHLY_ADJUSTED",
    "quote": "GLOBAL_QUOTE",
    "search": "SYMBOL_SEARCH"
}

# database defaults
LOCAL_DB = {
    "db_host": "localhost",
    "port": 5432,
    "db_name": "Stock_Data",
    "username": "postgres",
    "password": "postgresjezakon" 
}
RDS_DB = {
    "db_host": "mkruzicdb.c2ta4cxogmsp.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "db_name": "Stock_Data",
    "username": "MKruzic",
    "password": "1awsRDSjezakon!" 
} 


STOCK_QUOTES_TABLE = ["quote text PRIMARY KEY"]
QUOTE_TABLE = [int(), str(), float(), float(), float(), float(), int()]
