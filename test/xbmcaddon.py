''' 
     XBMC Addon dummy for testing.
     Version: 1.0
'''

class Addon():
    def __init__(self, *args, **kwargs):
        self.settings = {
            'username': 'abc',
            'password': 'def',
            'video_quality': 1,
            'debug': True
        }

    def getSetting(self, *args, **kwargs):
        print "XBMCAddon : getSetting " + repr(args) + " - " + repr(kwargs)
        return self.settings.get(args[0])
        # return "getSetting test return"

    def setSetting(self, *args, **kwargs):
        print "XBMCAddon : setSetting " + repr(args) + " - " + repr(kwargs)
        self.settings[args[0]] = args[1]
        return True

    def openSetting(*args, **kwargs):
        print "XBMCAddon : openSetting " + repr(args) + " - " + repr(kwargs)
        return True

    def getAddonInfo(*args, **kwargs):
        print "XBMCAddon : getSetting " + repr(args) + " - " + repr(kwargs)

        if kwargs.has_key("path"):
            return "/tmp"
        else:
            return "getAddonInfo test return"
