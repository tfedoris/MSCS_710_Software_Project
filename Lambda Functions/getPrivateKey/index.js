// console.log(connection);
exports.handler = async (event) => {
  var mysql = require("mysql");
  var connection = mysql.createConnection({
    host: "wardatabase.cm9i2tottiif.us-west-2.rds.amazonaws.com",
    user: "admin",
    password: "12345678",
    database: "waruserinfo",
  });

  connection.connect();
  return new Promise((resolve, reject) => {
    const query = `SELECT private_key FROM registration_info WHERE registration_id=?`;
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
    connection.query(query, [event.registration_id], (err, results, fields) => {
      if (err) {
        response.data = err;
        resolve(response);
      } else {
        response.success = results.length > 0 ? true : false;
        response.data = results.length > 0 ? results[0] : {};
        resolve(response);
      }
    });
  });
};
