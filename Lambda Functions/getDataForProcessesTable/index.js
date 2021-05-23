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

  // Set query string
  const query =
    "SELECT entry_time, pid, name, process_status, cpu_percent, memory_physical_used_byte, memory_virtual_bsed_byte, io_read_count, io_read_bytes, io_write_count, io_write_bytes, thread_num " +
    "FROM processes_metrics " +
    "LEFT JOIN map_user_machine USING(machine_id) " +
    "WHERE user_id = ? AND machine_id = ? " +
    "UNION " +
    "SELECT entry_time, pid, name, process_status, cpu_percent, memory_physical_used_byte, memory_virtual_bsed_byte, io_read_count, io_read_bytes, io_write_count, io_write_bytes, thread_num " +
    "FROM processes_metrics " +
    "RIGHT JOIN map_user_machine USING(machine_id) " +
    "WHERE user_id = ? AND machine_id = ?";

  // Run your query
  let results = await mysql.query(query, [
    event.user_id,
    event.machine_id,
    event.user_id,
    event.machine_id,
  ]);
  response.success = results.length > 0 ? true : false;
  response.data = results.length > 0 ? results : {};

  // Run clean up function
  await mysql.end();

  // Return the results
  return response;
};
