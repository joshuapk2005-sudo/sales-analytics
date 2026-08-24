from flask import Flask, render_template_string
import plotly.graph_objects as go

from app.database import init_db
from app.queries import fetch_sales_data, get_region_summary, get_top_products

app = Flask(__name__)


@app.route("/")
def index():
    init_db()
    sales_data = fetch_sales_data()
    region_summary = get_region_summary()
    product_summary = get_top_products()

    total_revenue = sum(float(row["revenue"]) for row in sales_data)
    total_units = sum(int(row["units"]) for row in sales_data)
    avg_revenue = total_revenue / len(sales_data) if sales_data else 0
    total_revenue_label = f"$ {total_revenue:,.0f}"
    total_units_label = f"{total_units:,}"
    avg_revenue_label = f"$ {avg_revenue:,.0f}"

    region_fig = go.Figure(data=[go.Bar(x=[item["region"] for item in region_summary], y=[float(item["revenue"]) for item in region_summary])])
    region_fig.update_layout(title="Revenue by Region", template="plotly_white")

    product_fig = go.Figure(data=[go.Bar(x=[item["product"] for item in product_summary], y=[float(item["revenue"]) for item in product_summary])])
    product_fig.update_layout(title="Top Products by Revenue", template="plotly_white")

    region_html = region_fig.to_html(full_html=False)
    product_html = product_fig.to_html(full_html=False)

    return render_template_string(
        """
        <!doctype html>
        <html>
        <head>
            <title>Sales Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 30px; background: #f5f7fb; }
                .container { max-width: 1100px; margin: auto; }
                .kpis { display: flex; gap: 20px; margin-bottom: 20px; }
                .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); flex: 1; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; }
                th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
                h2 { margin-top: 30px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Sales Analytics Dashboard</h1>
                <div class="kpis">
                    <div class="card"><strong>Total Revenue</strong><br><h3>{{ total_revenue_label }}</h3></div>
                    <div class="card"><strong>Total Units</strong><br><h3>{{ total_units_label }}</h3></div>
                    <div class="card"><strong>Average Revenue / Order</strong><br><h3>{{ avg_revenue_label }}</h3></div>
                </div>

                <div>{{ region_html | safe }}</div>
                <div>{{ product_html | safe }}</div>

                <h2>SQL Summary</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Region</th>
                            <th>Revenue</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in region_summary %}
                        <tr>
                            <td>{{ item.region }}</td>
                            <td>$ {{ item.revenue }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>

                <h2>Sales Data</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Region</th>
                            <th>Product</th>
                            <th>Units</th>
                            <th>Revenue</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in sales_data[:15] %}
                        <tr>
                            <td>{{ row.order_date }}</td>
                            <td>{{ row.region }}</td>
                            <td>{{ row.product }}</td>
                            <td>{{ row.units }}</td>
                            <td>$ {{ row.revenue }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """,
        total_revenue_label=total_revenue_label,
        total_units_label=total_units_label,
        avg_revenue_label=avg_revenue_label,
        region_html=region_html,
        product_html=product_html,
        region_summary=region_summary,
        sales_data=sales_data,
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
