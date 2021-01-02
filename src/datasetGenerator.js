const path = require("path");
const request = require("superagent");
const _ = require("lodash");
const ora = require("ora");
const fs = require("fs");

const DAYS = 2;
const PAGE_SIZE = 100;
const START_DATE_UTC = 1577836800;
const DAY_LENGTH_UTC = 86400;
const BASE_URL = "https://api.pushshift.io/reddit/search/submission";
const OUTPUT = path.join(__dirname, "./stock_posts.json");
const PROPS = [
  "selftext",
  "title",
  "upvote_ratio",
  "ups",
  "total_awards_received",
  "score",
  "created",
  "num_comments",
  "created_utc",
];

const saveData = (filePath, data) => {
  fs.writeFileSync(filePath, JSON.stringify(data));
};

const sleep = (time) =>
  new Promise((resolve) =>
    setTimeout(() => {
      resolve();
    }, time)
  );

const getPostsAfter = async (after, before) => {
  const res = await request.get(BASE_URL).query({
    after,
    before,
    limit: PAGE_SIZE,
    subreddit: "stocks",
  });
  const posts = res.body.data.map((post) => _.pick(post, PROPS));
  return posts;
};

const countPosts = (buffer) =>
  Object.values(buffer).reduce((acc, curr) => {
    return (acc += curr.length);
  }, 0);

const generateDataset = async () => {
  const spinner = ora("Initializing script...").start();
  const buffer = {};
  for (let i = 0; i < DAYS; i++) {
    const after = START_DATE_UTC + i * DAY_LENGTH_UTC;
    const before = after + DAY_LENGTH_UTC;
    spinner.text = `Total posts: ${countPosts(
      buffer
    )}. Status: awaiting response...`;
    const posts = await getPostsAfter(after, before);
    const date = new Date(after * 1000);
    const key = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
    buffer[key] = posts;
    spinner.text = `Total posts: ${countPosts(
      buffer
    )}. Status: starting new request...`;
    await sleep(500);
  }
  spinner.text = `Total posts: ${countPosts(buffer)}. Status: saving posts...`;
  saveData(OUTPUT, buffer);
  await sleep(500);
  spinner.stop();
};

generateDataset();
