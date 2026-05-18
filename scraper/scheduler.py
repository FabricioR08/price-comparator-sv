import schedule
import time
from spiders.selectos import scrape_selectos, save_prices as save_selectos
from spiders.vtex import scrape_vtex, save_prices as save_vtex

TIENDAS_VTEX = [
    {"name": "Walmart El Salvador",      "url": "https://www.walmart.com.sv",              "store_id": 1},
    {"name": "Maxi Despensa",            "url": "https://www.maxidespensa.com.sv",          "store_id": 4},
    {"name": "La Despensa de Don Juan",  "url": "https://www.ladespensadedonjuan.com.sv",   "store_id": 3},
]
PRODUCTOS = ["arroz", "frijoles", "aceite", "azucar", "leche", "huevos"]

def correr_scraper():
    print("Iniciando scraper automatico...")

    # Super Selectos
    for producto in PRODUCTOS:
        print(f"  [Selectos] Buscando: {producto}")
        productos = scrape_selectos(producto)
        if productos:
            save_selectos(productos)

    # Tiendas VTEX
    for tienda in TIENDAS_VTEX:
        for producto in PRODUCTOS:
            print(f"  [{tienda['name']}] Buscando: {producto}")
            productos = scrape_vtex(tienda["name"], tienda["url"], tienda["store_id"], producto)
            if productos:
                save_vtex(productos, tienda["store_id"])

    print("Scraper completo")

schedule.every(6).hours.do(correr_scraper)
correr_scraper()

print("Scheduler corriendo... (Ctrl+C para detener)")
while True:
    schedule.run_pending()
    time.sleep(60)
