const request = require('superagent');
const fs = require('fs');
const path = require('path');

const DATASET_FOLDER = path.join(__dirname, './datasets'); // Folder where our gathered data will sit
const BASE_URL = 'https://www.reddit.com/r/stocks/hot/.json'; // Reddit API base url
const FILENAME = 'data.json'; // Filename for the data
const FILENAME_ERROR = 'data_error.json'; // Filename for when something goes wrong and we want to save our progress
const DATASET_SIZE = 10000; // How many posts we want in total
const PAGE_SIZE = 100; // How many posts we would like per API call
const G = 'GLOBAL'; // Region

const getPage = async (after) => {
  const response = await request.get(BASE_URL).query({ g: G, limit: PAGE_SIZE, after }); // Get the actual response from the Reddit API
  const posts = response.body.data.children;
  const newAfter = response.body.data.after;
  return [newAfter, posts];
};

const saveData = (filePath, data) => {
  fs.writeFileSync(filePath, JSON.stringify(data));
};

const sleep = async (time) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve();
    }, time);
  });
};

const start = async () => {
  let data = []; // Buffer for all our posts
  let after = null; // The Reddit API uses this as a 'this is the last post I've seen'
  try {
    while (data.length < DATASET_SIZE) {
      const limit = (DATASET_SIZE - data.length) % PAGE_SIZE; // Make sure we don't go over our DATASET_SIZE, in case API does not always return 100 posts
      const [newAfter, newData] = await getPage(after, limit);
      after = newAfter;
      data = data.concat(newData);
      console.info(`${Math.floor((data.length / DATASET_SIZE) * 100)}%`);
      await sleep(2 * 1000); // Avoid Reddit rate limit
    }
    saveData(`${DATASET_FOLDER}/${FILENAME}`, data);
  } catch (error) {
    console.error(`Error while generating data\nCollected ${data.length} posts\nError:\n${error}`);
    saveData(`${DATASET_FOLDER}/${FILENAME_ERROR}`, data); // Save data in case of error, but with a different filename
  }
};

start();
