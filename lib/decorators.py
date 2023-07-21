class Decorators:
    @staticmethod
    def check_http(func):
        def wrapper(url: str):
            assert any((url.startswith('http://'), url.startswith('https://'))), 'invalid url address (url must statswich on "http://" or "https://")'
            return func(url)
        return wrapper

