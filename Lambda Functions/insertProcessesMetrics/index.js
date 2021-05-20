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
    "REPLACE INTO processes_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

  // Run your query
  let results = await mysql.query(query, [
    event.machine_id,
    event.entry_time,
    event.pid,
    event.name,
    event.start_time,
    event.start_user,
    event.process_status,
    event.cpu_user_time,
    event.cpu_kernel_time,
    event.cpu_percent,
    event.memory_percent_used_byte,
    event.memory_physical_used_byte,
    event.memory_virtual_used_byte,
    event.memory_unique_used_byte,
    event.memory_page_fault,
    event.io_read_count,
    event.io_read_bytes,
    event.io_write_count,
    event.io_write_bytes,
    event.thread_num,
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
