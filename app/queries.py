from app.database import get_connection


def _build_filters(region=None, product=None, start_date=None, end_date=None):
    conditions = []
    params = []

    if region:
        conditions.append("region = ?")
        params.append(region)

    if product:
        conditions.append("product = ?")
        params.append(product)

    if start_date:
        conditions.append("order_date >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("order_date <= ?")
        params.append(end_date)

    return conditions, params


def fetch_sales_data(region=None, product=None, start_date=None, end_date=None):
    conditions, params = _build_filters(region, product, start_date, end_date)
    query = """
        SELECT order_date, region, product, category, units, price,
               (units * price) AS revenue
        FROM sales
    """
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY order_date ASC"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_region_summary(region=None, product=None, start_date=None, end_date=None):
    conditions, params = _build_filters(region, product, start_date, end_date)
    query = """
        SELECT region, SUM(units * price) AS revenue
        FROM sales
    """
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY region ORDER BY revenue DESC"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_monthly_summary(region=None, product=None, start_date=None, end_date=None):
    conditions, params = _build_filters(region, product, start_date, end_date)
    query = """
        SELECT substr(order_date, 1, 7) AS month,
               SUM(units * price) AS revenue
        FROM sales
    """
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY substr(order_date, 1, 7) ORDER BY month ASC"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_top_products(region=None, product=None, start_date=None, end_date=None):
    conditions, params = _build_filters(region, product, start_date, end_date)
    query = """
        SELECT product, SUM(units * price) AS revenue, SUM(units) AS units_sold
        FROM sales
    """
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY product ORDER BY revenue DESC LIMIT 5"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]
