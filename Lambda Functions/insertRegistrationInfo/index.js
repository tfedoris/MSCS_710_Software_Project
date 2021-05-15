const axios = require("axios");

// Require and initialize outside of your main handler
const mysql = require("serverless-mysql")({
  config: {
    host: "wardatabase.cm9i2tottiif.us-west-2.rds.amazonaws.com",
    user: "admin",
    password: "12345678",
    database: "waruserinfo",
  },
});

// Main handler function
exports.handler = async (event) => {
  var validated = false;
  var test = "false";
  // Initialize response object
  var response = {
    success: false,
    data: {},
    headers: {
      "X-Requested-With": "*",
      "Access-Control-Allow-Headers":
        "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST,OPTIONS",
    },
  };
  var gotKeyPair = false;
  var public_key = "";
  var private_key = "";

  await axios
    .get(
      "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/generate-key-pair"
    )
    .then(
      (result) => {
        if (result.data.success) {
          gotKeyPair = true;
          public_key = result.data.data.publicKey;
          private_key = result.data.data.privateKey;
        }
      },
      (error) => {
        console.log(error);
      }
    );

  console.log(test);

  if (!gotKeyPair) return response;

  // Set query string
  const query = "REPLACE INTO registration_info VALUES (?, ?, ?, ?)";

  // Run your query
  let results = await mysql.query(query, [
    event.user_id,
    event.registration_id,
    public_key,
    private_key,
  ]);
  response.success = results.affectedRows > 0 ? true : false;
  response.data = results;

  // Run clean up function
  await mysql.end();

  // Return the results
  return response;
};
