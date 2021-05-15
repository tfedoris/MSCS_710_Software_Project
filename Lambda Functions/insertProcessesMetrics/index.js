const axios = require("axios");

exports.handler = async (event) => {
  var mysql = require("mysql");
  var connection = mysql.createConnection({
    host: "wardatabase.cm9i2tottiif.us-west-2.rds.amazonaws.com",
    user: "admin",
    password: "12345678",
    database: "warproject",
  });

  var validated = false;
  var test = "false";
  var response = { success: false, data: {} };

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

  connection.connect();
  return new Promise((resolve, reject) => {
    const query =
      "INSERT INTO processes_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
    connection.query(
      query,
      [
        event.machine_id,
        event.entry_time,
        event.pid,
        event.name,
        event.start_time,
        event.start_user,
        event.status,
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
      ],
      (err, results, fields) => {
        if (err) {
          response.data = err;
          resolve(response);
        } else {
          console.log(results);
          response.success = results.affectedRows > 0 ? true : false;
          response.data = results;
          resolve(response);
        }
      }
    );
  });
};
