from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for enabling Cross-Origin Resource Sharing
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with your own API key and endpoint
api_key = "c6ffa0cf55e747fda925c68097721e11"
endpoint = "https://t-vin34-rg-service.cognitiveservices.azure.com/"

def generate_summary(text):
    # Create a Text Analytics client
    credential = AzureKeyCredential(api_key)
    text_analytics_client = TextAnalyticsClient(endpoint, credential)

    # Explicitly specify the language as English (en)
    language_detection_result = text_analytics_client.detect_language(documents=[text], country_hint="US")
    detected_language = language_detection_result[0].primary_language.name

    # Perform sentiment analysis on the text
    sentiment_analysis_result = text_analytics_client.analyze_sentiment(documents=[text], language="en")

    # Sort sentences by sentiment score (0: negative, 1: positive)
    sorted_sentences = sorted(
        sentiment_analysis_result[0].sentences,
        key=lambda sentence: sentence.confidence_scores.positive,
        reverse=True
    )

    # Extract the sentence with the highest positive sentiment score as the summary
    if sorted_sentences:
        summary = sorted_sentences[0].text
        return summary

    return None

@app.route("/analyze", methods=["POST"])  # Update route to /analyze
def analyze_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request. 'text' field not found."}), 400

    input_text = data["text"]
    summary = generate_summary(input_text)
    print(summary)

    if summary:
        return jsonify({"summary": summary}), 200
    else:
        return jsonify({"error": "No summary could be generated."}), 500

if __name__ == "__main__":
    app.run(debug=True)
