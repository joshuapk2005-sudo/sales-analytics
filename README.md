# Sales Analytics Dashboard

A simple Python project that loads sales data into SQLite, runs SQL queries, and displays the results in a browser using Flask and Plotly.

## Project Overview

This project demonstrates how to:
- load CSV data into a SQLite database
- query data using SQL
- calculate sales summaries and KPIs
- visualize results with Plotly
- serve the dashboard through Flask

## Tech Stack

- Python
- SQLite
- SQL
- Flask
- Plotly

## Project Structure

```text
python-sql-dashboard/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── dashboard.py
│   └── queries.py
├── data/
│   ├── sales.csv
│   └── sales.db
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── .venv/
```

## Setup

1. Open a terminal in the project folder.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Dashboard

From the project root, start the app:

```bash
python main.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Database

The app creates a SQLite database file at:

```text
data/sales.db
```

The data is loaded from:

```text
data/sales.csv
```

## Data source

This project uses a synthetic sample sales dataset stored in `data/sales.csv`. It is created for learning and portfolio purposes and is not taken from a real company or production database.

## Example SQL Queries

The project includes SQL queries for:
- total revenue by region
- top products by revenue
- monthly revenue trend
- raw sales data

## Future Improvements

Possible enhancements include:
- filters by product, region, and date
- richer KPI cards
- export to CSV/Excel
- PostgreSQL support
- authentication and user roles

## License

This project is for learning and demonstration purposes.
