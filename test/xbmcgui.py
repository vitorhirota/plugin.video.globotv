''' 
     XBMC Gui dummy for testing.
     Version: 1.0
'''
class Base():
    msg = 'XBMCGui   |%-21s: %s'

class Dialog(Base):
    def create(self, *args, **kwargs):
        print self.msg % ('Dialog->create', repr(kwargs))
        # print "XBMCGui : Dialog->create : " + repr(args) + " - " + repr(kwargs)
        return True

    def close(self, *args, **kwargs):
        print self.msg % ('Dialog->close', repr(kwargs))
        # print "XBMCGui : Dialog->close : " + repr(args) + " - " + repr(kwargs)
        return True

    def update(self, *args, **kwargs):
        print self.msg % ('Dialog->update', repr(kwargs))
        # print "XBMCGui : Dialog->update : " + repr(args) + " - " + repr(kwargs)
        return True

    def select(self, *args, **kwargs):
        print self.msg % ('Dialog->select', repr(kwargs))
        # print "XBMCGui : Dialog->select : " + repr(args) + " - " + repr(kwargs)
        return True

class ListItem(Base):
    def __init__(self, *args, **kwargs):
        # print self.msg % ('ListItem', repr(kwargs))
        # print "XBMCGui : ListItem : " + repr(args) + " - " + repr(kwargs)
        self.properties = {}
        pass

    def getProperty(self, name):
        # print self.msg % ('ListItem->setProperty', repr(args))
        # print "XBMCGui : ListItem->setProperty : " + repr(args) + " - " + repr(kwargs)
        return self.properties[name]

    def setInfo(self, *args, **kwargs):

        print self.msg % ('ListItem->setInfo', repr(args))
        # print "XBMCGui : ListItem->setInfo : " + repr(args) + " - " + repr(kwargs)
        return True

    def setProperty(self, *args, **kwargs):
        # print self.msg % ('ListItem->setProperty', repr(args))
        # print "XBMCGui : ListItem->setProperty : " + repr(args) + " - " + repr(kwargs)
        self.properties[args[0]] = args[1]
        return True


def ControlImage(*args, **kwargs):
    print "XBMCGui : ControlImage : " + repr(args) + " - " + repr(kwargs)
    return True

def ControlLabel(*args, **kwargs):
    print "XBMCGui : ControlLabel : " + repr(args) + " - " + repr(kwargs)
    return True

def ControlProgress(*args, **kwargs):
    print "XBMCGui : ControlProgress : " + repr(args) + " - " + repr(kwargs)
    return True

def WindowXMLDialog(*args, **kwargs):
    print "XBMCGui : WindowXMLDialog : " + repr(args) + " - " + repr(kwargs)
    return True

def getCurrentWindowId(*args, **kwargs):
    print "XBMCGui : getCurrentWindowId : " + repr(args) + " - " + repr(kwargs)
    return True

def Window(*args, **kwargs):
    print "XBMCGui : Window : " + repr(args) + " - " + repr(kwargs)
    return True

