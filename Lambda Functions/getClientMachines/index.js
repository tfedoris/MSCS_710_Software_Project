const axios = require("axios");

// Require and initialize outside of your main handler
const mysql = require("serverless-mysql")({
  config: {
    host: process.env.ENDPOINT,
    user: process.env.USER_NAME,
    password: process.env.PASSWORD,
    database: process.env.PRIMARY_DB_NAME,
  },
});

// Main handler function
exports.handler = async (event) => {
  var validated = false;
  var test = "false";
  // Initialize response object
  var response = {
    success: false,
    data: [],
    headers: {
      "X-Requested-With": "*",
      "Access-Control-Allow-Headers":
        "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST,OPTIONS",
    },
  };
  var user_id = "";

  // Set query string
  const query =
    "SELECT machine_id, machine_name " +
    "FROM client_machine " +
    "LEFT JOIN map_user_machine USING(machine_id) " +
    "WHERE user_id = ? " +
    "UNION " +
    "SELECT machine_id, machine_name " +
    "FROM client_machine " +
    "RIGHT JOIN map_user_machine USING(machine_id) " +
    "WHERE user_id = ? ";

  // Run your query
  let results = await mysql.query(query, [user_id, user_id]);
  response.success = results.length > 0 ? true : false;
  response.data = results.length > 0 ? results : {};

  // Run clean up function
  await mysql.end();

  // Return the results
  return response;
};
