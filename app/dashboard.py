from flask import Flask, render_template_string, request
import plotly.graph_objects as go

from app.database import init_db
from app.queries import (
    fetch_sales_data,
    get_monthly_summary,
    get_region_summary,
    get_top_products,
)

app = Flask(__name__)


@app.route("/")
def index():
    init_db()

    selected_region = request.args.get("region", "")
    selected_product = request.args.get("product", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    all_sales_data = fetch_sales_data()
    sales_data = fetch_sales_data(
        region=selected_region or None,
        product=selected_product or None,
        start_date=start_date or None,
        end_date=end_date or None,
    )
    region_summary = get_region_summary(
        region=selected_region or None,
        product=selected_product or None,
        start_date=start_date or None,
        end_date=end_date or None,
    )
    product_summary = get_top_products(
        region=selected_region or None,
        product=selected_product or None,
        start_date=start_date or None,
        end_date=end_date or None,
    )
    monthly_summary = get_monthly_summary(
        region=selected_region or None,
        product=selected_product or None,
        start_date=start_date or None,
        end_date=end_date or None,
    )

    regions = sorted({row["region"] for row in all_sales_data})
    products = sorted({row["product"] for row in all_sales_data})

    total_revenue = sum(float(row["revenue"]) for row in sales_data)
    total_units = sum(int(row["units"]) for row in sales_data)
    avg_revenue = total_revenue / len(sales_data) if sales_data else 0

    total_revenue_label = f"$ {total_revenue:,.0f}"
    total_units_label = f"{total_units:,}"
    avg_revenue_label = f"$ {avg_revenue:,.0f}"

    if region_summary:
        region_fig = go.Figure(
            data=[
                go.Bar(
                    x=[item["region"] for item in region_summary],
                    y=[float(item["revenue"]) for item in region_summary],
                    marker_color="#4F46E5",
                )
            ]
        )
    else:
        region_fig = go.Figure()
        region_fig.add_annotation(text="No matching data", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
    region_fig.update_layout(title="Revenue by Region", template="plotly_white", paper_bgcolor="white", plot_bgcolor="white")

    if product_summary:
        product_fig = go.Figure(
            data=[
                go.Bar(
                    x=[item["product"] for item in product_summary],
                    y=[float(item["revenue"]) for item in product_summary],
                    marker_color="#10B981",
                )
            ]
        )
    else:
        product_fig = go.Figure()
        product_fig.add_annotation(text="No matching data", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
    product_fig.update_layout(title="Top Products by Revenue", template="plotly_white", paper_bgcolor="white", plot_bgcolor="white")

    if monthly_summary:
        monthly_fig = go.Figure(
            data=[
                go.Scatter(
                    x=[item["month"] for item in monthly_summary],
                    y=[float(item["revenue"]) for item in monthly_summary],
                    mode="lines+markers",
                    line={"color": "#F59E0B", "width": 3},
                    marker={"size": 8},
                )
            ]
        )
    else:
        monthly_fig = go.Figure()
        monthly_fig.add_annotation(text="No matching data", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False)
    monthly_fig.update_layout(title="Monthly Revenue Trend", template="plotly_white", paper_bgcolor="white", plot_bgcolor="white")

    region_html = region_fig.to_html(full_html=False)
    product_html = product_fig.to_html(full_html=False)
    monthly_html = monthly_fig.to_html(full_html=False)

    return render_template_string(
        """
        <!doctype html>
        <html>
        <head>
            <title>Sales Dashboard</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    background: #f3f4f6;
                    color: #111827;
                }
                .container {
                    max-width: 1200px;
                    margin: 30px auto;
                    padding: 0 20px 30px;
                }
                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 24px;
                    gap: 20px;
                }
                h1 {
                    margin: 0;
                    font-size: 2.2rem;
                }
                .filters {
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 14px;
                    padding: 18px;
                    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
                    margin-bottom: 24px;
                }
                .filter-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 14px;
                    align-items: end;
                }
                .field {
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                    font-size: 0.92rem;
                    color: #374151;
                }
                .field input, .field select {
                    border: 1px solid #d1d5db;
                    border-radius: 10px;
                    padding: 10px 12px;
                    font-size: 0.96rem;
                    background: white;
                }
                .actions {
                    display: flex;
                    gap: 10px;
                    justify-content: flex-end;
                    margin-top: 14px;
                }
                button {
                    border: none;
                    border-radius: 10px;
                    padding: 10px 16px;
                    cursor: pointer;
                    font-size: 0.95rem;
                }
                .btn-primary {
                    background: #111827;
                    color: white;
                }
                .btn-secondary {
                    background: #e5e7eb;
                    color: #111827;
                }
                .kpis {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 18px;
                    margin-bottom: 24px;
                }
                .card {
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 14px;
                    padding: 18px 20px;
                    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
                }
                .card-label {
                    color: #6b7280;
                    font-size: 0.84rem;
                    margin-bottom: 10px;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                .card-value {
                    font-size: 2rem;
                    font-weight: 700;
                    margin: 0;
                }
                .charts {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                    gap: 18px;
                    margin-bottom: 24px;
                }
                .chart-card {
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 14px;
                    padding: 10px;
                    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
                }
                th, td {
                    padding: 12px 14px;
                    border-bottom: 1px solid #e5e7eb;
                    text-align: left;
                }
                th {
                    background: #f9fafb;
                    color: #374151;
                }
                .empty {
                    padding: 18px;
                    color: #6b7280;
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 12px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Sales Analytics Dashboard</h1>
                </div>

                <div class="filters">
                    <form method="get">
                        <div class="filter-grid">
                            <div class="field">
                                <label for="region">Region</label>
                                <select id="region" name="region">
                                    <option value="">All regions</option>
                                    {% for item in regions %}
                                        <option value="{{ item }}" {% if item == selected_region %}selected{% endif %}>{{ item }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="field">
                                <label for="product">Product</label>
                                <select id="product" name="product">
                                    <option value="">All products</option>
                                    {% for item in products %}
                                        <option value="{{ item }}" {% if item == selected_product %}selected{% endif %}>{{ item }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="field">
                                <label for="start_date">Start date</label>
                                <input id="start_date" name="start_date" type="date" value="{{ selected_start_date }}">
                            </div>
                            <div class="field">
                                <label for="end_date">End date</label>
                                <input id="end_date" name="end_date" type="date" value="{{ selected_end_date }}">
                            </div>
                        </div>
                        <div class="actions">
                            <button class="btn-secondary" type="reset" onclick="window.location.href='/'">Reset</button>
                            <button class="btn-primary" type="submit">Apply filters</button>
                        </div>
                    </form>
                </div>

                <div class="kpis">
                    <div class="card">
                        <div class="card-label">Total Revenue</div>
                        <p class="card-value">{{ total_revenue_label }}</p>
                    </div>
                    <div class="card">
                        <div class="card-label">Units Sold</div>
                        <p class="card-value">{{ total_units_label }}</p>
                    </div>
                    <div class="card">
                        <div class="card-label">Avg. Revenue / Order</div>
                        <p class="card-value">{{ avg_revenue_label }}</p>
                    </div>
                </div>

                <div class="charts">
                    <div class="chart-card">{{ region_html | safe }}</div>
                    <div class="chart-card">{{ monthly_html | safe }}</div>
                    <div class="chart-card" style="grid-column: 1 / -1;">{{ product_html | safe }}</div>
                </div>

                {% if sales_data %}
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Region</th>
                            <th>Product</th>
                            <th>Category</th>
                            <th>Units</th>
                            <th>Price</th>
                            <th>Revenue</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in sales_data[:15] %}
                        <tr>
                            <td>{{ row.order_date }}</td>
                            <td>{{ row.region }}</td>
                            <td>{{ row.product }}</td>
                            <td>{{ row.category }}</td>
                            <td>{{ row.units }}</td>
                            <td>$ {{ row.price }}</td>
                            <td>$ {{ row.revenue }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="empty">No data matches the selected filters.</div>
                {% endif %}
            </div>
        </body>
        </html>
        """,
        regions=regions,
        products=products,
        selected_region=selected_region,
        selected_product=selected_product,
        selected_start_date=start_date,
        selected_end_date=end_date,
        total_revenue_label=total_revenue_label,
        total_units_label=total_units_label,
        avg_revenue_label=avg_revenue_label,
        region_html=region_html,
        monthly_html=monthly_html,
        product_html=product_html,
        sales_data=sales_data,
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
