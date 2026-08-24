from app.database import get_connection


def fetch_sales_data():
    query = """
        SELECT order_date, region, product, category, units, price,
               (units * price) AS revenue
        FROM sales
        ORDER BY order_date ASC
    """
    conn = get_connection()
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_region_summary():
    query = """
        SELECT region, SUM(units * price) AS revenue
        FROM sales
        GROUP BY region
        ORDER BY revenue DESC
    """
    conn = get_connection()
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_monthly_summary():
    query = """
        SELECT substr(order_date, 1, 7) AS month,
               SUM(units * price) AS revenue
        FROM sales
        GROUP BY substr(order_date, 1, 7)
        ORDER BY month ASC
    """
    conn = get_connection()
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_top_products():
    query = """
        SELECT product, SUM(units * price) AS revenue, SUM(units) AS units_sold
        FROM sales
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT 5
    """
    conn = get_connection()
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]
