const { tokenize, analyzeSentiment } = require('../src/nlp');

describe('NLP Functions', () => {
  test('Tokenization works correctly', () => {
    const text = 'Hello world!';
    const tokens = tokenize(text);
    expect(tokens).toEqual(['Hello', 'world', '!']);
  });

  test('Sentiment analysis works correctly', () => {
    const text = 'I love programming!';
    const sentiment = analyzeSentiment(text);
    expect(sentiment).toBeGreaterThan(0); // Expect positive sentiment
  });
});
