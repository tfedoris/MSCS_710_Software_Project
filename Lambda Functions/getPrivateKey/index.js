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
exports.handler = async (event, context) => {
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

  // Set query string
  const query = `SELECT private_key FROM registration_info WHERE registration_id=?`;

  // Run your query
  let results = await mysql.query(query, [event.registration_id]);
  response.success = results.length > 0 ? true : false;
  response.data = results.length > 0 ? results[0] : {};

  // Run clean up function
  await mysql.end();

  // Return the results
  return response;
};
