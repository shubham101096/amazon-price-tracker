import smtplib
import requests
from bs4 import BeautifulSoup
import lxml
import os

HEADERS = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
           "Accept-Language":"en-US,en;q=0.9"}

URL = "https://www.amazon.in/Apple-12W-USB-Power-Adapter/dp/B08D7GNCV2/ref=pd_rhf_ee_s_pd_crcd_1_2/259-3536655-8771134?_encoding=UTF8&pd_rd_i=B08D7GNCV2&pd_rd_r=d221a98a-021c-43b3-a339-f00a1db65fd9&pd_rd_w=bF8pr&pd_rd_wg=If1Di&pf_rd_p=fbb8e9ba-d910-4a9e-8143-6ce2a84b81ca&pf_rd_r=Y7TRH7YYXVQS65D71FZT&psc=1&refRID=Y7TRH7YYXVQS65D71FZT"

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

response = requests.get(URL, headers=HEADERS)
print(response)
soup = BeautifulSoup(response.content, "lxml")

price = soup.find(id="priceblock_ourprice").getText().split("₹ ")[1]
print(price)

price_list = list(price)
print(price_list)

price_list = [i for i in price_list if i!=","]
print(price_list)

price_float = float("".join(price_list))
print(price_float)

title = soup.find(id="productTitle").getText().strip()
print(title)

required_price = 2000

if price_float < required_price:

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        msg = f"{title}\n{price}\n{URL}"
        connection.sendmail(EMAIL, EMAIL, f"Subject: Amazon Price Tracker \n\n {msg}")
        print("Mail sent")
