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
import json
import re
import requests
import util


# xhrsession = requests.session()
# xhrsession.headers['User-Agent'] = 'xbmc.org'
# xhrsession.headers['X-Requested-With'] = 'XMLHttpRequest'

# url masks
BASE_URL = 'http://globotv.globo.com'
SHOW_URL = BASE_URL + '%(uri)s'
RAIL_URL = SHOW_URL + '/_/trilhos/%(rail)s/page/%(page)s/'
INFO_URL = 'http://api.globovideos.com/videos/%s/playlist'
OFFER_URL = 'http://globotv.globo.com/_/oferta_tematica/%(slug)s.json'
HASH_URL = 'http://security.video.globo.com/videos/%s/hash?resource_id=%s'
LOGIN_URL = 'https://login.globo.com/login/151?tam=widget'


class GloboApi(object):
    def __init__(self, plugin, cache):
        self.plugin = plugin
        self.cache = cache

    def _get_cached(self, key):
        data = self.cache.get(key)
        if data:
            try:
                data = eval(data)
            except:
                pass
        elif 'http://' in key:
                r = requests.get(key)
                data = (r.headers.get('content-type') == 'application/json'
                        and json.loads(r.text) or r.text)
                self.cache.set(key, repr(data))
        return data

    def _get_hashes(self, video_id, resource_ids):
        args = (video_id, '|'.join(resource_ids))
        _cookies = {'GLBID': self.authenticate()}
        req = requests.get(HASH_URL % args, cookies=_cookies)
        self.plugin.log.debug('resource ids: %s' % '|'.join(resource_ids))
        self.plugin.log.debug('return: %s' % req.text)
        try:
            data = json.loads(req.text)
            return data['hash']
        except ValueError:
            msg = 'JSON not returned. Message returned:\n%s' % req.text
            self.plugin.log.error(msg)
            raise
        except KeyError:
            args = (data['http_status_code'], data['message'])
            self.plugin.log.error('Request error: [%s] %s' % args)
            raise

    def _get_video_info(self, video_id):
        recache = False
        info = self._get_cached('video|%s' % video_id) or dict()
        if 'resources' not in info:
            data = self._get_cached(INFO_URL % video_id)['videos'][0]
            # substitute unicode keys with basestring
            data = dict((str(key), value) for key, value in data.items())
            info.update(data)
            recache = True
        if 'duration' not in info:
            info['duration'] = sum(x['resources'][0]['duration']/1000
                                   for x in info.get('children') or [info])
            recache = True
        if recache:
            self.cache.set('video|%s' % video_id, repr(info))
        return info

    def authenticate(self):
        glbid = self.plugin.get_setting('glbid')
        username = self.plugin.get_setting('username')
        password = self.plugin.get_setting('password')

        if not glbid and (username and password):
            payload = {
                'botaoacessar': 'acessar',
                'login-passaporte': username,
                'senha-passaporte': password
            }
            r = requests.post(LOGIN_URL, data=payload)
            glbid = r.cookies.get('GLBID')
            if glbid:
                self.plugin.log.debug('successfully authenticated')
                self.plugin.set_setting('glbid', glbid)
            else:
                self.plugin.log.debug('wrong username or password')
                self.plugin.notify(self.plugin.get_string(31001))
        elif glbid:
            self.plugin.log.debug('already authenticated')
            return glbid

    def get_shows_by_categories(self):
        categories = {}
        data = self._get_cached(BASE_URL)
        # match categories
        rexp = ('<h4 data-tema-slug="(.+?)">(.+?)'
                + '<span[\s\S]+?<ul>([\s\S]+?)</ul>')
        for slug, category, content in re.compile(rexp).findall(data):
            # match show uri, names and thumb and return an object
            # match: ('/gnt/decora', 'Decora', 'http://s2.glbimg.com/[.].png'),
            shows_re = ('<a href="(.+?)".*programa="(.+?)">'
                        + '[\s\S]+?<img data-src="(.+?)"')
            shows = re.compile(shows_re).findall(content)
            categories[slug] = {'title': category, 'shows': shows}
        return categories

    def get_rails(self, uri):
        data = self._get_cached(SHOW_URL % {'uri': uri})
        # match video 'rail's id and name
        # match ex: ('4dff4cf691089163a9000002', 'Edi\xc3\xa7\xc3\xa3o')
        rails_re = 'id="trilho-(.+?)"[\s\S]+?<h2.*title="(.+?)"'
        rails = re.compile(rails_re).findall(data)
        return rails

    def get_rail_videos(self, **kwargs):
        video_count = last_count = 0
        videos = util.struct()
        videos.list = []
        videos.next = 1
        while video_count < int(self.plugin.get_setting('page_size') or 15):
            data = requests.get(RAIL_URL % kwargs).text
            # match video 'rail's
            # match: (title, video_id, date [DD/MM/AAAA],
            #         thumb, duration [MM:SS], plot)
            regExp = (
                '<li.*data-video-title="(.+?)"[\s]+data-video-id="(.+?)"[\s]+'
                + 'data-video-data-exibicao="(.+?)">[\s\S]+?'
                + '<img.+src="(.+?)"[\s\S]+?'
                + '<span class="duracao.*?">(.+?)</span>[\s\S]+?'
                + 'div class="balao">[\s]+?<p>[\s]+?([\w].+?)[\s]+?</p>'
            )
            matches = re.compile(regExp).findall(data)
            mcount = len(matches)
            properties = ('title', 'id', 'date', 'thumb', 'duration', 'plot')
            for item in matches:
                video = util.struct(dict(zip(properties, item)))
                # update attrs
                video.title = util.unescape(video.title)
                video.plot = util.unescape(video.plot)
                video.date = video.date.replace('/', '.')
                _split = video.duration.split(':')
                video.duration = sum(int(x) * 60 ** i for i, x in
                                     enumerate(reversed(_split)))
                self.cache.set('video|%s' % video.id, repr(video))
                videos.list.append(video)
            if mcount == 0 or mcount < last_count:
                videos.next = None
                break
            video_count += mcount
            last_count = mcount
            kwargs['page'] += 1
        if videos.next:
            videos.next = kwargs['page']
        return videos

    def get_offer_videos(**kwargs):
        data = json.loads(requests.get(OFFER_URL % kwargs).text)
        key = {'last': 'ultimos_videos',
               'popular': 'videos_mais_vistos'}[kwargs.get('filter') or 'last']
        content = json.loads(data)[key]
        items = []
        for entry in content:
            title, _id, date, thumb, duration, descr = (entry['titulo'],
                                                        entry['id'],
                                                        entry['exibicao'],
                                                        entry['thumbnail'],
                                                        entry['duracao'],
                                                        entry['descricao'])
            # params = {'action': 'play', 'video_id': _id}
            items.append({
                'Date': date.replace('/', '.'),
                'Duration': duration,
                'PlotOutline': descr,
            })
            # addItem(title, thumb, params, listItemAttr)
            # self.cache.set(_id, repr([title, date, thumb, duration, descr]))
        return items

    def get_videos(self, video_id):
        data = self._get_video_info(video_id)
        if 'children' in data:
            items = [util.struct(self._get_video_info(video['id']))
                     for video in data.get('children')]
            return items
        else:
            return [util.struct(data)]

    def resolve_video_url(self, video_id):
        # which index to look in the list
        hd_first = int(self.plugin.get_setting('video_quality') or 1)
        data = self._get_video_info(video_id)
        self.plugin.log.debug('resolving video: %s' % video_id)
        # this method assumes there's no children
        if 'children' in data:
            raise Exception('Invalid video id: %s' % video_id)

        resources = [r for r in sorted(data['resources'],
                                       key=lambda v: v.get('bitrate') or 0)
                     if r.get('delivery_type') in (None, 'download')]

        if (not hd_first or
                (data.get('subscriber_only') is True and
                 not self.authenticate())):
            return resources[0]['url']
        else:
            r = resources[-1]
            url = r['url'].replace('flash', 'ipad')
            hashes = self._get_hashes(video_id, [r['_id']])
            signed_hashes = util.hashJS.get_signed_hashes(hashes)
            return '?'.join([url, signed_hashes[0]])
