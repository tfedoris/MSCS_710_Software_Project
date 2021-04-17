import os


def store_local(collector, csv_path):
    if collector.to_stored:
        metric_df = collector.get_metrics_df()
        if os.path.exists(csv_path):
            metric_df.to_csv(csv_path, mode="a", header=False)
        else:
            metric_df.to_csv(csv_path)
        collector.to_stored = False
    else:
        collector.logger.info("Skipping collect " + type(collector).__name__)


def store_to_database(collector, db_connection):
    if collector.to_stored:
        metric_df = collector.get_metrics_df()
        if hasattr(collector, "get_store_table"):
            metric_df.to_sql(collector.get_store_table(), db_connection, if_exists="append", method="multi")
        collector.to_stored = False
    else:
        collector.logger.info("Skipping collect " + type(collector).__name__)
