const fs = require("fs");

const tickers = JSON.parse(fs.readFileSync("./tickers.json"));

let sorted = [];
tickers.forEach((ticker) => {
  const posts = JSON.parse(fs.readFileSync(`./data/${ticker}.json`)).length;
  if (posts > 150) sorted.push({ ticker, posts });
});

console.log(sorted.length);
