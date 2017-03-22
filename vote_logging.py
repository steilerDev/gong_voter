import logging

# Only allow root logger
class Whitelist(logging.Filter):
    def __init__(self, *whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)
        
def init(level=logging.DEBUG):
    FORMAT = "[%(filename)14s:%(lineno)-3s - %(funcName)-10s ] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=FORMAT, level=level)
    
    for handler in logging.root.handlers:
        handler.addFilter(Whitelist('root'))