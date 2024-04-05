import datetime

import requests

from bitpin.models import BitPinCurrency, BitPinNetwork


def get_default_prices():
    return {
        "price_info_price": 0.0,
        "price_info_time": None,
        "price_info_change": 0.0,
        "price_info_min": 0.0,
        "price_info_max": 0.0,
        "price_info_mean": 0.0,
        "price_info_value": 0.0,
        "price_info_amount": 0.0,
        "price_info_market_value": 0.0,
        "price_info_market_amount": 0.0,
        "price_info_usdt_price": 0.0,
        "price_info_usdt_change": 0.0,
        "price_info_usdt_time": None,
        "price_info_usdt_min": 0.0,
        "price_info_usdt_max": 0.0,
        "price_info_usdt_mean": 0.0,
        "price_info_usdt_value": 0.0,
        "price_info_usdt_amount": 0.0,
        "price_info_usdt_market_value": 0.0,
        "price_info_usdt_market_amount": 0.0
    }


def get_bitpin_currencies_cron():
    print("CRONJOB start:", datetime.datetime.now())
    response = requests.get("https://api.bitpin.ir/v1/mkt/currencies/")
    if response.status_code != 200:
        print("cron fail at:", datetime.datetime.now(), response)
        return
    data = response.json()
    for row in data["results"]:
        if row["code"] == 'Toman':
            print(row)
        if not isinstance(row, dict):
            continue

        del row["id"]
        price = row.pop("price_info") if "price_info" in row else {}
        price_usdt = row.pop("price_info_usdt") if "price_info_usdt" in row else {}
        networks = row.pop("networks") if "networks" in row else []
        try:
            prices = {}
            bitasia_active = False
            for k, v in price.items():
                if k == "price" and v != "0": bitasia_active = True
                if k == "time" and v == "0": v = None
                prices[f"price_info_{k}"] = v

            for k, v in price_usdt.items():
                if k == "time" and v == "0": v = None
                prices[f"price_info_usdt_{k}"] = v

            if not prices:
                prices = get_default_prices()

            currency = BitPinCurrency.objects.filter(code=row.get('code'))
            created = False
            if not bool(currency):
                defaults = {k: v for k, v in row.items()}
                defaults["bitasia_active"] = bitasia_active
                defaults["min_withdraw"] = float(defaults["min_withdraw"])
                defaults["max_withdraw_commission"] = float(defaults["max_withdraw_commission"])
                created = True
                currency = BitPinCurrency.objects.create(**defaults, **prices)
            else:
                currency.update(**prices)
            if not created:
                currency = currency.first()
            for net in networks:
                network, c = BitPinNetwork.objects.get_or_create(code=net.get('code'),
                                                                 defaults={"title": net.get("title"),
                                                                           "title_fa": net.get(
                                                                               "title_fa")})
                if network.id not in [x.id for x in currency.network_ids.all()]:
                    currency.network_ids.add(network)

            currency.save()
        except Exception as e:
            print(row, row["code"])
            print(e)

    print("DONE")