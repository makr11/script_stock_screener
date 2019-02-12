import argparse
import sqlite3
from settings import FUNCTION, STOCK_QUOTES_TABLE
import av_script 
import av_db

def Main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument(
        'lists',
        choices=['quotes'],
        help=['List of available quotes and tables']
    )

    parser_prices = subparsers.add_parser('prices')
    parser_prices.add_argument(
        'quote',
        help=['Quote prices']
    )
    parser_prices.add_argument(
        'date_range',
        choices=['intraday'],
        help=['Quote prices']
    )

    parser_run = subparsers.add_parser('run-script')
    parser_run.add_argument(
        'date_range',
        choices=['intraday', 'daily', 'weekly', 'monthly'],
        help='Choose price date interval')

    parser_create = subparsers.add_parser('add-quote')
    parser_create.add_argument(
        'quote',
        nargs="+",
        help='Choose quote for tracking api data')

    parser_create = subparsers.add_parser('del-records')
    parser_create.add_argument(
        'table_name',
        nargs="+",
        help='Delete quote table records, example: "MSFT_INTRADAY"')

    args = parser.parse_args()

    quotes = [i for i in av_db.query("quotes", "*")]

    if args.subcommand == "run-script":
        date_range = args.date_range.lower()

        av_script.run_script(quotes, date_range)

    elif args.subcommand == "add-quote":
        quote_list = args.quote
        
        av_script.add_quote(quote_list, quotes)

    elif args.subcommand == "del-records":
        tb_names = args.table_name
        for tb in tb_names:
            av_db.sql_to_db("del records", tb, "*")

    elif args.subcommand == "list":

        if args.lists == "quotes":
            for quote in quotes:
                print(quote)

    elif args.subcommand == "prices":
        quote = Quote(args.quote, args.date_range)
        quote.intraday_list()


if __name__ == "__main__":
    Main()