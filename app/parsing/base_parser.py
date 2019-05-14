class BaseParser:
    def __init__(self, obj, whois_data):
        self.obj = obj
        self.whois_data = whois_data
        self.lines = whois_data.split('\n')
        self.data = {}

    def get_data(self):
        return self.data