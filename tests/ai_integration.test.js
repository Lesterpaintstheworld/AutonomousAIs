// tests/ai_integration.test.js

const { analyzeAndDecide, comprehensiveAnalysis, tokenizeInput } = require('../src/ai_integration');
const ml = require('../src/machine_learning');
const nlp = require('../src/nlp');
const dm = require('../src/decision_making');

test('analyzeAndDecide combines NLP and ML', () => {
    const inputText = "AI is the future.";
    const mlInput = [0.5, 0.5];
    const model = {}; // Mock model
    const result = analyzeAndDecide(inputText, mlInput, model);
    
    expect(result).toHaveProperty('tokens');
    expect(result).toHaveProperty('sentiment');
    expect(result).toHaveProperty('mlPrediction');
    expect(result).toHaveProperty('decision');
});

test('comprehensiveAnalysis provides a summary', () => {
    const inputText = "AI is amazing.";
    const mlInput = [0.7, 0.3];
    const model = {}; // Mock model
    const result = comprehensiveAnalysis(inputText, mlInput, model);
    
    expect(result).toHaveProperty('summary');
});

test('tokenizeInput returns tokens', () => {
    const inputText = "Tokenize this text.";
    const tokens = tokenizeInput(inputText);
    
    expect(tokens).toBeInstanceOf(Array);
});
