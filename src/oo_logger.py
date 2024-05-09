import requests, os, urllib3
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from typing import Optional
from datetime import datetime

class OOLogger:
    """
    This class implements a lightweight basic logger for the RBPUM application using the OpenObserve Platform api.
    """

    def __init__(self, url:str) -> None:
        self.queue = []
        self.url = url
        load_dotenv()
        self.auth = HTTPBasicAuth(os.getenv("OBSERVE_API_USER"),  os.getenv("OBSERVE_API_PW"))
        self.identifier = os.getenv("LOG_IDENTIFIER")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def info(self, message:str, further_fields:Optional[dict]=None) -> None:
        """
        This method logs an info message.
        """
        self._log("INFO", message, further_fields)
    
    def error(self, message:str, further_fields:Optional[dict]=None) -> None:
        """
        This method logs an error message.
        """
        self._log("ERROR", message, further_fields)

    def warning(self, message:str, further_fields:Optional[dict]=None) -> None:
        """
        This method logs a warning message.
        """
        self._log("WARNING", message, further_fields)

    def _log(self, level:str, message:str, further_fields:Optional[dict]=None) -> None:
        
        log_content = {
            "level": level,
            "message": message,
            "identifier": self.identifier,
            "datetime": datetime.now().isoformat()
        }

        if further_fields:
            log_content.update(further_fields)
        
        self._send_to_api(log_content=log_content)
        
    def _send_to_api(self, log_content:dict) -> bool:
        """
        This method sends the log content to the OpenObserve Platform api.
        """
        
        headers = {'Content-Type': 'application/json'}
        
        self.queue.append(log_content)
        queue_copy = self.queue.copy()
        for log in queue_copy:
            try:
                response = requests.post(self.url, json=log, auth=self.auth, headers=headers, verify=False)
                if response.status_code == 200:
                    self.queue.remove(log)
                else:
                    return False
            except Exception as e:
                return False

