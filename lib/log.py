#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os, logging, datetime

logDir = os.path.join(os.path.dirname(__file__),"../logs/")
log_file =''.join([logDir, datetime.datetime.now().strftime("%Y%m%d"), '.log'])

def init(logDir):
    logging.basicConfig(level=logging.DEBUG,
            format='%(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=''.join([logDir, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '.log']),
            filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s%(levelname)s %(message)s',datefmt='%Y/%m/%d %H:%M:%S')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    print "succ"
    logging.info("in the init")
   

#设置log文件
def setLog(logMessage, level="info", loggingFile=log_file):
    #if level == "info":
    #    logging.info(logMessage)
    #else:
    #    logging.error(logMessage)
    logger=logging.getLogger()
    _level = {
        "debug" : logger.debug,
        "info" : logger.info,
        "warn" : logger.warn,
        "error" : logger.error,
        "critical" : logger.critical
        }

    handler=logging.FileHandler(loggingFile)
    formatter =logging.Formatter('%(asctime)s-%(levelname)s-%(message)s',datefmt='%Y/%m/%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    _level[level](logMessage)
    # 如果没有此句话，则会将同一个message追加到不同的log中
    logger.removeHandler(handler)

if __name__ == "__main__":
    logDir = "../logs/"
    init(logDir)
    setLog("test.log","12238913",level='error')
    setLog("test.log","12238913",level='debug')
