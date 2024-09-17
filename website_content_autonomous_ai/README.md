# Core AI Engine Module

## Usage Example

To use the NLP component, you can import the functions as follows:

```javascript
const { tokenize, analyzeSentiment } = require('./src/nlp');

const text = 'I love programming!';
const tokens = tokenize(text);
console.log(tokens); // Output: ['I', 'love', 'programming', '!']

const sentiment = analyzeSentiment(text);
console.log(sentiment); // Output: Positive sentiment score
```
