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

module.exports = {
  sleep,
  saveData,
};
