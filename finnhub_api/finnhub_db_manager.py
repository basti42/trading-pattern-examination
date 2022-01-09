import sqlite3
from pandas import DataFrame as DF
from datetime import datetime
from finnhub_api.finnhub_api_caller import ApiCaller


class FinnhubDBManager:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def table_exists(self, table_name: str) -> bool:
        stmt = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        qr = self.cursor.execute(stmt).fetchone()
        return True if qr[0] == 1 else False

    def create_table(self, table_name: str):
        stmt = f"""CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            open REAL NOT NULL, 
            high REAL NOT NULL,
            close REAL NOT NULL, 
            low REAL NOT NULL,
            date DATETIME NOT NULL,
            timestamp INTEGER NOT NULL,
            volume REAL NOT NULL,
            status STRING NOT NULL)"""
        self.cursor.execute(stmt)
        self.connection.commit()

    def begin_transaction(self):
        self.cursor.execute("BEGIN TRANSACTION")

    def commit_transaction(self):
        self.cursor.execute("COMMIT TRANSACTION")

    def add_candles(self, df: DF, table_name: str):
        self.begin_transaction()
        stmt = "INSERT INTO {} (open, high, close, low, date, timestamp, volume, status)" \
               "VALUES ({}, {}, {}, {}, '{}', {}, {}, '{}')"
        for ind, row in df.iterrows():
            self.cursor.execute(stmt.format(table_name, row['open'], row['high'], row['close'], row['low'],
                                            row['date'], row['t'], row['volume'], row['status']))
        self.commit_transaction()

    def commit_and_close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":

    bot = FinnhubDBManager(db_path="test.db")

    caller = ApiCaller()
    friday_candles = caller.get_latest_candle(sym="TSLA", res="60")

    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    table_name = f"TSLA_hourly_{today.strftime('%Y_%m_%d')}"

    bot.create_table(table_name=table_name)
    bot.add_candles(df=friday_candles, table_name=table_name)

    print()


