const path = require('path');
const request = require('superagent');
const { saveData } = require('./_utils');

const DATASET_FOLDER = path.join(__dirname, './datasets'); // Folder where our gathered data will sit
const FILENAME = 'pusshift_test.json'; // Filename for the data
const DATASET_SIZE = 1000;
const PAGE_SIZE = 100;
const BASE_URL = 'https://api.pushshift.io/reddit/search/submission';
const UNIX_DAY_LENGTH = 86400;

const roundUnixToStartOfDay = (unixDate) => {
  const date = new Date(unixDate * 1000);
  date.setHours(0);
  date.setMinutes(0);
  date.setSeconds(0);
  date.setMilliseconds(0);
  return date.getTime() / 1000;
};

const getPage = async (after, before) => {
  console.log('new request started...');
  const res = await request.get(BASE_URL).query({
    after,
    before: 1609196553,
    limit: PAGE_SIZE,
    // sort_type: 'created_utc',
    // sort: 'desc',
    subreddit: 'stocks',
  });
  const posts = res.body.data;
  return posts;
};

const getAllPostsWithinTimeframe = async (after, before) => {
  let lastUTC = after;
  let posts = [];
  while (posts.length < DATASET_SIZE) {
    try {
      const newPosts = await getPage(lastUTC, lastUTC);
      console.log(newPosts.length);
      lastUTC = newPosts[newPosts.length - 1].created_utc;
      posts = posts.concat(newPosts);
    } catch (error) {
      console.error(error);
    }
    console.log(`Collected ${posts.length} posts`);
    console.log(`last post: ${new Date(lastUTC * 1000)}`);
  }
  return posts;
};

const getPostsInDay = async (utc) => {
  const after = roundUnixToStartOfDay(utc);
  const before = after + UNIX_DAY_LENGTH;
  const posts = getAllPostsWithinTimeframe(after, before);
  return posts;
};

const start = async () => {
  const after = 1577836800;
  const posts = await getPostsInDay(after);
  saveData(`${DATASET_FOLDER}/${FILENAME}`, posts);
};

start();
