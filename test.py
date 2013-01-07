#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
import sys
import default
import random

'''
	This is not a unit test, just a series of calls that would have been done 
	in the XBMC GUI to test each response.
'''	

default._settings.setSetting('debug', 'true')
# setup
# fetchs categories and shows
categories = default.cache.cacheFunction(default.get_shows_by_categories)
# select a random category for testing
slug = random.choice(categories.keys())
category = categories[slug]
show = random.choice(category['shows'])
rail = random.choice(default.get_rails(show[0]))


# # test categories
# print '+ Test categories'
# default.list_categories()
# print 

# # # test shows
# print '+ Test shows'
# print '... randomly selected for %s' % category['title']
# kwargs = {
# 	'slug': slug, 
# 	'path': 'root/%s' % slug
# }
# default.list_shows(**kwargs)
# print

# # test rails
# print '+ Test rails'
# print '... randomly elected %s (%s)' % (show[1], category['title'])
# kwargs = {
# 	'uri': show[0]
# }
# default.list_rails(**kwargs)
# print

# # test videos
# print '+ Test videos'
# print '... randomly elected %s (%s)' % (rail[1], show[1])
# kwargs = {
# 	'uri': show[0],
# 	'rail_id': rail[0],
# 	'page': 1
# }
# print 'kwargs:', kwargs
# default.list_videos(**kwargs)
# print

# test play
# print '+ Test videos'
# print '... randomly elected %s (%s)' % (rail[1], show[1])
# kwargs = {
# 	'uri': show[0],
# 	'rail_id': rail[0],
# 	'page': 1
# }
# print 'kwargs:', kwargs
# default.list_videos(**kwargs)
# print

# TO-DO

# test login and authorized access, credentials must be passed via arguments
# setup
if len(sys.argv) > 1:
	default._settings.setSetting('username', sys.argv[1])
	default._settings.setSetting('password', sys.argv[2])
	default.authenticate()
else:
	print 'No credentials passed via arguments. Skipping authentication tests.'


_loginInfo = default._settings.getSetting('login_info') or None
if _loginInfo:
	print 'testing'
	a_category = categories['novelas']
	a_show = a_category['shows'][0]
	a_rail = default.get_rails(a_show[0])[2]
	
	default.play(**{'video_id': '2242918'})

# test hash

	# video_list = []
	# video_urls = []
	# for c in content['children']:
	# 	video_urls.append(c['resources'][video_idx]['url'])
	# 	video_list.append(c['resources'][video_idx]['_id'])
	# print '+ Get hashes'
	# req = urllib2.Request(hash_url % (video_id, '|'.join(video_list)))
	# cookie = 'GLBID='\
	# 		+ '16fa241b8d289ebc85c210445058dcc5f37587763516865717572744641337731526f73673835716a4'\
	# 		+ '238444c43794a656947386d67744e504c56647936777377434f426677373043444a6e363732504b3a3'\
	# 		+ '03a7269636172646f626f6e6f6e40676d61696c2e636f6d;'
	# req.add_header('Cookie', cookie)
	# response = urllib2.urlopen(req)
	# data = response.read()
	# response.close()
	# hashes = json.loads(data)['hash']
	# print hashes

	# print '+ Get video'
	# url = video_urls[0] + '?' + hashes[0]
	# print url
	# # req = urllib2.Request(url)
	# # cookie += 'http://flashvideo.globo.com/h264/entretenimento/3/salve_jorge/2012/12/03/EF_CGPN_B_2274933_mmp4.mp4?03135794259489525578045M80z90g9vaH+C3xmYzedQ'
	# # req.add_header('Cookie', cookie)
	# # response = urllib2.urlopen(req)
	# # for a in response.headers:
	# # 	print a, response.headers[a]
	# # response.close()
