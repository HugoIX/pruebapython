import services
import sys

# HERE IS THE PRECHARGED ARTICLES ON THE INVENTORY (Requirement: 5 pre-loaded products)
inventory = [
    {
        "name": "El Alquimista",
        "author": "Paulo Coelho",
        "category": "novela",
        "price": 25.00,
        "stock": 15,
    },
    {
        "name": "Obra Negra",
        "author": "Gonzalo Arango",
        "category": "poesia",
        "price": 55.00,
        "stock": 6,
    },
    {
        "name": "Narraciones Extraordinarias",
        "author": "Edgar Allan Poe",
        "category": "suspenso",
        "price": 35.00,
        "stock": 10,
    },
    {
        "name": "El Arte de la Guerra",
        "author": "Sun Tzu",
        "category": "literatura",
        "price": 20.00,
        "stock": 8,
    },
    {
        "name": "La Iliada",
        "author": "Homero",
        "category": "clasica",
        "price": 15.00,
        "stock": 7,
    }
]

sales = []

# Function to make the customer can choose to return to main menu or leave the program.
def return_to_menu():
    while True:
        user_input = input("presione M para regresar al menu o S para salir del programa: ").strip().lower()

        if user_input == "m":
            break
        elif user_input == "s":
            print("Gracias. Hasta Luego.")
            sys.exit()
        else:
            print("Opción Invalida. Presione 'M' o 'S'.")

# Main menu with several functions for search, consult and update information.
def main_menu():
    global inventory, sales

    while True:
        print("BIENVENIDO AL SISTEMA DE INVENTARIO DE LIBRERIA NACIONAL")
        print("Por favor, seleccione una de las siguientes opciones: ")
        print("1. AGREGAR LIBRO")
        print("2. MOSTRAR INVENTARIO")
        print("3. BUSCAR POR TITULO")
        print("4. BUSCAR POR AUTOR")
        print("5. BUSCAR POR CATEGORIA")
        print("6. REGISTRAR VENTA")
        print("7. BORRAR LIBRO")
        print("8. ESTADISTICAS")
        print("9. SALIR")

        try:
            option = int(input("Por favor ingrese una opción(1-9): ").strip())

            if option == 1:
                print("AGREGAR LIBRO")
                name = input("Ingrese el titulo del Libro: ").strip()
                author = input("Ingrese el nombre del Autor: ").strip()
                category = input("Ingrese la Categoria: ").strip()

                try:
                    price = float(input("Ingrese el precio: "))
                    if price <= 0:
                        raise ValueError("El precio debe ser positivo.")

                    stock = int(input("Ingrese la cantidad: "))
                    if stock <= 0:
                        raise ValueError("La cantidad debe ser positiva.")
                except ValueError as e:
                    print(f"ERROR de entrada: {e}")
                    return_to_menu()
                    continue
                
                result = services.add_product(inventory, name, author, category, price, stock)
                print(result)
                return_to_menu()

            elif option == 2:
                print("INVENTARIO ACTUAL")
                services.show_inventory(inventory) 
                return_to_menu()

            elif option == 3:
                print("BUSCAR POR TITULO")
                if not inventory:
                    print("El inventario está vacío.")
                else:
                    search_name = input("Ingrese el titulo a buscar: ").strip()
                    product_found = services.search_product(inventory, search_name)

                    if product_found:
                        print("Titulo encontrado:")
                        print(f"Nombre: {product_found['name']} | Autor: {product_found['author']} | Precio: ${product_found['price']:.2f} | Cantidad: {product_found['stock']} \n")
                    else:
                        print("Producto no encontrado.")
                return_to_menu()
            
            elif option == 4:
                print("\BUSCAR POR AUTOR")
                if not inventory:
                    print("El inventario está vacío.")
                else:
                    author_name = input("Ingrese el nombre del autor: ").strip()
                    products_found = services.search_author(inventory, author_name) 

                    if products_found:
                        print("Producto no encontrado:")
                        for prod in products_found:
                             print(f"Nombre: {prod['name']} | Autor: {prod['author']} | Precio: ${prod['price']:.2f} | Cantidad: {prod['stock']} \n")
                    else:
                        print("Autor no encontrado.")
                return_to_menu()

            elif option == 5:
                print("BUSCAR POR CATEGORIA")
                if not inventory:
                    print("El inventario está vacío.")
                else:
                    search_cat = input("Ingrese la categoria a ingresar: ").strip()
                    products_found = services.search_category(inventory, search_cat) 

                    if products_found:
                        print("Porductos no encontrados en esta categoria:")
                        for prod in products_found:
                             print(f"Nombre: {prod['name']} | Autor: {prod['author']} | Categoria: {prod['category']} | Precio: ${prod['price']:.2f} | Cantidad: {prod['stock']} \n")
                    else:
                        print("Categoria no disponible.")
                return_to_menu()

            elif option == 6:
                print("\REGISTRAR VENTA")
                product_name = input("Ingrese el titulo a vender: ").strip()
                product = services.search_product(inventory, product_name)
                
                if product: 
                    print(f"Titulo seleccionado: {product['name']} | Disponible: {product['stock']}")
                    try:
                        quantity = int(input("Ingrese la cantidad a vender: ").strip())

                        if quantity <= 0:
                            print("Cantidad debe ser superior a 0.")
                            continue
                        client_name = input("Ingrese el nombre del cliente: ").strip()

                        sale_date = input("Ingrese fecha (AAAA-MM-DD, dejar en blanco para hoy): ") or services.get_current_date()

                        discount = 0.0 

                        result = services.register_sale(inventory, sales, product_name, quantity, client_name, discount, sale_date)
                        print(result)

                    except ValueError as e:
                        print(f"ERROR: {e}")

                else:
                    print("Producto no encontrado en inventario.")
                return_to_menu()

            elif option == 7:
                print("ELIMINAR LIBRO")
                if not inventory:
                    print("El Inventario esta vacio.")
                else:
                    name_to_delete = input("Ingrese el nombre del libro a borrar: ").strip()
                    result = services.delete_product(inventory, name_to_delete)
                    print(result)
                return_to_menu()

            elif option == 8:
                services.generate_reports(inventory, sales)
                return_to_menu()

            elif option == 8:
                print("REPORTE Y ESTADISTICAS")
                services.generate_reports(inventory, sales)
                return_to_menu()
                

            elif option == 9:
                print("Saliendo del programa. Hasta luego")
                sys.exit()

            else:
                print("Opción invalida. Seleccione una opción del 1 al 9.")

        except ValueError:
            print("ERROR: Entradaa invalidad. Solo digite números.")
            return_to_menu()

if __name__ == "__main__":
    main_menu()

