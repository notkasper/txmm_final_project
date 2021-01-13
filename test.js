const weekly = require('./weekly_ticker_sentiments.json');

Object.keys(weekly).forEach((week_key) => {
  const scores = weekly[week_key];
  Object.keys(scores).forEach((ticker) => {
    sentiment = scores[ticker];
    if (sentiment.pos > 0.1) {
      console.log(`week: ${week_key}, ${ticker}`);
    }
  });
});
