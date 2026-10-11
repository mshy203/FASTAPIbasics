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
        
        func = self.routes[path]
        query_params = parse_qs(parsed.query)
        sig = inspect.signature(func)
        kwargs = {}

        for name, param in sig.parameters.items():
            raw_vals = query_params.get(name)
            
            if raw_vals is None:
                if param.default is inspect.Parameter.empty:
                    return {"status": 422, "error": f"Field '{name}' is required"}
                kwargs[name] = param.default
                continue
            
            val_str = raw_vals[0]
            annotation = param.annotation
            
            try:
                if annotation is bool:
                    kwargs[name] = val_str.lower() in ("true", "1", "yes", "t")
                elif annotation is not inspect.Parameter.empty:
                    kwargs[name] = annotation(val_str)
                else:
                    kwargs[name] = val_str
            except (ValueError, TypeError):
                return {"status": 422, "error": f"Field '{name}' has invalid type"}

        return func(**kwargs)