const axios = require('axios');

const subscriptionKey = 'c6ffa0cf55e747fda925c68097721e11'; // Replace this with your Azure Text Analytics API key
const endpoint = 'https://eastus.api.cognitive.microsoft.com/text/analytics/v3.2-preview.1/analyze';

const textToSummarize = 'This is a long piece of text that needs to be summarized. It is important to extract the key points from this text.';

async function getSummarization() {
  try {
    const response = await axios.post(endpoint, {
      documents: [
        {
          language: 'en',
          id: '1',
          text: textToSummarize,
        },
      ],
      tasks: ['extractiveSummarization'],
    }, {
      headers: {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
      },
    });

    const summarizedText = response.data.documents[0].tasks.extractiveSummarization[0].sentences;
    console.log('Summarized Text:');
    summarizedText.forEach((sentence, index) => {
      console.log(`${index + 1}. ${sentence}`);
    });
  } catch (error) {
    console.error('Error:', error.message);
  }
}

getSummarization();
