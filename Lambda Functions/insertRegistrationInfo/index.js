const axios = require("axios");

exports.handler = async (event) => {
  var mysql = require("mysql");
  var connection = mysql.createConnection({
    host: "wardatabase.cm9i2tottiif.us-west-2.rds.amazonaws.com",
    user: "admin",
    password: "12345678",
    database: "waruserinfo",
  });

  var gotKeyPair = false;
  var test = "false";
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
          public_key = result.data.public_key;
          private_key = result.data.private_key;
        }
      },
      (error) => {
        console.log(error);
      }
    );

  console.log(test);

  if (!gotKeyPair) return response;

  connection.connect();
  return new Promise((resolve, reject) => {
    const query = "INSERT INTO registration_info VALUES (?, ?, ?, ?)";
    connection.query(
      query,
      [event.user_id, event.registration_id, public_key, private_key],
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
