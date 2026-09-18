# Crypto-Forex Time-Series Data Ingestion Engine

## 📌 Project Overview
A serverless, automated ETL (Extract, Transform, Load) pipeline designed to ingest real-time cryptocurrency metrics and cross-reference them with live foreign exchange (Forex) rates. This engine autonomously builds a continuous time-series database, tracking market volatility for the top 60 cryptocurrencies and generating analytics-ready data for downstream business intelligence tools.

## 🏗️ Architecture & Tech Stack
* **Data Extraction (APIs):** CoinGecko API (Crypto), ExchangeRate-API (Forex)
* **Data Transformation:** Python, Pandas
* **Database & Storage:** SQLite (`crypto_historical_data.db`)
* **Cloud Orchestration & CI/CD:** GitHub Actions

## ⚙️ The ETL Pipeline Workflow
* **Extract:** Python scripts call REST APIs to fetch current USD prices for the top 60 cryptocurrencies by market cap, alongside the live USD-to-INR fiat exchange rate.
* **Transform:**
  * Parses and flattens nested JSON responses using Pandas.
  * Dynamically calculates the INR value for each asset based on the live Forex rate.
  * Appends a precise `pipeline_run_time` timestamp to each batch to convert static snapshots into a continuous time-series log.
* **Load:** Appends the transformed DataFrame into the `market_data` table within a centralized SQLite database.

## 🤖 Serverless Automation
This pipeline requires no manual intervention or dedicated server hosting.
* **GitHub Actions Integration:** A custom YAML workflow provisions a temporary Ubuntu cloud runner, installs dependencies, executes the Python ETL script, and securely commits the updated `.db` file back to the repository.
* **Continuous Logging:** Because the script uses an `if_exists='append'` loading strategy, every automated run stacks new rows, creating a deep historical log of market fluctuations.

## 🗄️ Database Schema
The pipeline writes to a SQLite table named `market_data` structured as follows:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | TEXT | The unique identifier for the cryptocurrency (e.g., bitcoin) |
| `symbol` | TEXT | The ticker symbol (e.g., btc) |
| `price_usd` | REAL | Live price in US Dollars |
| `price_inr` | REAL | Dynamically calculated price in Indian Rupees |
| `pipeline_run_time` | TIMESTAMP | The exact UTC execution time of the ETL batch |

## 📊 Downstream Use Cases
The resulting `crypto_historical_data.db` is structured as a relational database, making it immediately ready for:
* **Advanced SQL Analytics:** Querying historical max/min prices using Window Functions and CTEs.
* **Business Intelligence:** Direct integration into Power BI or Tableau to build live dashboards visualizing price trends, market rank shifts, and fiat conversion impacts.
