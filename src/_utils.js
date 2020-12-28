const fs = require('fs');

const sleep = async (time) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve();
    }, time);
  });
};

const saveData = (filePath, data) => {
  fs.writeFileSync(filePath, JSON.stringify(data));
};

const readData = (filePath) => JSON.parse(fs.readFileSync(filePath));

module.exports = {
  sleep,
  saveData,
  readData,
};
