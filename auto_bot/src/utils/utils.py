import time
from functools import wraps
import yaml
from pathlib import Path

def retry(func):
    """
        Uses attributes of class (max_attempts & delay)
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        attempts = 0
        while attempts < self.max_attempts:
            result = func(self, *args, **kwargs)
            if result:
                return result
            attempts += 1
            time.sleep(self.delay)
    return wrapper

def root_path():
    return Path(__file__).parent.parent.parent
    

def read_config():
    with open(str(root_path() / 'config.yml')) as config_file: 
        return yaml.safe_load(config_file)