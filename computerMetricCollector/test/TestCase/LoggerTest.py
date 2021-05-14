from computerMetricCollector.CollectorUtils import get_logger


def set_logger(level):
    log_file = "Test.log"
    rotate_time = "midnight"
    backup_cnt = 10
    logger = get_logger(log_file, level, rotate_time, backup_cnt)
    return logger