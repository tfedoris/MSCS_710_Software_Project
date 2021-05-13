from abc import ABC


class Collector(ABC):

    def fetch_metrics(self):
        """
        This function fetch the metrics to be store in the database
        :return:
        """
        pass

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        pass

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        pass
