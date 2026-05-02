from bs4 import BeautifulSoup
import requests

html = requests.get("https://news.ycombinator.com").text
soup = BeautifulSoup(html, 'html.parser')

stories = soup.find_all('tr', class_='athing submission')

for s in stories[:10]:
    link = s.find('span', class_='titleline').find('a')
    print(f"Title: {link.text}")
    print(f"URL: {link.get('href')}\n")