import os


class Logging:
    """
    Various writes to log files
    """

    @staticmethod
    def open_log_file(log_file):
        # Check path exists
        if os.path.exists(log_file):
            try:
                file = open(log_file, 'a')
            except OSError:
                file = open(log_file, 'w')

            return file
        else:
            return 1

    @classmethod
    def write_log_event(cls, log_file, stage, event, result):
        log = None
        while type(log) is int or log is None:
            # Get file object in append/write mode
            log = cls.open_log_file(log_file)
            if type(log) is int:
                print("Log File Error: Incorrect path for writing")
                log_file = "."
        # If file is empty, first write the header
        if os.path.getsize(log_file) == 0:
            log.write("{:15s}\t{:15s}\t{:15s}\n".format("Stage", "Event", "Result/Details"))

        log.write("{:15s}\t{:15s}\t{:15s}\n".format(stage, event, result))
