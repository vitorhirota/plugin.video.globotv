#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    Globo.tv plugin for XBMC
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# main imports
from StringIO import StringIO
import gzip
import json
import re
import sys
# import util
import urllib
import urllib2
try:
    import xbmcgui
    import xbmcplugin
except:
    import test.xbmcgui as xbmcgui
    import test.xbmcplugin as xbmcplugin

try:
    import StorageServer
except:
    import test.storageserverdummy as StorageServer

cache = StorageServer.StorageServer("Globosat", 12)
_thisPlugin = 0

# url masks
BASE_URL = 'http://globotv.globo.com'
SHOW_URL = BASE_URL + '%(uri)s'
RAIL_URL = SHOW_URL + '/_/trilhos/%(rail_id)s/page/%(page)s/'
INFO_URL = 'http://api.globovideos.com/videos/%s/playlist'
OFFER_URL = 'http://globotv.globo.com/_/oferta_tematica/%(slug)s.json'


# === Helper methods ================================================================= #
def get_request(url):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    return request


def get_page(url):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    response.close()
    return data


def get_shows_by_categories():
    categories = {}
    data = get_page(BASE_URL)
    # match categories
    match_categories = re.compile('<h4 data-tema-slug="(.+?)">(.+?)<span[\s\S]+?<ul>([\s\S]+?)</ul>').findall(data)
    for slug, category, content in match_categories:
        # match show uri, names and thumb and build a dict with all the info
        # match ex: ('/gnt/decora', 'Decora', 'http://s2.glbimg.com/[...]/5175/logotipo_xs/1/45x34.png'),
        shows = re.compile('<a href="(.+?)".*programa="(.+?)">[\s\S]+?<img data-src="(.+?)"').findall(content)
        categories[slug] = {'title': category, 'shows': shows}
    return categories


def get_rails(uri):
    data = get_page(SHOW_URL % {'uri': uri})
    # match video 'rail's id and name
    # match ex: ('4dff4cf691089163a9000002', 'Edi\xc3\xa7\xc3\xa3o')
    # print data
    rails = re.compile('id="trilho-(.+?)"[\s\S]+?<h2.*title="(.+?)"').findall(data)
    # print rails
    return rails


# === Navigation methods ============================================================= #
def list_categories():
    items = []
    categories = cache.cacheFunction(get_shows_by_categories)
    params = {'action': 'list_shows'}
    for slug, category in categories.items():
        params['slug'] = slug
        params['path'] = 'root/' + slug
        name = '%s (%s shows)' % (category['title'], len(category['shows']))
        addFolder(name, '', params)


def list_shows(**kwargs):
    slug = kwargs['slug']
    shows = cache.cacheFunction(get_shows_by_categories)[slug]['shows']
    addFolder('Últimos vídeos', '', {'action': 'list_videos', 'filter': 'last', 'slug': slug})
    addFolder('Mais vistos', '', {'action': 'list_videos', 'filter': 'popular', 'slug': slug})
    params = {'action': 'list_rails'}
    for uri, name, thumb in shows:
        params.update({'uri': uri, 'path': kwargs['path'] + uri})
        addFolder(name, thumb, params)


def list_rails(**kwargs):
    uri = kwargs['uri']
    rails = cache.cacheFunction(get_rails, uri)
    params = {
        'action': 'list_videos',
        'filter': 'rail',
        'uri': uri, 
        'rail_id': '',
        'page': 1,
    }
    for rail_id, name in rails:
        name = ' '.join(x.capitalize() for x in name.split(' '))
        params['rail_id'] = rail_id
        addFolder(name, '', params)


def list_videos(**kwargs):
    if kwargs.get('rail_id'):
        video_count = 0
        while video_count < 10:
            data = get_page(RAIL_URL % kwargs)
            # match video 'rail's
            # match ex: ('Guias do Complexo - parte 1', '2256997', '24/11/2012', 
            #            'http://s02.video.glbimg.com/180x108/2256997.jpg', '05:37', 
            #            'A ag\xc3\xaancia de turismo Bom Fruto forma guias [...] para os tursitas'), 
            regExp = (
                '<li.*data-video-title="(.+?)"[\s]+data-video-id="(.+?)"[\s]+data-video-data-exibicao="(.+?)">[\s\S]+?'
                + '<img.+src="(.+?)"[\s\S]+?'
                + '<span class="duracao.*?">(.+?)</span>[\s\S]+?'
                + 'div class="balao">[\s]+?<p>[\s]+?([\w].+?)[\s]+?</p>'
            )
            videos=re.compile(regExp).findall(data)
            if len(videos) == 0: break
            for title, _id, date, thumb, duration, descr in videos:
                params = {'action': 'play', 'video_id': _id}
                listItemAttr = {
                    'Date': date.replace('/', '.'),
                    'Duration': duration,
                    'PlotOutline': descr,
                }
                addItem(title, thumb, params, listItemAttr)
                cache.set(_id, repr([title, date, thumb, duration, descr]))
            video_count += len(videos)
            kwargs['page'] += 1
        # add next page
        if len(videos) > 0:
            kwargs['page'] += 1
            addFolder('Próxima Página', '', kwargs)
    else:
        data = get_page(OFFER_URL % kwargs)
        key = {'last': 'ultimos_videos', 'popular': 'videos_mais_vistos'}[kwargs.get('filter') or 'last']
        content = json.loads(data)[key]
        for entry in content:
            title, _id, date, thumb, duration, descr = (entry['titulo'], entry['id'], 
                                                        entry['exibicao'], entry['thumbnail'], 
                                                        entry['duracao'], entry['descricao'])
            params = {'action': 'play', 'video_id': _id}
            listItemAttr = {
                'Date': date.replace('/', '.'),
                'Duration': duration,
                'PlotOutline': descr,
            }
            addItem(title, thumb, params, listItemAttr)
            cache.set(_id, repr([title, date, thumb, duration, descr]))


def play(**kwargs):
    video_id = kwargs['video_id']
    data = get_page(INFO_URL % video_id)
    content = json.loads(data)['videos'][0]
    _type  = content['type']
    
    if _type == 'Video':
        listItem = getVideoItem(video_id, content)
        xbmcplugin.setResolvedUrl(handle=_thisPlugin, succeeded=True, listitem=listItem) 
    elif _type in ('Gallery', 'FullEpisode'):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        # queue all entries
        for idx, entry in enumerate(content['children']):
            listItem = getVideoItem(entry['id'])
            listItem.setProperty('IsPlayable', 'true')
            listItem.setProperty('Video', 'true')
            playlist.add(url='%s?action=play&video_id=%s' % (sys.argv[0], entry['id']), 
                         listitem=listItem,
                         index=idx)
        xbmc.executebuiltin('playlist.playoffset(video, 0)')


def getVideoItem(video_id, content=''):
    if not content:
        data = get_page(INFO_URL % video_id)
        content = json.loads(data)['videos'][0]

    if content['type'] == 'Video':
        # get 'iphone' video url
        vUrl = ''
        for res in content['resources']:
            if 'iphone' in res['url']:
                vUrl = res['url']
                break
        try:
            title, date, thumb, duration, descr = eval(cache.get(video_id))
        except:
            title, date, thumb, duration, descr = [content['title'], '', '', '', '']
        listItem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb, path=vUrl)
        listItem.setInfo('video', {
            'date'        : date.replace('/', '.'),
            'duration'    : duration,
            'genre'       : content.get('category'),
            'plotoutline' : descr,
            'title'       : title,
            'duration'    : duration,
            'studio'      : content['channel'],
            'premiered'   : '%s-%s-%s' % (date[-4:], date[3:5], date[:2]),
            'aired'       : '%s-%s-%s' % (date[-4:], date[3:5], date[:2]),
        })
        return listItem


def addFolder(name, thumb, params):
    return addItem(name, thumb, params, isFolder=True)

def addItem(name, thumb, params, listItemAttr={}, isFolder=False):
    ok = True
    listItemAttr.update({'Title': name})
    listItem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
    listItem.setInfo(type="Video", infoLabels=listItemAttr)
    if not isFolder:
        listItem.setProperty('IsPlayable', 'true')
        listItem.setProperty('Video', 'true')
    ok = xbmcplugin.addDirectoryItem(
            handle=_thisPlugin,
            url=sys.argv[0]+'?'+urllib.urlencode(params),
            listitem=listItem,
            isFolder=isFolder)
    return ok

        
def get_params():
    qs = sys.argv[2].lstrip('?').rstrip('/').split('&')
    try:
        r = dict([x.split("=") for x in qs])
    except:
        r = {}
    return r


if __name__ == '__main__':
    _thisPlugin = int(sys.argv[1])
    params=get_params()
    if 'path' in params:
        params['path'] = urllib.unquote(params['path'])
    if 'uri' in params:
        # unquote uri params
        params['uri'] = urllib.unquote(params['uri'])
    if 'page' in params:
        # cast to int
        params['page'] = int(params['page'])
    # call action function with given params
    action = params.get('action') or 'list_categories'
    print 'Action: %s' % action
    print 'Params: %s' % params
    locals()[action](**params)

    xbmcplugin.endOfDirectory(_thisPlugin)
