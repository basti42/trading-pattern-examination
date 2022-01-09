from datetime import datetime, timedelta
import time
import pandas as pd

from finnhub_api.finnhub_api_caller import ApiCaller
from finnhub_api.finnhub_db_manager import FinnhubDBManager


#
#   This script should be called daily to obtain yesterdays candles
#


if __name__ == "__main__":

    # read in all symbols of the s&p500 companies
    df = pd.read_csv("sp500.csv")

    caller = ApiCaller()
    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    yesterday = today - timedelta(1)

    bot = FinnhubDBManager(db_path="test.db")

    for symbol in df.Symbol.values:
        try:
            print(f"[i] Requesting for {symbol}")
            time.sleep(1)  # to not exceed the rate limit of the finnhub api sleep for a second before each request
            yesterday_candles = caller.get_latest_candle(sym=symbol, res="60")
            if not yesterday_candles:
                continue
            table_name = f"{symbol}_hourly"
            bot.create_table(table_name=table_name)
            bot.add_candles(df=yesterday_candles, table_name=table_name)
        except BaseException as bex:
            print(f"[E] {bex}")

    bot.commit_and_close()
