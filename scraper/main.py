from spiders.selectos import scrape_selectos, save_prices

if __name__ == "__main__":
    termino = input("¿Que producto quieres buscar? ")
    print(f" Buscando '{termino}' en Super Selectos...")

    productos = scrape_selectos(termino)

    if productos:
        for p in productos:
            print(f"  {p['name']} - ${p['price']}")
        save_prices(productos)
    else:
        print("No se encontraron productos o el sitio bloqueo la solicitud :c.")
