from time import clock


def initializeLogger():
    global START_TIME
    START_TIME = clock()

def logInfo(msg):
    seconds = int(clock() - START_TIME)
    print '--------------------'
    print msg
    print "TIME: %d:%02d:%02d" % (seconds/3600, seconds/60%60, seconds%60)
    print
