const fs = require('fs');
const path = require('path');
const { saveData } = require('./_utils');

const DATASET_FOLDER = path.join(__dirname, './datasets');
const POSTS_FILENAME = 'pusshift_test.json';
const OUTPUT_FILENAME = 'binned_data.json';
const UNIX_DAY_LENGTH = 86400;

const findEarliestDateUnix = (posts) => {
  let earliestDateUnix = Number.MAX_SAFE_INTEGER;
  posts.forEach((post) => {
    if (post.created_utc < earliestDateUnix) {
      earliestDateUnix = post.created_utc;
    }
  });
  return earliestDateUnix;
};

const readPosts = () => JSON.parse(fs.readFileSync(`${DATASET_FOLDER}/${POSTS_FILENAME}`));

const roundUnixToStartOfDay = (unixDate) => {
  const date = new Date(unixDate * 1000);
  date.setHours(0);
  date.setMinutes(0);
  date.setSeconds(0);
  date.setMilliseconds(0);
  return date.getTime() / 1000;
};

const bin = (posts) => {
  const bins = {};
  posts.forEach((post) => {
    const binIndex = new Date(post.created_utc * 1000).getDate();
    if (!bins[binIndex]) {
      bins[binIndex] = [];
    }
    bins[binIndex].push(post);
  });
  return bins;
};

const start = async () => {
  const posts = readPosts();
  let earliestDateUnix = findEarliestDateUnix(posts);
  earliestDateUnix = roundUnixToStartOfDay(earliestDateUnix);
  const binSize = UNIX_DAY_LENGTH;
  const bins = bin(posts);
  Object.values(bins).forEach((bin) => console.log(bin.length));
  saveData(`${DATASET_FOLDER}/${OUTPUT_FILENAME}`, bins);
};

start();
