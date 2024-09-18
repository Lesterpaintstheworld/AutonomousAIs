// tests/entity_recognition.test.js

const { recognizeEntities } = require('../src/entity_recognition');

test('Recognizes AI-related terms', () => {
    const inputText = "AI and machine learning are transforming industries.";
    const expectedOutput = ['AI', 'machine learning'];
    expect(recognizeEntities(inputText)).toEqual(expectedOutput);
});

test('Returns empty array for no recognized terms', () => {
    const inputText = "This text does not contain any relevant terms.";
    expect(recognizeEntities(inputText)).toEqual([]);
});
