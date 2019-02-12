from datetime import datetime, date
import psycopg2
from settings import LOCAL_DB, QUOTE_TABLE, STOCK_QUOTES_TABLE, FUNCTION


def db(commit):
    """database connection for executing sql"""
    def sql_wrapper(sql):
        def wrapper(*args, **kwargs):
            db = psycopg2.connect(
                host=LOCAL_DB["db_host"], 
                port=LOCAL_DB["port"],
                user=LOCAL_DB["username"],
                password=LOCAL_DB["password"],
                dbname=LOCAL_DB["db_name"]
            )
            data = []  
            c = db.cursor()
            e = sql(*args, **kwargs)
            if type(e).__name__ != "tuple":
                c.execute(e)
            else: 
                c.executemany(e[0], e[1])
            
            if commit:
                db.commit()
                db.close()
            else:
                try:
                    data = c.fetchall()
                except AttributeError:
                    pass
            db.close()
            return data
        return wrapper
    return sql_wrapper
    

def filter_sql(sql, condition="", order_by="", direction="", limit=""):
    if condition != "":
        condition = f" WHERE {condition}"
    if order_by != "":
        order_by = f" ORDER BY {order_by} {direction}"
    if limit != "":
        limit = f" LIMIT {limit}"
    sql = sql + condition + order_by + limit
    return sql


@db(commit=False)
def query(tb_name, columns, **kwargs):
    sql = f"SELECT {columns} FROM {tb_name}"
    final = filter_sql(sql, **kwargs)
    return final


@db(commit=True)
def insert(tb_name, columns, data):
    values = str()
    column = "%s"
    sep = ", "      
    if len(columns) == 1:
        values = column
    else:
        for col in columns:
            values += column + sep
        values = values[:-2]
    sql = f"INSERT INTO {tb_name} VALUES(DEFAULT, {values})"
    return sql, data


def delete(tb_name, columns):
    sql = f"DELETE FROM {tb_name}"
    return sql


def save_data_to_db(quote_id, data, tb_name, date_range):
    """checks the last entry from selected quote
    and updates new entries to database"""

    bulk = list()

    try:
        last_entry = query(tb_name, "*", condition=f"quote={quote_id}", order_by="date", direction="DESC", limit=1)[0][2]
    except IndexError:
        last_entry = None

    for entry in data:
        if date_range == "intraday":
            date_format = "%Y-%m-%d %H:%M:%S"
            api_entry = datetime.strptime(entry, date_format)
            if last_entry == None:
                last_entry = datetime(1000, 1, 1)
            print("in", api_entry)
        else:
            date_format = "%Y-%m-%d"
            api_entry = datetime.strptime(entry, date_format).date()
            if last_entry == None:
                last_entry = date(1000, 1, 1)
            print("d", api_entry)

        if api_entry > last_entry:
            clean_data = data[entry]
            bulk.append((
                quote_id,
                entry,
                float(clean_data["1. open"]),
                float(clean_data["2. high"]),
                float(clean_data["3. low"]),
                float(clean_data["4. close"]),
                int(clean_data["5. volume"])
            ))
        else:
            break
    print("data to be commited: ", bulk)

    if len(bulk) > 0:
        insert(tb_name, QUOTE_TABLE, data=bulk)
