from fastapi import FastAPI, Query

app = FastAPI()

# -----------------------------
# Dummy Data
# -----------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []
order_counter = 1


# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def home():
    return {"message": "Welcome to app 🚀"}


# -----------------------------
# CREATE ORDER
# -----------------------------
@app.post("/orders")
def create_order(customer_name: str):
    global order_counter

    new_order = {
        "order_id": order_counter,
        "customer_name": customer_name
    }

    orders.append(new_order)
    order_counter += 1

    return {"message": "Order created", "order": new_order}


# -----------------------------
# GET ALL PRODUCTS
# -----------------------------
@app.get("/products")
def get_products():
    return {"products": products}


# -----------------------------
# SEARCH PRODUCTS
# -----------------------------
@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    result = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }


# -----------------------------
# SORT PRODUCTS
# -----------------------------
@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    result = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=(order == "desc")
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": result
    }


# -----------------------------
# PAGINATION
# -----------------------------
@app.get("/products/page")
def paginate_products(
    page: int = Query(1, ge=1),
    limit: int = Query(2, ge=1)
):
    start = (page - 1) * limit
    total = len(products)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "products": products[start:start + limit]
    }


# -----------------------------
# Q4: SEARCH ORDERS
# -----------------------------
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# -----------------------------
# Q5: SORT BY CATEGORY + PRICE
# -----------------------------
@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(products, key=lambda p: (p["category"], p["price"]))

    return {
        "products": result,
        "total": len(result)
    }


# -----------------------------
# Q6: SEARCH + SORT + PAGINATE
# -----------------------------
@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20)
):
    result = products

    # 🔍 Search
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # ↕ Sort
    if sort_by in ["price", "name"]:
        result = sorted(
            result,
            key=lambda p: p[sort_by],
            reverse=(order == "desc")
        )

    # 📄 Pagination
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }


# -----------------------------
# BONUS: ORDERS PAGINATION
# -----------------------------
@app.get("/orders/page")
def paginate_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20)
):
    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total": len(orders),
        "total_pages": -(-len(orders) // limit),
        "orders": orders[start:start + limit]
    }


# -----------------------------
# GET PRODUCT BY ID (keep last)
# -----------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p

    return {"error": "Product not found"}
