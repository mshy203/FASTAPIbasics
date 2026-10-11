import inspect
from urllib.parse import urlparse, parse_qs

class MiniApp:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def handle(self, method, url_str):
        parsed = urlparse(url_str)
        path = parsed.path
        
        if path not in self.routes:
            return {"status": 404, "error": "Not Found"}