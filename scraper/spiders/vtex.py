from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_connection
from datetime import datetime

def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def scrape_vtex(store_name, base_url, store_id, search_term):
    driver = get_driver()
    productos = []

    try:
        url = f"{base_url}/{search_term}?_q={search_term}&map=ft"
        print(f"  Abriendo {url}...")
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.vtex-product-summary-2-x-element"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.select("article.vtex-product-summary-2-x-element")
        print(f"  Encontradas {len(items)} tarjetas en {store_name}")

        for item in items:
            try:
                # Nombre
                name_tag = item.select_one("span.vtex-product-summary-2-x-productBrand")
                if not name_tag:
                    name_tag = item.select_one(".vtex-product-summary-2-x-nameContainer")
                if not name_tag:
                    continue
                name = name_tag.text.strip()

                # Precio
                price_tag = item.select_one(".vtex-product-price-1-x-sellingPriceValue")
                if not price_tag:
                    price_tag = item.select_one(".vtex-product-price-1-x-currencyContainer")
                if not price_tag:
                    continue
                price_text = price_tag.text.strip().replace("$", "").replace(",", "").strip()
                price = float(price_text)

                # Link
                link_tag = item.select_one("a")
                product_url = link_tag["href"] if link_tag else ""
                if product_url and not product_url.startswith("http"):
                    product_url = base_url + product_url

                productos.append({
                    "name": name,
                    "price": price,
                    "product_url": product_url
                })

            except Exception as e:
                print(f"  Error parseando producto: {e}")
                continue

    except Exception as e:
        print(f"  Error con Selenium: {e}")

    finally:
        driver.quit()

    return productos


def save_prices(productos, store_id):
    conn = get_connection()
    cur = conn.cursor()

    for p in productos:
        cur.execute(
            "SELECT id FROM product WHERE LOWER(name) = LOWER(%s)",
            (p["name"],)
        )
        result = cur.fetchone()

        if result:
            product_id = result[0]
        else:
            cur.execute(
                "INSERT INTO product (name) VALUES (%s) RETURNING id",
                (p["name"],)
            )
            product_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO price (product_id, store_id, price, last_updated, product_url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (product_id, store_id, p["price"], datetime.now(), p["product_url"]))

    conn.commit()
    cur.close()
    conn.close()
    print(f"{len(productos)} productos guardados")
