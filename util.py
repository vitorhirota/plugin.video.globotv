import gzip
import sys 
import urllib
import urllib2
from cookielib import CookieJar

try:
    import cPickle as pickle
except ImportError:
    import pickle
from StringIO import StringIO


class SCookieJar(CookieJar):
    def __init__(self, string=None, policy=None):
        CookieJar.__init__(self, policy)
        if hasattr(sys.modules[ "__main__" ], '_loginInfo'):
            self._cookies = pickle.loads(sys.modules[ "__main__" ]._loginInfo)

    def dump(self):
        return pickle.dumps(self._cookies)


class Scrapper():
    __cj__ = SCookieJar()
    __opener__ = urllib2.build_opener(urllib2.HTTPCookieProcessor(__cj__))
    urllib2.install_opener(__opener__)

    def get_request(self, url, data=None, headers=None):
        if not headers:
            headers = {}
        headers.update({
                'Accept-encoding': 'gzip',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1'
            })
        if data:
            data = urllib.urlencode(data)
            headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        # if _loginInfo:
        #     headers.update({'Cookie': _loginInfo})
        return urllib2.Request(url, data, headers)

    def get_page(self, url, data=None):
        response = urllib2.urlopen(self.get_request(url, data))
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response.read()
        response.close()
        return data


class Hash():
    '''
        hd content hashing methods for authorized users
        http://s.videos.globo.com/p2/j/api.min.js
    '''
    class alist(list):
        '''helper class to "mimic" JS Arrays behaviour'''
        def __getitem__(self, key):
            try:
                return list.__getitem__(self, key)
            except IndexError:
                return 0
        def __setitem__(self, key, value):
            try:
                return list.__setitem__(self, key, value)
            except IndexError:
                for i in range(key - len(self) + 1): 
                    self.append(0)
                self.__setitem__(key, value)

    C = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    D = 3600
    E = "=0xAC10FD"    
    F = ""

    def setSignedHashes(self, a):
        try:
            b = type(a['hash']) == list and a['hash'] or [a['hash']]
            return map(self.L, b)
        except:
            return ['']

    def signed(self, i):
        if (i & 0x80000000): return -0x100000000 + i
        return i
    def _32_lshift(self, data, bits):
        # return (data & 0xFFFFFF) << bits
        return self.signed((data << bits) & 0xFFFFFFFF)
    def _32_rshift(self, data, bits):
        return (data & 0xFFFFFF) >> bits
    def _right_shift(self, data, bits):
        sign = (data >> 31) & 1 
        if sign:
           fills = ((sign << bits) - 1) << (32 - bits)
        else:
           fills = 0
        return ((data & 0xffffffff) >> bits) | fills
    def _zero_fill_right_shift(self, data, bits):
        return (data & 0xffffffff) >> bits
    ####
    # the bitwise methods are to guarantee the same expected behaviour as in JS
    # http://stackoverflow.com/questions/6535373/special-js-operators-in-python
    ####
    def _b(self, a):
        b = ""; c = len(a)
        for d in range(0, c, 3):
            e = ord(a[d]) << 16 | (d + 1 < c and ord(a[d+1]) << 8 or 0) | (d + 2 < c and ord(a[d+2]) or 0)
            for f in range(0, 4):
                if d * 8 + f * 6 > c* 8:
                    b += self.F
                else: 
                    # zero fill right shift
                    b += self.C[e >> 6 * (3 - f) & 63]
        # print '_b:', a, b, c
        return b
    def _c(self, a, b):
        c = ""; d = 0
        a += b[1:9]
        while d < len(a):
            e = ord(a[d])
            f = d + 1 < len(a) and ord(a[d + 1]) or 0
            # print '_c:', a, b, c, d, e, f
            if (55296 <= e and e <= 56319 and
                    56320 <= f and f <= 57343):
                e = 65536 + ((e & 1023) << 10) + (f & 1023)
                d += 1
            # zero fill right shift
            if e <= 127:
                c += unichr(e)
            elif e <= 2047:
                c += unichr(192 | e >> 6 & 31) + unichr(128 | e & 63)
            elif e <= 65535:
                c += unichr(224 | e >> 12 & 15) + unichr(128 | e >> 6 & 63) + unichr(128 | e & 63)
            elif e <= 2097151:
                c += unichr(240 | e >> 18 & 7) + unichr(128 | e >> 12 & 63) + unichr(128 | e >> 6 & 63) + unichr(128 | e & 63)
            d += 1
        # print '_c:', a, b, c, d
        return c
    def _d(self, a):
        b = [0 for c in range((len(a) >> 2)+1)]
        for c in range(0, len(a) * 8, 8):
            b[c >> 5] |= (ord(a[c / 8]) & 255) << c % 32
            # print '_d:', '%2s' % (c >> 5), b
        # print '_d:', a, b
        return b
    def _e(self, a):
        b = ""
        for c in range(0, len(a) * 32, 8):
            # zero fill right shift 5] >>> c
            b += unichr(a[c >> 5] >> c % 32 & 255);
            # print '_e:', b
        # print '_e:', a, b
        return b
    def _f(self, a, b):
        # print '_f:', a, b
        c = (a & 65535) + (b & 65535)
        d = (a >> 16) + (b >> 16) + (c >> 16);
        # print '_f:', a, b, c, d, self._32_lshift(d, 16) | c & 65535
        # original: d << 16 | c & 65535
        return self._32_lshift(d, 16) | c & 65535
    def _g(self, a, b):
        # print '_g:', a, b
        # original: a << b | a >>> 32 - b
        return self._32_lshift(a, b) | self._zero_fill_right_shift(a, 32 - b)
    def _h(self, a, b, c, d, e, h):
        return self._f(self._g(self._f(self._f(b, a), self._f(d, h)), e), c)
    def _i(self, a, b, c, d, e, f, g):
        __i = self._h(b & c | ~b & d, a, b, e, f, g)
        # print '_i:', __i
        return __i
    def _j(self, a, b, c, d, e, f, g):
        __j = self._h(b & d | c & ~d, a, b, e, f, g)
        # print '_j:', __j
        return __j
    def _k(self, a, b, c, d, e, f, g):
        __k = self._h(b ^ c ^ d, a, b, e, f, g)
        # print '_k:', __k
        return __k
    def _l(self, a, b, c, d, e, f, g):
        return self._h(c ^ (b | ~d), a, b, e, f, g)
    def _m(self, a, b):
        # zero fill right shift: 64 >>> 9
        # print '_m (init):', a, b, b >> 5, (b + 64 >> 9 << 4)
        a = self.alist(a)
        a[b >> 5] |= 128 << b % 32
        a[(b + 64 >> 9 << 4) + 14] = b;
        # print '_m: a: %s, b: %s' % (a, b)
        c = 1732584193; d = -271733879; e = -1732584194; g = 271733878
        for h in range(0, len(a), 16):
            m = c; n = d; o = e; p = g;
            # print '_m ( for):', h, len(a), c, d, e, g
            c = self._i(c, d, e, g, a[h + 0], 7, -680876936); g = self._i(g, c, d, e, a[h + 1], 12, -389564586); 
            e = self._i(e, g, c, d, a[h + 2], 17, 606105819); d = self._i(d, e, g, c, a[h + 3], 22, -1044525330)
            
            c = self._i(c, d, e, g, a[h + 4], 7, -176418897); g = self._i(g, c, d, e, a[h + 5], 12, 1200080426);
            e = self._i(e, g, c, d, a[h + 6], 17, -1473231341); d = self._i(d, e, g, c, a[h + 7], 22, -45705983)
            
            c = self._i(c, d, e, g, a[h + 8], 7, 1770035416); g = self._i(g, c, d, e, a[h + 9], 12, -1958414417); 
            e = self._i(e, g, c, d, a[h + 10], 17, -42063); d = self._i(d, e, g, c, a[h + 11], 22, -1990404162)
            
            c = self._i(c, d, e, g, a[h + 12], 7, 1804603682); g = self._i(g, c, d, e, a[h + 13], 12, -40341101); 
            e = self._i(e, g, c, d, a[h + 14], 17, -1502002290); d = self._i(d, e, g, c, a[h + 15], 22, 1236535329)
            
            c = self._j(c, d, e, g, a[h + 1], 5, -165796510); g = self._j(g, c, d, e, a[h + 6], 9, -1069501632); 
            e = self._j(e, g, c, d, a[h + 11], 14, 643717713); d = self._j(d, e, g, c, a[h + 0], 20, -373897302)
            
            c = self._j(c, d, e, g, a[h + 5], 5, -701558691); g = self._j(g, c, d, e, a[h + 10], 9, 38016083); 
            e = self._j(e, g, c, d, a[h + 15], 14, -660478335); d = self._j(d, e, g, c, a[h + 4], 20, -405537848)
            
            c = self._j(c, d, e, g, a[h + 9], 5, 568446438); g = self._j(g, c, d, e, a[h + 14], 9, -1019803690); 
            e = self._j(e, g, c, d, a[h + 3], 14, -187363961); d = self._j(d, e, g, c, a[h + 8], 20, 1163531501)
            
            c = self._j(c, d, e, g, a[h + 13], 5, -1444681467); g = self._j(g, c, d, e, a[h + 2], 9, -51403784); 
            e = self._j(e, g, c, d, a[h + 7], 14, 1735328473); d = self._j(d, e, g, c, a[h + 12], 20, -1926607734)
            
            c = self._k(c, d, e, g, a[h + 5], 4, -378558); g = self._k(g, c, d, e, a[h + 8], 11, -2022574463)
            e = self._k(e, g, c, d, a[h + 11], 16, 1839030562); d = self._k(d, e, g, c, a[h + 14], 23, -35309556)
            
            c = self._k(c, d, e, g, a[h + 1], 4, -1530992060); g = self._k(g, c, d, e, a[h + 4], 11, 1272893353)
            e = self._k(e, g, c, d, a[h + 7], 16, -155497632); d = self._k(d, e, g, c, a[h + 10], 23, -1094730640)
            
            c = self._k(c, d, e, g, a[h + 13], 4, 681279174); g = self._k(g, c, d, e, a[h + 0], 11, -358537222)
            e = self._k(e, g, c, d, a[h + 3], 16, -722521979); d = self._k(d, e, g, c, a[h + 6], 23, 76029189)
            
            c = self._k(c, d, e, g, a[h + 9], 4, -640364487); g = self._k(g, c, d, e, a[h + 12], 11, -421815835)
            e = self._k(e, g, c, d, a[h + 15], 16, 530742520); d = self._k(d, e, g, c, a[h + 2], 23, -995338651)
            
            c = self._l(c, d, e, g, a[h + 0], 6, -198630844); g = self._l(g, c, d, e, a[h + 7], 10, 1126891415)
            e = self._l(e, g, c, d, a[h + 14], 15, -1416354905); d = self._l(d, e, g, c, a[h + 5], 21, -57434055)
            
            c = self._l(c, d, e, g, a[h + 12], 6, 1700485571); g = self._l(g, c, d, e, a[h + 3], 10, -1894986606)
            e = self._l(e, g, c, d, a[h + 10], 15, -1051523); d = self._l(d, e, g, c, a[h + 1], 21, -2054922799)
            
            c = self._l(c, d, e, g, a[h + 8], 6, 1873313359); g = self._l(g, c, d, e, a[h + 15], 10, -30611744)
            e = self._l(e, g, c, d, a[h + 6], 15, -1560198380); d = self._l(d, e, g, c, a[h + 13], 21, 1309151649)
            
            c = self._l(c, d, e, g, a[h + 4], 6, -145523070); g = self._l(g, c, d, e, a[h + 11], 10, -1120210379)
            e = self._l(e, g, c, d, a[h + 2], 15, 718787259); d = self._l(d, e, g, c, a[h + 9], 21, -343485551)
            
            c = self._f(c, m); d = self._f(d, n); e = self._f(e, o); g = self._f(g, p)
        # print '_m:', a, b, c, d, e, g
        return [c, d, e, g]
    def _n(self, a):
        return self._e(self._m(self._d(a), len(a) * 8))

    def G(self, a):
        # print 'G:', a
        return self._b(self._n(self._c(a, self.E)))

    def H(self):
        import random
        a = round(random.random() * 1e10)
        # print 'H:', '%010d' % a
        return '%010d' % a

    def I(self, a):
        b = a[0:2]; c = a[2:12]; d = a[12:22]; e = a[22:44]; f = int(c) + self.D; g = self.H(); 
        # print 'I:', a, b, c, d, e, f, g
        h = self.G(e + str(f) + g);
        # print 'I:', a, b, c, d, e, f, g, h
        # return b + c + d + str(f) + g + h
        return "05" + b + c + d + str(f) + g + h

    def J(self):
        import time
        # print 'J:', int(time.mktime(time.gmtime()))
        return int(time.mktime(time.gmtime()))
    
    def K(self, a):
        b = a[0:2]; c = a[2:1]; d = a[3:10]; e = a[13:10]; f = a[24:22]
        g = self.J() + self.D; 
        h = self.H(); 
        i = self.G(f + str(g) + h)
        # print 'K:', a, b, c, d, e, f, g, h, i
        return b + c + d + e + str(g) + h + i
    
    def L(self, a):
        b = '04'; c = '03'; d = ''; e = a[0:2]
        # print 'L:', a, b, c, d, e
        return (e == b and self.K(a)
             or e == c and self.I(a)
             or d)
