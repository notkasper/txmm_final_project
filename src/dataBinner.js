const fs = require('fs');
const path = require('path');
const { saveData } = require('./_utils');

const DATASET_FOLDER = path.join(__dirname, './datasets');
const POSTS_FILENAME = 'data.json';
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

const bin = (posts, startTimeUnix, binSize) => {
  const bins = {};
  posts.forEach((post) => {
    const binIndex = Math.floor((post.created_utc - startTimeUnix) / binSize);
    if (!bins[binIndex]) {
      bins[binIndex] = [];
    }
    bins[binIndex].push(post);
  });
  return bins;
};

const start = async () => {
  const posts = readPosts();

  uniqueDays = [];
  posts.forEach((post) => {
    const date = new Date(post.created_utc * 1000);
    const str = `${date.getDay()}-${date.getMonth()}-${date.getFullYear()}`;
    if (!uniqueDays.includes(str)) {
      uniqueDays.push(str);
    }
  });
  console.log(uniqueDays);

  let earliestDateUnix = findEarliestDateUnix(posts);
  earliestDateUnix = roundUnixToStartOfDay(earliestDateUnix);
  const binSize = UNIX_DAY_LENGTH;
  const bins = bin(posts, earliestDateUnix, binSize);
  Object.values(bins).forEach((bin) => console.log(bin.length));
  saveData(`${DATASET_FOLDER}/${OUTPUT_FILENAME}`, bins);
};

start();
