// src/ai_integration.js

const nlp = require('./nlp');
const ml = require('./machine_learning');
const dm = require('./decision_making');

/**
 * Analyzes text input and makes a decision based on sentiment and ML prediction.
 * @param {string} text - The input text to analyze.
 * @param {number[]} mlInput - Additional input data for ML prediction.
 * @param {Object} model - Trained ML model.
 * @returns {Object} Analysis result and decision.
 */
function analyzeAndDecide(text, mlInput, model) {
  if (!text || !mlInput || !model) {
    throw new Error('Missing required parameters');
  }

  const tokens = nlp.tokenize(text);
  const sentiment = nlp.analyzeSentiment(text);
  const mlPrediction = ml.predict(model, mlInput);
  const decision = dm.probabilisticDecision(text, mlInput, model);

  return {
    tokens,
    sentiment,
    mlPrediction,
    decision
  };
}

/**
 * Combines sentiment analysis and ML prediction for a comprehensive analysis.
 * @param {string} text - The input text to analyze.
 * @param {number[]} mlInput - Additional input data for ML prediction.
 * @param {Object} model - Trained ML model.
 * @returns {Object} Combined analysis result.
 */
function comprehensiveAnalysis(text, mlInput, model) {
  const analysis = analyzeAndDecide(text, mlInput, model);
  return {
    ...analysis,
    summary: `Sentiment: ${analysis.sentiment}, Prediction: ${analysis.mlPrediction}`
  };
}

/**
 * Tokenizes input text and returns the tokens.
 * @param {string} text - The input text to tokenize.
 * @returns {Array} List of tokens.
 */
function tokenizeInput(text) {
  return nlp.tokenize(text);
}

module.exports = {
  analyzeAndDecide,
  comprehensiveAnalysis,
  tokenizeInput,
};
