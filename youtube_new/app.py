from flask import Flask, request, jsonify,render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import joblib

app = Flask(__name__)




# Load the 'vaderSentiment' model
model = joblib.load("D:/youtube_new/youtube.joblib")

@app.route("/")
def home():
    return render_template("comment.html")
app.static_folder = 'static'

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data["comment"]

    # Sentiment analysis using 'vaderSentiment'
    sentiment = SentimentIntensityAnalyzer()
    result = sentiment.polarity_scores(text)

    if result['pos'] >= 0.5:
        prediction = "The comment is good"
    elif result['neu'] >= 0.5:
        prediction = "The comment is neutral"
    else:
        prediction = "The comment is bad"

    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    app.run(debug=True)
