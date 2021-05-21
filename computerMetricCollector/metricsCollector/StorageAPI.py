import os
import requests
from json import loads


def store_local(collector, csv_path):
    """
    This function store the data frame in the collector on the given csv path
    :param collector: Collector object with the data frame to store
    :param csv_path: Full path of the csv file to store the data frame
    :return:
    """
    metric_df = collector.get_metrics_df()
    try:
        if os.path.exists(csv_path) and not collector.is_stored_locally:
            collector.logger.info("Target csv path " + csv_path + " exists")
            metric_df.to_csv(csv_path, mode="a", header=False, index=False, index_label=False)
            collector.logger.info("Append to " + csv_path)
        else:
            collector.logger.info("Target csv path " + csv_path + " does not exists.")
            collector.logger.info("Created csv for " + type(collector).__name__)
            metric_df.to_csv(csv_path, index=False, index_label=False)
        collector.is_stored_locally = True
    except Exception as e:
        collector.logger.error("Fail to store metrics data to csv for collector " + type(collector).__name__)
        collector.logger.error(e.args[0])


def store_to_database(collector, reg_id):
    """
    This function store the data frame in the collector onto remote database with given registration id that
    authenticate the user.
    :param collector: Collector object with the data frame to store
    :param reg_id: Registration id associate with the user account
    :return:
    """
    if not collector.is_stored and collector.remote_url != "":
        metrics_df = collector.get_metrics_df()
        metrics_df["registration_id"] = reg_id
        post_data = loads(metrics_df.to_json(orient="records"))
        collector.logger.info("Start storing " + type(collector).__name__)
        try:
            for idx, json in enumerate(post_data):
                json["nonce"] = "none"
                json["session_key"] = "none"
                response = requests.post(collector.remote_url, json=json)
                response_text = response.text
                if response.status_code != 200 or "success" not in response_text.lower():
                    collector.logger.error("Fail to store " + type(collector).__name__ + " record " + str(idx))
                    collector.logger.error("Attempt storing metrics data again")
                    response = requests.post(collector.remote_url, json=json)
                    response_text = response.text
                    if response.status_code == 200 or "success" not in response_text.lower():
                        collector.logger.error("Second attempt fail")
                        print("Fail to store " + type(collector).__name__ + " record " + str(idx))
                    else:
                        collector.is_stored = True
                else:
                    collector.is_stored = True
        except ConnectionError as ce:
            collector.logger.error("Connection error in persisting data to remote database")
            print("Connection error in persisting data to remote database")
            print("Please check your network connection.")
            collector.logger.error(ce.args[0])
        except Exception as e:
            collector.logger.error("Fail to persist " + type(collector).__name__ + " onto remote database" )
            print("Fail to persist performance metrics to the database")
            print("Please contact the development team or report this issue on " +
                  "https://github.com/tfedoris/MSCS_710_Software_Project")
            collector.logger.error(e.args[0])
        collector.logger.info("End storing " + type(collector).__name__)
    else:
        collector.logger.info("Skipping collector " + type(collector).__name__)


def register_machine(logger, reg_url, reg_id, machine_id, datetime):
    """
    This function post a record that associated the user account with the host machine
    :param logger: the logger instance for writing the state of the software
    :param reg_url: URL of the API to register the record that map the user and the host machine
    :param reg_id: Registration id that represents the user
    :param machine_id: Machine id of the host machine
    :param datetime: datetime of the record
    :return:
    """
    data_json = {
        "registration_id": reg_id,
        "machine_id": machine_id,
        "last_updated_time": datetime
    }
    logger.info("Start registering user machine on to the database")
    response = requests.post(reg_url, json=data_json)
    response_text = response.text
    if response.status_code != 200 or "success" not in response_text.lower():
        logger.error("Fail to register user machine")
        logger.error("Attempt storing metrics data again")
        response = requests.post(reg_url, json=data_json)
        response_text = response.text
        if response.status_code != 200 or "success" not in response_text.lower():
            logger.error("Fail to register user machine the second time.")
    logger.info("End registering user machine on to the database")
    return response
