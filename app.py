
from flask import Flask, jsonify, render_template
from pipeline.fetcher import fetch_coins
from pipeline.transformer import transform_all
from pipeline.loader import save_raw_coins, save_processed_coins, get_processed_coins, get_coin_by_id
from dotenv import load_dotenv
import traceback

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    """
    Serve the main dashboard page
    """
    return render_template("index.html")


@app.route("/api/coins", methods=["GET"])
def get_coins():
    """
    Return all processed coins from MongoDB as JSON
    """
    try:
        coins = get_processed_coins()
        return jsonify({"status": "success", "data": coins})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/refresh", methods=["POST"])
def refresh():
    """
    Fetch fresh data from CoinGecko, transform and save to MongoDB
    """
    try:
        # Step 1: Fetch raw data
        raw_coins = fetch_coins()

        if not raw_coins:
            return jsonify({"status": "error", "message": "No data from CoinGecko"}), 500

        # Step 2: Save raw data
        save_raw_coins(raw_coins)

        # Step 3: Transform data
        transformed = transform_all(raw_coins)

        # Step 4: Save processed data
        save_processed_coins(transformed)

        return jsonify({
            "status": "success",
            "message": f"Pipeline complete! {len(transformed)} coins updated"
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

    except ConnectionError:
        return jsonify({
            "status": "error",
            "message": "No internet connection please check your network"
        }), 500
    
    except TimeoutError:
        return jsonify({
            "status": "error",
            "message": "Request timed out CoinGecko took too long to respond"
        }), 500


@app.route("/api/coin/<coin_id>", methods=["GET"])
def get_coin(coin_id):
    """
    Return a single coin by its id
    """
    try:
        coin = get_coin_by_id(coin_id)
        if not coin:
            return jsonify({"status": "error", "message": "Coin not found"}), 404
        return jsonify({"status": "success", "data": coin})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=8080)