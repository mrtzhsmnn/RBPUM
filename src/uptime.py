from typing import List
import time, requests
from oo_logger import OOLogger

class Uptime:
    """
    This class is used to check the online status of my server
    """

    def __init__(self, urls: List[str], logger:OOLogger):
        """
        Constructor for the Uptime class.
        """
        
        self.urls = {}

        for url in urls:
            self.urls[url] = {
                "paused": False,
                "pause_started": 0,
            }
        
        self.log = logger
        
    def check(self):
        """
        This method checks the online status of the server.
        """
        ret_bool = False
        failed_urls = []

        for url in self.urls.keys():
            
            if self.urls[url]["paused"] and self.urls[url]["pause_started"] + 300 < time.time():
                self.urls[url]["paused"] = False
            
            if not self.urls[url]["paused"]:
                if not self.ping(url):
                    failed_urls.append(url)
                
                else:
                    ret_bool = True
                    
                    for url in failed_urls:
                        self.urls[url]["paused"] = True
                        self.urls[url]["pause_started"] = time.time()
                    break
        if not ret_bool:
            self.log.error(f"Server has no internet connection.")
        else:
            self.log.info(f"Server is online.")
        return ret_bool
    
    def ping(self, url: str) -> bool:
        """
        This method pings the server to check if it is online.
        """
        try:
            resp = requests.get(url, timeout=0.1)
        except Exception as e:
            self.log.warning(f"Error while pinging {url}. Error: {e}")
            return False
        if resp.status_code == 200:
            return True
        else:
            self.log.warning(f"Status code {resp.status_code} while pinging {url}")
            return False
        
        