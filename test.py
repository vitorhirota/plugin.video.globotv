# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re

print '+ Testa retorno de programas'
req = urllib2.Request('http://gnt.globo.com/Programas/')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=unicode(response.read(), 'ISO-8859-1')
response.close()
match=re.compile('<img src="(.+?)"[\s\S.]+?<h2><a href="(.+?)">(.+?)</a>').findall(link)
for tb,url,nm in match:
	print 'Programa:', nm, 'URL:', url, 'Thumb:', tb
print len(match), 'programas encontrados'
print

from random import randrange
import json

print '+ Testa retorno dos videos e episodios'
pgr = match[randrange(len(match))]
print '--', pgr[2]
url_args = pgr[1].split('/')[:-1]
url_args.append('videos')
url = '/'.join(url_args)
req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=unicode(response.read(), 'ISO-8859-1')
response.close()
match=re.compile('<a href="'+url+'/([^ ]+?)"[\s\S.]+?<img class="imageThumb" src="[#](.+?)"[\s\S.]+?<div class="titulo">(.+?)</div>[\s]+?<div class="subtitulo">[\s]+?([^\t\r\n]*)[\s]+?</div>').findall(link)
for _url, tb, title, desc in match:
	try:
		video_id = re.search('\d+', _url).group()
	except:
		print 'no videos found'
		break
	# get link for the stream
	req = urllib2.Request('http://api.globovideos.com/videos/%s/playlist/callback/wmPlayerPlaylistLoaded' % video_id)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	contents = json.loads(link[23:-2])
	video_url = ''
	for res in contents['videos'][0]['resources']:
		if 'flash' in res['url']:
			video_url = res['url']
			break
	print """- Titulo: %s
  Descr: %s
  PageUrl: %s/%s 
  Thumb: %s
  Video: %s""" % (title, desc, url, _url, tb, video_url)




print len(match), 'videos encontrados'
print
