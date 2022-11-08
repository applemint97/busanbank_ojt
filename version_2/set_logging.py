import logging
import logging.handlers

log = logging.getLogger("ojt_log")
logging.basicConfig(filename="OJTlog.txt", filemode="w")
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('[Leehwajung]{%(ip)s}[%(levelname)s](%(filename)s:%(lineno)d) %(message)s')

fileHandler = logging.FileHandler('OJTlog.txt')
streamHandler = logging.StreamHandler()

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

log.addHandler(fileHandler)
log.addHandler(streamHandler)

if __name__ == '__main__':
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')