def no_cache(func):
    def wrapper():
        print("!")
        response = func()
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"  # HTTP 1.1.
        response.headers["Pragma"] = "no-cache"  # HTTP 1.0.
        response.headers["Expires"] = "0"  # Proxies.
        return response
    return wrapper
