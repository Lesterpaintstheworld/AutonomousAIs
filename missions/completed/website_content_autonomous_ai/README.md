# Core AI Engine Module

## Usage Example

To use the NLP component, you can import the functions as follows:

```javascript
const { tokenize, analyzeSentiment, recognizeEntities } = require('./src/nlp');

const text = 'I love programming with AI and machine learning!';
const tokens = tokenize(text);
console.log(tokens); // Output: ['I', 'love', 'programming', 'with', 'AI', 'and', 'machine', 'learning', '!']

const sentiment = analyzeSentiment(text);
console.log(sentiment); // Output: Positive sentiment score

const entities = recognizeEntities(text);
console.log(entities); // Output: ['AI', 'machine']
```
