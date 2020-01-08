
import logging

print("hello world")

logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s', filename = 'error_log.log')

logging.error('test log')

