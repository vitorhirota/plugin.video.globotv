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
import json
import re
import sys
import util
import urllib
import urllib2
try:
    import xbmc, xbmcaddon, xbmcgui, xbmcplugin
except:
    import test.xbmc as xbmc
    import test.xbmcaddon as xbmcaddon
    import test.xbmcgui as xbmcgui
    import test.xbmcplugin as xbmcplugin
try:
    import StorageServer
except:
    import test.storageserverdummy as StorageServer

cache = StorageServer.StorageServer("Globosat", 12)

_thisPlugin = 0
_loginInfo = None
_settings = xbmcaddon.Addon(id='plugin.video.globotv')
_scraper = util.Scraper()

# url masks
BASE_URL = 'http://globotv.globo.com'
SHOW_URL = BASE_URL + '%(uri)s'
RAIL_URL = SHOW_URL + '/_/trilhos/%(rail_id)s/page/%(page)s/'
INFO_URL = 'http://api.globovideos.com/videos/%s/playlist'
OFFER_URL = 'http://globotv.globo.com/_/oferta_tematica/%(slug)s.json'
HASH_URL  = 'http://security.video.globo.com/videos/%s/hash?resource_id=%s'
LOGIN_URL = 'https://login.globo.com/login/151?tam=widget'


# === Scrapping methods ============================================================== #
def authenticate():
    if not _loginInfo:
        data = {
            'botaoacessar': 'acessar',
            'login-passaporte': _settings.getSetting('username'),
            'senha-passaporte': _settings.getSetting('password'),
        }
        _scraper.get_page(LOGIN_URL, data)
        # _scraper.__cj__.clear_session_cookies()
        if len(_scraper.__cj__) > 1:
            _logininfo = _scraper.__cj__.dump()
            # import pdb; pdb.set_trace()
            _settings.setSetting('login_info', _logininfo)
            log('successfully authenticated')
        else:
            log('invalid user or password')
    else:
        log('already authenticated')


def get_shows_by_categories():
    categories = {}
    data = _scraper.get_page(BASE_URL)
    # match categories
    match_categories = re.compile('<h4 data-tema-slug="(.+?)">(.+?)<span[\s\S]+?<ul>([\s\S]+?)</ul>').findall(data)
    for slug, category, content in match_categories:
        # match show uri, names and thumb and build a dict with all the info
        # match ex: ('/gnt/decora', 'Decora', 'http://s2.glbimg.com/[...]/5175/logotipo_xs/1/45x34.png'),
        shows = re.compile('<a href="(.+?)".*programa="(.+?)">[\s\S]+?<img data-src="(.+?)"').findall(content)
        categories[slug] = {'title': category, 'shows': shows}
    return categories


def get_rails(uri):
    data = _scraper.get_page(SHOW_URL % {'uri': uri})
    # match video 'rail's id and name
    # match ex: ('4dff4cf691089163a9000002', 'Edi\xc3\xa7\xc3\xa3o')
    # print data
    rails = re.compile('id="trilho-(.+?)"[\s\S]+?<h2.*title="(.+?)"').findall(data)
    # print rails
    return rails


def get_hashes(video_id, resource_ids=[]):
    data = _scraper.get_page(HASH_URL % (video_id, '|'.join(resource_ids)))
    log('video id: %s, resource ids: %s' % (video_id, '|'.join(resource_ids)))
    log ('hashes: %s' % data)
    hashes = json.loads(data)
    return hashes


def get_list_items(data):
    def transpose_items(items, reverse_items):
        _fn = reverse_items and reversed or list
        return zip(*[[(j['_id'], j['url'].replace('flash', 'ipad')) for j in _fn(i['resources'])] for i in items])

    hash_util = util.Hash()
    # set-up resources
    items = data.get('children') \
            or [{'id': data['id'], 'resources': data['resources']}]

    resolved = False
    for i in transpose_items(items, _settings.getSetting('video_quality')):
        # log('items: %s' % i)
        # log('ids: %s' % [x[0] for x in i])
        hashes = hash_util.setSignedHashes(get_hashes(data['id'], [x[0] for x in i]))
        if len(hashes) == 1:
            hashes *= len(i)
        urls = ['?'.join(i) for i in zip([x[1] for x in i], hashes)]
        
        try:
            response = urllib2.urlopen(urls[0])
            if response.getcode() == 200: 
                resolved = True
                break
        except:
            continue

    if not resolved:
        raise Exception('No videos resolved.')

    listItems = []
    for idx, item in enumerate(items):
        try:
            title, date, thumb, duration, descr = eval(cache.get(item['id']))
        except:
            title, date, thumb, duration, descr = [data['title'], '', '', '', '']
        
        listItem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb, path=urls[idx])
        listItem.setInfo('video', {
            'date'        : date.replace('/', '.'),
            'duration'    : duration,
            'genre'       : data.get('category'),
            'plotoutline' : descr,
            'title'       : title,
            'duration'    : duration,
            'studio'      : data.get('channel'),
            'premiered'   : '%s-%s-%s' % (date[-4:], date[3:5], date[:2]),
            'aired'       : '%s-%s-%s' % (date[-4:], date[3:5], date[:2]),
        })
        listItem.setProperty('IsPlayable', 'true')
        listItem.setProperty('Video', 'true')
        listItem.setProperty('VideoId', str(item['id']))
        # add to return
        listItems.append(listItem)
    return listItems

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
            data = _scraper.get_page(RAIL_URL % kwargs)
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
        data = _scraper.get_page(OFFER_URL % kwargs)
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
    data = cache.cacheFunction(_scraper.get_page, INFO_URL % video_id)
    content = json.loads(data)['videos'][0]
    _type  = content['type']

    listItems = get_list_items(content)
    if len(listItems) > 1:
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        # queue all entries
        for listItem in listItems:
            print listItem.getProperty('VideoId')
            playlist.add(url='%s?action=play&video_id=%s' % (sys.argv[0], listItem.getProperty('VideoId')), 
                         listitem=listItem)
        xbmc.executebuiltin('playlist.playoffset(video, 0)')
    else:
        xbmcplugin.setResolvedUrl(handle=_thisPlugin, succeeded=True, listitem=listItems[0]) 

# === Helper methods ================================================================= #

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

def log(msg):
    import inspect
    _dbg = _settings.getSetting('debug')
    if _dbg:
        xbmc.log('[globotv] %s: %s' % (inspect.stack()[1][3], msg))
        

def get_params():
    qs = sys.argv[2].lstrip('?').rstrip('/').split('&')
    try:
        r = dict([x.split("=") for x in qs])
    except:
        r = {}
    return r

# ==================================================================================== #

if __name__ == '__main__':
    _thisPlugin = int(sys.argv[1])

    # login info
    # _loginInfo = _settings.getSetting('login_info')
    _username = _settings.getSetting('username')
    _password = _settings.getSetting('password')
    if not _loginInfo and _username and _password:
        authenticate()

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
    # print 'Action: %s' % action
    log('Params: %s' % params)
    locals()[action](**params)

    xbmcplugin.endOfDirectory(_thisPlugin)
