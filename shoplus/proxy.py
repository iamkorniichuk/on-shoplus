import requests


def get_proxies():
    proxy_list_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all"
    proxies = requests.get(proxy_list_url).text.split()

    check_proxy_url = "https://httpbin.org/ip"
    for obj in proxies:
        result = {
            "http": f"http://{obj}",
            "https": f"http://{obj}",
        }
        try:
            response = requests.get(check_proxy_url, proxies=result, timeout=10)
            response.raise_for_status()
            return result
        except:
            continue
