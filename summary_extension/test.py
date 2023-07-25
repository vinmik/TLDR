from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

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

if __name__ == "__main__":
    input_text = "Dish-bearers (often called seneschals by historians) and butlers (or cup-bearers) were thegns who acted as personal attendants of kings in Anglo-Saxon England. Royal feasts played an important role in consolidating community and hierarchy among the elite, and dish-bearers and butlers served the food and drinks at these meals. Thegns were members of the aristocracy, leading landowners who occupied the third lay (non-religious) rank in English society after the king and ealdormen. Dish-bearers and butlers probably also carried out diverse military and administrative duties as required by the king. Some went on to have illustrious careers as ealdormen, but most never rose higher than thegn."

    summary = generate_summary(input_text)

    if summary:
        print("Generated Summary:")
        print(summary)
    else:
        print("No summary could be generated.")
