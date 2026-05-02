import csv

def analyze_csv():
    try:
        with open("sales_data.csv") as f:
            input_file = csv.DictReader(f)
            total_revenue = 0
            revenue_electronics = 0
            revenue_furniture = 0
            highest_sales = None
            highest_sales_product = None

            for row in input_file:
                price = float(row["price"])
                quantity = int(row["quantity"])
                product = row['product']
                revenue_per_product = price * quantity
                total_revenue += revenue_per_product

                if row["category"] == 'Electronics':
                    revenue_electronics += revenue_per_product
                else:
                    revenue_furniture += revenue_per_product
        
                if highest_sales_product is None or highest_sales < quantity:
                    highest_sales = quantity
                    highest_sales_product= product
    except(FileNotFoundError)as e:
        print("Something went wrong:", e)
        return

    print(f"Overall revenue: {total_revenue:.2f}")
    print(f"Revenue electronic: {revenue_electronics:.2f}")
    print(f"Revenue furniture: {revenue_furniture:.2f}")
    print("Highest sold product:", highest_sales_product, "with", highest_sales, "sold units")

analyze_csv()