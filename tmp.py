import requests

url = 'https://ipv4.icanhazip.com'
proxies = {
    'http': 'http://S1zO6DCYBhFoBmAY:WVOEMucxzg54GrI1@geo.iproyal.com:12321',
    'https': 'http://S1zO6DCYBhFoBmAY:WVOEMucxzg54GrI1@geo.iproyal.com:12321'
}

response = requests.get(url, proxies=proxies)
print(response.text)
