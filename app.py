from flask import Flask, render_template, jsonify
from scrape_twitter import scrape_twitter

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_script", methods=["GET"])
def run_script():
    result = scrape_twitter()
    if result:
        # Ensure inserted_id is converted to a string if present
        if "_id" in result:
            result["_id"] = str(result["_id"])

        # Extract only the topic names for the trends
        topic_names = [trend["topic_name"] for trend in result["trends"][:5]]

        return jsonify({
            "message": f"These are the most happening topics as on {result['date_time']}",
            "topics": topic_names,
            "proxy": result["proxy"],
            "json_extract": result,
        })
    else:
        return jsonify({"error": "Failed to scrape trending topics."})

if __name__ == "__main__":
    app.run(debug=True)
