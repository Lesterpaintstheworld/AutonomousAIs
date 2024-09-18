// src/entity_recognition.js

/**
 * Recognizes common AI-related terms in the input text.
 * @param {string} text - The input text to analyze.
 * @returns {Array} List of recognized AI-related terms.
 */
function recognizeEntities(text) {
    const aiTerms = ['AI', 'machine learning', 'deep learning', 'neural network', 'NLP', 'algorithm'];
    const recognized = aiTerms.filter(term => text.includes(term));
    return recognized;
}

module.exports = {
    recognizeEntities,
};
