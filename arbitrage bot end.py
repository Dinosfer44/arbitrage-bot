import requests
import json

binance_coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "TONUSDT"]
kucoin_coins = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ADA-USDT", "TON-USDT"]

url_binance = "https://api.binance.com/api/v3/ticker/price"
url_kucoin = "https://api.kucoin.com/api/v1/market/allTickers"

#записываем данные в формате json
kucoin_response = requests.get(url_kucoin)
kucoin_prices = kucoin_response.json()
with open ("kucoin_prices.json", "w", encoding="utf-8") as kucoin_file:
    json.dump(kucoin_prices, kucoin_file, indent=4)
binance_response = requests.get(url_binance)
binance_prices = binance_response.json()
with open ("binance_prices.json", "w", encoding="utf-8") as binance_file:
    json.dump(kucoin_prices, binance_file, indent=4)

#читаем данные из json файлов
with open("kucoin_prices.json", "r", encoding="utf-8") as filek:
    datak = filek.read()
with open ("binance_prices.json", "r", encoding="utf-8") as fileb:
    datab = fileb.read()

#Отбираем монеты
kucoin_filtered_prices = {}
for coin in kucoin_coins:
    for item in kucoin_prices['data']['ticker']:
        if item['symbol'] == coin:
            kucoin_filtered_prices[coin] = float(item['last'])

binance_filtered_prices = {}
for coin in binance_coins:
    for item in binance_prices:
        if item['symbol'] == coin:
            binance_filtered_prices[coin] = float(item['price'])

#Очищаем список кукоина
cleaned_kucoin_filtered_prices= {}
for coin, price in kucoin_filtered_prices.items():
    cleaned_coin = coin.replace("-", "")
    cleaned_kucoin_filtered_prices[cleaned_coin] = (price)

#Обозначаем спред
spread_threshold = 0.000005

#Производим сравнение цен
for coin in binance_filtered_prices:
    cleaned_coin = coin.replace("-", "")
    if cleaned_coin in cleaned_kucoin_filtered_prices:
        kucoin_price = cleaned_kucoin_filtered_prices[cleaned_coin]
        binance_price = binance_filtered_prices[coin]

        # Рассчитываем спред
        price_difference = abs(kucoin_price - binance_price)
        avg_price = (kucoin_price + binance_price) / 2
        spread = price_difference / avg_price

        # Проверяем, превышает ли спред порог
        if spread > spread_threshold:
            print(f"Арбитраж найден между {coin}: KuCoin - {kucoin_price}, Binance - {binance_price}, "
                  f"разница: {price_difference:.2f} ({spread * 100:.4f}%)")
            arbitrage_found = True

# Если арбитраж не найден, выводим соответствующее сообщение
if not arbitrage_found:
    print("Арбитраж не найден. Все цены находятся в пределах допустимого спреда.")



