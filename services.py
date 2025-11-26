import datetime

# INVENTORY MANAGEMENT FUNCTIONS

def add_product(inventory_list, name, author, category, price, stock):

    new_product = {
        "name": name.strip().title(),
        "author": author.strip().title(),
        "category": category.strip().title(),
        "price": float(price),
        "stock": int(stock),
    }
    inventory_list.append(new_product)
    return f"El libro '{name}' fue agregado correctamente."

#SHOW PRODUCT INVENTORY WITH A FOR CICLE ON THE LIST

def show_inventory(inventory_list):

    if not inventory_list:
        print("Inventario vacío, Agregue articulos.")
        return

    print("INVENTARIO ACTUAL")
    for i, item in enumerate(inventory_list): 
        print(f"[{i + 1}] | Titulo: {item['name']} | Autor: {item['author']} | Categoria: {item['category']} | Precio: ${item['price']:.2f} | Cantidad: {item['stock']}")

#SEARCH FOR PRODUCT USING AN INPUT
def search_product(inventory_list, name):

    search_term = name.strip().lower()
    return next((item for item in inventory_list if item["name"].lower() == search_term), None)

#SEARCH FOR AUTHOR USING AN INPUT
def search_author(inventory_list, author_name):

    search_term = author_name.strip().lower()
    results = [item for item in inventory_list if search_term in item["author"].lower()]
    return results

#SEARCH FOR CATEGORY USING AN INPUT
def search_category(inventory_list, category_name):

    search_term = category_name.strip().lower()
    results = [item for item in inventory_list if item["category"].lower() == search_term]
    return results


#DELETE FUNCTION AFTER SEARCH THE PRODUCT ON THE LIST

def delete_product(inventory_list, name):

    product = search_product(inventory_list, name)

    if product:
        inventory_list.remove(product)
        return f"Producto '{name}' borrado correctamente."
    else:
        return f"Producto '{name}' no encontrado."

#SALES MANAGEMENT AND REPORTING FUNCTIONS COMMENTED WITH SOME OF THE REQUIREMENTS

def get_current_date():
    return datetime.date.today().isoformat()

def register_sale(inventory_list, sales_list, product_name, quantity, client_name, discount_rate, sale_date): # se corrige que se declaraban 6 funciones y se llamaban 7, se agrego el "sale_date" y se logra corregir. 

    product = search_product(inventory_list, product_name)

    if not product:
        return f"Error: Producto '{product_name}' no encontrado."
    
    # Requirement: Validate stock availability
    if product["stock"] < quantity:
        return f"Error: Cantidad insuficiente para '{product_name}'. Disponible: {product['stock']}"
    
    # Requirement: Update stock automatically
    product["stock"] -= quantity
    
    # Calculate prices
    final_price_per_item = product["price"] * (1 - discount_rate)
    total_sale_net = final_price_per_item * quantity


    sale_record = {
        "client_name": client_name,
        "product_name": product_name,
        "author": product["author"],
        "quantity": quantity,
        "price_per_item_gross": product["price"],
        "discount_applied": discount_rate,
        "total_sale_net": total_sale_net,
        "date": sale_date #Se soluciona el proceso de llamar la fecha de venta y no el get.datetime()
    }
    sales_list.append(sale_record)
    return f"Venta registrada con éxito. Total neto: ${total_sale_net:.2f}"


def generate_reports(inventory_list, sales_list):

    print("REPORTE DE VENTAS Y ESTADISTICAS")

    if not sales_list:
        print("NO HAY VENTAS ACTUALMENTE.")
        return

    # 1. Calculate Gross and Net Income 
    gross_income_calc = lambda sales_records: sum(s['price_per_item_gross'] * s['quantity'] for s in sales_records)
    net_income_calc = lambda sales_records: sum(s['total_sale_net'] for s in sales_records)

    gross_income = gross_income_calc(sales_list)
    net_income = net_income_calc(sales_list)

    print(f"total ganancias (antes de descuentos): ${gross_income:,.2f}")
    print(f"Total neto: ${net_income:,.2f}")

    # 2. Generate report of total sales grouped by author
    sales_by_author = {}
    for sale in sales_list:
        author = sale['author']
        if author not in sales_by_author:
            sales_by_author[author] = 0
        sales_by_author[author] += sale['total_sale_net']
    
    print("Total de ventas por autor(Valor Neto): ")
    for author, sales_amount in sales_by_author.items():
        print(f" - {author}: ${sales_amount:,.2f}")

    # 3. Show the top 3 most sold products
    product_sales_qty = {}
    for sale in sales_list:
        name = sale['product_name']
        if name not in product_sales_qty:
            product_sales_qty[name] = 0
        product_sales_qty[name] += sale['quantity']
    
    # use of lambda key
    sorted_products = sorted(product_sales_qty.items(), key=lambda item: item[1], reverse=True)
    
    print("Top 3 maás vendidos (Por cantidad):")
    for rank, (product_name, quantity_sold) in enumerate(sorted_products[:3], 1):
        print(f" {rank}. {product_name} | Cantidad vendida: {quantity_sold}")

