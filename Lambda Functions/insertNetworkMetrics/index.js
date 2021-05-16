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
    data: {},
    headers: {
      "X-Requested-With": "*",
      "Access-Control-Allow-Headers":
        "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST,OPTIONS",
    },
  };

  await axios
    .post(
      "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-registration-info",
      {
        registration_id: event.registration_id,
      }
    )
    .then(
      (result) => {
        if (result.data.success) {
          validated = true;
        }
      },
      (error) => {
        console.log(error);
      }
    );

  console.log(test);

  if (!validated) return response;

  // Set query string
  const query =
    "REPLACE INTO network_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

  // Run your query
  let results = await mysql.query(query, [
    event.machine_id,
    event.entry_time,
    event.network_interface,
    event.bytes_send,
    event.bytes_receive,
    event.error_bytes_receive,
    event.error_bytes_send,
    event.packet_sent,
    event.packet_receive,
    event.packet_receive_drop,
    event.packet_send_drop,
    event.nonce,
    event.session_key,
  ]);
  response.success = results.affectedRows > 0 ? true : false;
  response.data = results;

  // Run clean up function
  await mysql.end();

  // Return the results
  return response;
};
