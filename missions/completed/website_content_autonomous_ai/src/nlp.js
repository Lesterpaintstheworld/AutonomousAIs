const natural = require('natural');

/**
 * Tokenizes the input text into an array of words.
 * @param {string} text - The input text to tokenize.
 * @returns {string[]} An array of tokens.
 */
function tokenize(text) {
  return natural.WordTokenizer().tokenize(text);
}

/**
 * Performs sentiment analysis on the input text.
 * @param {string} text - The input text to analyze.
 * @returns {Object} An object containing the sentiment score.
 */
function analyzeSentiment(text) {
  const analyzer = new natural.SentimentAnalyzer('English', natural.PorterStemmer, 'afinn');
  const tokens = tokenize(text);
  return analyzer.getSentiment(tokens);
}

/**
 * Recognizes entities in the input text.
 * @param {string} text - The input text to analyze for entities.
 * @returns {Array} An array of recognized entities.
 */
function recognizeEntities(text) {
  const tokenizer = new natural.WordTokenizer();
  const tokens = tokenizer.tokenize(text);
  // For simplicity, let's assume we are looking for specific AI-related terms
  const aiTerms = ['AI', 'machine learning', 'neural network', 'deep learning', 'algorithm'];
  return tokens.filter(token => aiTerms.includes(token));
}

module.exports = {
  tokenize,
  analyzeSentiment,
  recognizeEntities,
  // Add more NLP functions as we implement them
};
