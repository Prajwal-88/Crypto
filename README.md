# Crypto Analytics Pipeline

A data pipeline project built with Python, Flask, and MongoDB that pulls live cryptocurrency data from the CoinGecko API, processes it, and displays it on a web dashboard.

---

## What This Project Does

This pipeline fetches the top 20 cryptocurrencies from CoinGecko every time the user clicks refresh. The raw data is cleaned and transformed into meaningful features, then stored in MongoDB Atlas. A Flask web server serves the processed data to a frontend dashboard where users can explore the data through charts and a searchable table.

The main goal was to build a complete data pipeline from scratch — from raw API data all the way to a working frontend — while keeping the code clean, tested, and well documented.

---

## Features Engineered

The transformer takes raw CoinGecko data and calculates these features:

**Price Change %** — How much the price moved in the last 24 hours compared to its all time low. Useful for spotting short term movements.

**7-Day Moving Average** — The average price across a simulated 7 day window using the daily high and low. Smooths out noise and shows the overall trend direction.

**Volatility Score** — Standard deviation of the simulated price window. A higher score means the coin is more unpredictable and carries more risk.

**Volume to Market Cap Ratio** — Trading volume divided by market cap. When this is high it usually means there is strong interest or activity around that coin.

**Momentum Label** — A simple classification of Bullish, Bearish or Neutral based on the 7 day price change. Makes it easy to scan coins at a glance.

**Momentum Score** — A numerical version of momentum that combines the 7 day and 24 hour changes with a weighted formula. Gives a more precise view than the label alone.

**Fear Index** — Flags coins where the price is dropping but volume is spiking, which often indicates panic selling in the market.

---

## Tech Stack

Technology | What it is used for |
Python | Core pipeline logic and backend |
Flask | Web server and REST API |
MongoDB Atlas | Cloud database for storing coin data |
CoinGecko API | Source of live cryptocurrency data |
Pandas and Numpy | Data manipulation and calculations |
Chart.js | Interactive charts on the frontend |
Pytest | Unit and integration testing |
Python Dotenv | Managing environment variables |

## Use of AI

Data Transformation
AI helped refine and optimize some transformation logic, particularly in feature calculations such as volatility, moving averages, and momentum scoring.

Frontend Development
AI was used to assist in building and improving the frontend components, including chart integration and UI structure using Chart.js.