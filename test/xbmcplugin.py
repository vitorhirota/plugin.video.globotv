''' 
     XBMC plugin dummy for testing.
     Version: 1.0
'''
msg = 'XBMCPlugin|%-21s: %s'

def endOfDirectory(*args, **kwargs):
    print msg % ('endOfDirectory', repr(kwargs))
    # print "XBMCPlugin : endOfDirectory : " + repr(args) + " - " + repr(kwargs)
    return True

def addDirectory(*args, **kwargs):
    print msg % ('addDirectory', repr(kwargs))
    # print "XBMCPlugin : addDirectory : " + repr(args) + " - " + repr(kwargs)
    return True

def addDirectoryItem(*args, **kwargs):
    print msg % ('addDirectoryItem', repr(kwargs))
    # print "XBMCPlugin : addDirectoryItem : " + repr(args) + " - " + repr(kwargs)
    return True

def setContent(*args, **kwargs):
    print msg % ('setContent', repr(kwargs))
    # print "XBMCPlugin : setContent : " + repr(args) + " - " + repr(kwargs)
    return True

def addSortMethod(*args, **kwargs):
    print msg % ('addSortMethod', repr(kwargs))
    # print "XBMCPlugin : addSortMethod : " + repr(args) + " - " + repr(kwargs)
    return True

def setResolvedUrl(*args, **kwargs):
    print msg % ('setResolvedUrl', repr(kwargs))
    # print "XBMCPlugin : setResolvedUrl : " + repr(args) + " - " + repr(kwargs)
    return True
