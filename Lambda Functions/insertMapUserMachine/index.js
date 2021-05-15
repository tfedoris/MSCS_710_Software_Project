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
  var user_id = "";

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
          user_id = result.data.user_id;
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
    const query = "INSERT INTO map_user_machine VALUES (?, ?, ?)";
    connection.query(
      query,
      [user_id, event.machine_id, event.last_updated_time],
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
