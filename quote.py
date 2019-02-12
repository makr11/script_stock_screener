from datetime import datetime
import pandas


class Quote:

    def __init__(self, quote, date_range):
        self.quote = quote.upper()
        self.date_range = date_range.upper()

    def intraday_list(self):
        data = sql_to_db("query", self.quote + "_" + self.date_range, "*")
        dates = {}

        for entry in data:
            date_time = datetime.strptime(entry[0], "%Y-%m-%d %H:%M:%S")
            date = date_time.date()
            time = date_time.time()

            if date not in dates:
                dates.update({date: {
                                    "Time": [time],
                                    "Open": [entry[1]],
                                    "Low": [entry[2]],
                                    "High": [entry[3]],
                                    "End": [entry[4]],
                                    "Volume": [entry[5]]
                                    }})
            else:
                dates[date]["Time"].append(time)
                dates[date]["Open"].append(entry[1])
                dates[date]["Low"].append(entry[2])
                dates[date]["High"].append(entry[3])
                dates[date]["End"].append(entry[4])
                dates[date]["Volume"].append(entry[5])

        for date, data in dates.items():
            print(date)
            df = pandas.DataFrame(data)
            print(df)
