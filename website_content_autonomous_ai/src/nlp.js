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

module.exports = {
  tokenize,
  analyzeSentiment,
  // Add more NLP functions as we implement them
};
