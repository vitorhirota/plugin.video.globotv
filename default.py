"""
        GNT XBMC PLUGIN
"""
# main imports
import json
import re
import urllib
import urllib2
import xbmcgui
import xbmcplugin

#TV DASH - by You 2008.

def PROGRAMAS():
        url = 'http://gnt.globo.com/Programas/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<img src="(.+?)"[\s\S.]+?<h2><a href="(.+?)">(.+?)</a>').findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,1,thumbnail)
                       
def VIDEOS(url):
        url_args = url.split('/')[:-1]
        url_args.append('videos')
        url_videos = '/'.join(url_args)
        req = urllib2.Request(url_videos)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=unicode(response.read(), 'ISO-8859-1')
        # link=response.read()
        response.close()
        match=re.compile('<a href="'+url_videos+'/([^ ]+?)"[\s\S.]+?<img class="imageThumb" src="[#](.+?)"[\s\S.]+?<div class="titulo">(.+?)</div>[\s]+?<div class="subtitulo">[\s]+?([^\t\r\n]*)[\s]+?</div>').findall(link)
        
        swfPlayer = 'http://s.videos.globo.com/p2/player.swf?videosIDs=%s'
        for _url, thumbnail, title, desc in match:
                try:
                        video_id = re.search('\d+', _url).group()
                except:
                        print 'no videos found'
                        break
                video_id = re.search('\d+', _url).group()
                # get link for the stream
                req = urllib2.Request('http://api.globovideos.com/videos/%s/playlist/callback/wmPlayerPlaylistLoaded' % video_id)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()
                contents = json.loads(link[23:-2])
                video_url = ''
                for res in contents['videos'][0]['resources']:
                        if 'iphone' in res['url']:
                                video_url = res['url']
                                break
                addLink(title, 
                        video_url,
                        thumbnail
                        )

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        # print ""
        PROGRAMAS()
       
elif mode==1:
        # print ""+url
        VIDEOS(url)

# elif mode==2:
#         print ""+url
#         VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
