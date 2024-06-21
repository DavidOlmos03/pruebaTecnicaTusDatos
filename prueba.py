import requests
from bs4 import BeautifulSoup

client = requests.Session()

html = client.get('https://parascrapear.com/login').content
soup = BeautifulSoup(html,'html.parser')

print(soup.find(id="top-text").text)
