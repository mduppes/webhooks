import logging

def logging():
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    return logging
