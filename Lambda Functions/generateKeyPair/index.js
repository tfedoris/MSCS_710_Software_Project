// console.log(connection);
exports.handler = async (event) => {
  const { generateKeyPair } = require("crypto");
  var response = {
    success: false,
    data: {},
  };
  const promise = new Promise((resolve, reject) => {
    generateKeyPair(
      "rsa",
      {
        modulusLength: 4096,
        publicKeyEncoding: {
          type: "spki",
          format: "pem",
        },
        privateKeyEncoding: {
          type: "pkcs8",
          format: "pem",
        },
      },
      (err, outPublicKey, outPrivateKey) => {
        if (err) {
          response.data = err;
          return reject(response);
        }
        response.success = true;
        response.data = {
          publicKey: outPublicKey.toString(),
          privateKey: outPrivateKey.toString(),
        };
        resolve(response);
      }
    );
  });

  return promise;
};

const keypair = require("keypair");

exports.handler = async (event) => {
  var response = {
    success: false,
    data: {},
  };

  const promise = new Promise((resolve, reject) => {
    const pair = keypair([1024]);
    response.success = true;
    response.data = {
      publicKey: pair.public,
      privateKey: pair.private,
    };
    resolve(response);
  });

  return promise;
};
