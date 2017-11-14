# Coin listing

A bot that sends notifications about new listings on some popular cryptocurrency exchanges to Telegram channel [@coin_listing](http://t.me/coin_listing).

## Requirements

* postgresql
* python 3.6

## Quickstart

``` sh
$ git clone https://github.com/ape364/coinlisting.git
$ cd coinlisting
$ export COINLISTING_BOT_TOKEN=%YOUR_BOT_TOKEN% # telegram bot token from @BotFather
$ export DATABASE_URL=%YOUR_DSN_STRING% # database DSN string
$ export COINLISTING_BOT_CHECK_INTERVAL=600 # check interval in seconds
$ export COINLISTING_BOT_CHANNEL_ID=%YOUR_CHANNEL_ID% # channel id as negative number
$ export COINLISTING_BOT_ATTEMPTS_LIMIT=5 # request attempts limit
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ python coin_checker.py
```

## Supported exchanges

* [Bittrex](https://bittrex.com/)
* [Liqui](https://liqui.io/)
* [Kraken](https://www.kraken.com/)
* [Poloniex](https://poloniex.com/)
* [Binance](https://www.binance.com/)
* [Bitfinex](https://www.bitfinex.com/)
* [Bitstamp](https://www.bitstamp.net/)
* [Cryptopia](https://www.cryptopia.co.nz/)
* [Gate](https://gate.io/)
* [Radar Relay](https://app.radarrelay.com/)
* [Kucoin](https://www.kucoin.com/)

## Contributing

Feel free to send PR with new exchanges. You need to implement logic of BaseApi class, described in exchange/base.py

## Contacts

Telegram [@ape364](http://t.me/ape364)
