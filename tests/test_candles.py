from unittest import TestCase
from custom_types.candle import CandleType, Candle


class TestCandles(TestCase):

    def test_bull_bear_candles(self):
        d = [{"time": 1609200000, "high": 22336.77, "low": 21184.31, "open": 22139.16, "volumefrom": 15421.36,
              "volumeto": 335784748.42, "close": 22328.53, "conversionType": "direct", "conversionSymbol": ""},
             {"time": 1609286400, "high": 23549.22, "low": 22328.53, "open": 22328.53, "volumefrom": 19904.5,
              "volumeto": 456802214.71, "close": 23476.95, "conversionType": "direct", "conversionSymbol": ""}
             ]
        candles = list()
        for json in d:
            candles.append(Candle(_high=json["high"],
                                  _low=json["low"],
                                  _close=json["close"],
                                  _open=json["open"],
                                  _volume_from=json["volumefrom"],
                                  _volume_to=json["volumeto"]))

        self.assertEqual(CandleType.BULL, candles[0].type)
        self.assertEqual(CandleType.BULL, candles[1].type)
