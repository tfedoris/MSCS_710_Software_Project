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
      "INSERT INTO network_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
    connection.query(
      query,
      [
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
