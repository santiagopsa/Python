import bs4
import requests

resultado = requests.get('https://coinmarketcap.com/es/')


sopa=bs4.BeautifulSoup(resultado.text, 'lxml')
print('Valor Bitcoin: '+sopa.select('.cmc-link>span')[0].get_text())
