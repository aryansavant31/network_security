import sys

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail:sys):
        self.error_message = error_message
        _, _, exc_tb = error_detail.exc_info()

        self.exc_line_no = exc_tb.tb_lineno # exc = exception
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error has occured in [{0}], line number [{1}], error message [{2}]".format(
            self.filename, self.exc_line_no, str(self.error_message)
        )