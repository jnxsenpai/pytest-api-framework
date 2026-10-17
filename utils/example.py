


def cache(func):
    cached = {}

    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in cached:
            cached[key] = func(*args, **kwargs)
        return cached[key]
    return wrapper





