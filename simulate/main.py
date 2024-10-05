import random
import time

products = [
    {
        "name": 'Long Island',
        "base_price": 12000,
        "current_price": 12000,
        "trend": "stable",
        "min_price": 8000,
        "max_price": 20000,
        "quantity": 50
    },
    {
        "name": 'Margarita',
        "base_price": 12000,
        "current_price": 12000,
        "trend": "stable",
        "min_price": 8000,
        "max_price": 20000,
        "quantity": 50
    },
    {
        "name": 'Cosmopolitan',
        "base_price": 15000,
        "current_price": 15000,
        "trend": "stable",
        "min_price": 10000,
        "max_price": 25000,
        "quantity": 100
    },
    {
        "name": 'Espresso Martini',
        "base_price": 10000,
        "current_price": 10000,
        "trend": "stable",
        "min_price": 7500,
        "max_price": 15000,
        "quantity": 150
    },
    {
        "name": 'Pina Colada',
        "base_price": 10000,
        "current_price": 10000,
        "trend": "stable",
        "min_price": 7500,
        "max_price": 15000,
        "quantity": 120
    }
]

price_volatility_rise = 6 # % per 2 orders
price_volatility_fall = 3 # %
average_requests_per_session = 5


def test_static_pricing():
    total_max_sales = 0
    total_max_cost = 0
    for product in products:
        product_max_sales = product["base_price"] * product["quantity"]
        total_max_sales += product_max_sales
    for product in products:
        cost_price = product["base_price"] - (product["base_price"] * 0.10)
        product_max_cost = cost_price * product["quantity"]
        total_max_cost += product_max_cost
    return total_max_cost, total_max_sales


def test_dynamic_pricing():
    total_orders = []
    orders = {}
    products_available = [0,1,2,3,4]

    while products_available:

        # check last session orders for all products
        for i in range(len(products)-1):
            no_of_orders = orders.get(i, 0)
            product = products[i]
            if no_of_orders > 1:
                # price increase
                percentage_increase = price_volatility_rise*(no_of_orders//3)
                amount_increased = product["current_price"] + (percentage_increase/100 * product["current_price"])
                product["current_price"] = min(amount_increased, product["max_price"])
                product["trend"] = "up"

                print(f"{product['name']} +{percentage_increase/100}%: NGN{product['current_price']} ")
            else:

                # price decrease
                amount_decreased = product["current_price"] - (price_volatility_fall/100 * product["current_price"])
                product["current_price"] =  max(amount_decreased, product["min_price"])
                product["trend"] = "down"
                print(f"{product['name']} -{price_volatility_fall/100}%: NGN{product['current_price']}")

        # reset orders for session
        orders = {}

        for i in range(average_requests_per_session):
            product_id = random.randint(0, 4)
            order_quantity = 1
            product = products[product_id]
            if product["quantity"] > 0:
                if product['trend'] == "down" or product['trend'] == "stable":
                    order_quantity = order_quantity + random.randint(1,5)
                    if order_quantity > product["quantity"]:
                        order_quantity = product["quantity"]

                product["quantity"] -= order_quantity
                orders[product_id] = order_quantity
                total_orders.append(
                    {"product_id": product_id, "sold_price": product["current_price"], "quantity": order_quantity}
                )
        
            else:
                if product_id in products_available:
                    products_available.remove(product_id)

        

    total_max_cost = 0
    products_index = {}
    for order in total_orders:
        sale = order["sold_price"] * order["quantity"] 
        total_max_cost += sale

        product_id  = order.get("product_id")
        product_name = products[product_id]["name"]
        products_index[product_name] = products_index.get(product_name, 0) +  sale
    
    print(products_index)
    return total_max_cost



total_max_cost, total_max_sales = test_static_pricing()
print("Maximum Cost (NGN): ", total_max_cost)
print("Maximum Sales (NGN) (Static Pricing): ", total_max_sales)

total_max_sales_dynamic = test_dynamic_pricing()
net_profit = (total_max_sales - total_max_cost) / total_max_cost * 100
print(f"Maximum Profit (Static Pricing): { round(net_profit, 2) }%")


net_profit = (total_max_sales_dynamic - total_max_cost) / total_max_cost * 100
print(f"Maximum Profit (Dynamic Pricing): { round(net_profit, 2) }%")
 