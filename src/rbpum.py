from typing import Optional
from oo_logger import OOLogger
from uptime import Uptime
import time

class RBPUM:
    """
    This class is the main class for the RBPUM (Really Basic Python Uptime Monitor) application.
    """

    def __init__(self, check_interval:Optional[int]=30) -> None:
        """
        Constructor for the RBPUM class.
        :param check_interval: The interval in seconds between uptime checks. Default is 30 seconds.
        :type check_interval: int
        """

        self.check_interval = check_interval
        self.log = OOLogger(url="https://logs.13h.eu/api/default/aalen_uptime/_json")
        self.uptime = Uptime(urls=["http://www.facebook.com", "http://www.google.com", "http://telekom.de", "http://cloudflare.com", "http://youtube.com"], logger=self.log)

    def run(self) -> None:
        """
        This method runs the RBPUM application.
        It mainly uses the schedule library to schedule the uptime checks.
        """
        
        self.log.info("RBPUM started.")
        self.log.info(f"Check interval is set to {self.check_interval} seconds.")
        self.log.info("========================================================")

        while True:
            self.uptime.check()
            time.sleep(self.check_interval)

        

if __name__ == "__main__":
    rbpum = RBPUM()
    rbpum.run()