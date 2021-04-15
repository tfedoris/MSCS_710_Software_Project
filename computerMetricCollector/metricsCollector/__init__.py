

def store_local(collector, csv_path):
    metric_df = collector.get_metrics_df()
    metric_df.to_csv(csv_path)


def store_to_database(collector, connector):
    metric_df = collector.get_metrics_df()
    if hasattr(collector, "get_store_table"):
        metric_df.to_sql(collector.get_store_table(), connector, if_exists="append", method="multi")