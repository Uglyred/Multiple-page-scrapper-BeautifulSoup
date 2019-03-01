from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests, bs4

base_url = 'https://www.x-kom.pl/g-2/c/159-laptopy-notebooki-ultrabooki.html'

filename = "laptopy_x-kom_2.csv"
f = open(filename, "w")

headers = "producent, nazwa, kategoria, cena, link" + "\n"

f.write(headers)

#wyciąga ostatnia strone
r = requests.get("https://www.x-kom.pl/g-2/c/159-laptopy-notebooki-ultrabooki.html")
soup = bs4.BeautifulSoup(r.text, "html.parser")
last_page = soup.select_one(".pagination-wrapper > div > span > span").text

for page_number in range(1, int(last_page)):
	page_url = base_url + "?page=" + str(page_number)
	uClient = urlopen(page_url)
	page_html = uClient.read()
	uClient.close()

	ru = requests.get(page_url)
	page_soup = bs4.BeautifulSoup(ru.text, 'html.parser')

	product_list = page_soup.find("div", {"id": "productList"})
	products = product_list.find_all("div", {"class": "product-item product-impression"})

	for product in products:

		screen = product.find('div', {'class': 'description-wrapper'})
		screen_value = screen.a['title']
		href_link = screen.a['href']
		full_link = base_url + href_link
		brand = product['data-product-brand']
		name = product['data-product-name']
		price = product['data-product-price']

		print("link: " + full_link)
		print("producent: " + brand)
		print("nazaw: " + name)
		print("cena: " + price)
		print("kategoria: " + screen_value[0:22])

		f.write(brand + "," + name.replace(",", " ") + "," + screen_value[0:22].replace(",", "_") + "," + price + "," + full_link + "\n")

f.close()

