import os
import requests


def store_local(collector, csv_path):
    if collector.to_stored:
        metric_df = collector.get_metrics_df()
        if os.path.exists(csv_path):
            metric_df.to_csv(csv_path, mode="a", header=False, index=False, index_label=False)
        else:
            metric_df.to_csv(csv_path, header=False, index=False, index_label=False)
        collector.to_stored = False
    else:
        collector.logger.info("Skipping collect " + type(collector).__name__)


def store_to_database(collector, user_id, public_key):
    if collector.to_stored and collector.remote_url != "":
        metrics_df = collector.get_metrics_df()
        data = metrics_df.to_dict(orient="list")
        post_data = {"user_id": user_id, "key": public_key, "payload": data}
        requests.post(collector.remote_url, post_data=post_data)
    else:
        collector.logger.info("Skipping collector " + type(collector).__name__)
