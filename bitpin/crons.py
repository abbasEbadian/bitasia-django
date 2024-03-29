import datetime

import requests

from bitpin.models import BitPinCurrency, BitPinNetwork


def get_bitpin_currencies_cron():
    response = requests.get("https://api.bitpin.ir/v1/mkt/currencies/")
    if response.status_code != 200:
        print("cron fail at:", datetime.datetime.now(), response)
        return
    data = response.json()
    for row in data["results"]:
        if not isinstance(row, dict):
            continue

        del row["id"]
        price = row.pop("price_info") if "price_info" in row else {}
        price_usdt = row.pop("price_info_usdt") if "price_info_usdt" in row else {}
        networks = row.pop("networks") if "networks" in row else []
        try:
            prices = {}
            for k, v in price.items():
                if k == "time" and v == "0": v = None
                prices[f"price_info_{k}"] = v

            for k, v in price_usdt.items():
                if k == "time" and v == "0": v = None
                prices[f"price_info_usdt_{k}"] = v

            currency = BitPinCurrency.objects.filter(code=row.get('code'))
            created = bool(currency)
            if not currency:
                defaults = {k: v for k, v in row.items()}
                currency = BitPinCurrency.objects.create(**defaults, **prices)
            else:
                currency.update(**prices)
            if not created:
                currency = currency.first()
            for net in networks:
                network, c = BitPinNetwork.objects.get_or_create(code=net.get('code'),
                                                                 defaults={"title": row.get("title"),
                                                                           "title_fa": row.get(
                                                                               "title_fa")})
                if network.id not in [x.id for x in currency.network_ids.all()]:
                    currency.network_ids.add(network)

            currency.save()
            print("DONE")
        except Exception as e:
            print(e)
