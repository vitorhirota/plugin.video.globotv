#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re
from random import randrange
import json
import sys

base_url = 'http://globotv.globo.com'
show_url = base_url + '%s'
rail_url = show_url + '/_/trilhos/%s/page/%s'
info_url = 'http://api.globovideos.com/videos/%s/playlist/callback/wmPlayerPlaylistLoaded'

from StringIO import StringIO
import gzip

print '+ Test for sections and their shows'
request = urllib2.Request(base_url)
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
shows = {}
# match slug, category name and list of shows
match=re.compile('<h4 data-tema-slug="(.+?)">(.+?)<span[\s\S]+?<ul>([\s\S]+?)</ul>').findall(data)
print len(match), 'sections'
for m in match:
	# match show url, names and thumb and build a dict with all the info
	match_shows=re.compile('<a href="(.+?)".*programa="(.+?)">[\s\S]+?<img data-src="(.+?)"').findall(m[2])
	shows[m[0]] = {'title': m[1], 'shows': match_shows}
	_str = ''
	for m1 in match_shows:
		_str = _str + m1[1] + ', '
	print 'Category %s' % m[1]
	print ' ', len(match_shows), 'shows:', _str[:-2]

if not len(match):
	print 'no shows found'
	print data
	sys.exit()
print

# for debug purposes
# match = [
# 	# ('novelas', 'Novelas'), 
# 	# ('jornalismo', 'Jornalismo'), 
# 	# ('variedades', 'Variedades'), 
# 	# ('series', 'S\xc3\xa9ries'), 
# 	# ('esportes', 'Esportes'), 
# 	# ('moda-e-beleza', 'Moda e Beleza'), 
# 	# ('receitas', 'Receitas'), 
# 	# ('musica', 'M\xc3\xbasica'), 
# 	# ('humor', 'Humor'), 
# 	# ('comportamento', 'Comportamento'), 
# 	# ('saude', 'Sa\xc3\xbade'), 
# 	# ('casa', 'Casa'), 
# 	('educacao', 'Educa\xc3\xa7\xc3\xa3o'), 
# 	# ('viagens', 'Viagens'), 
# 	# ('sensual', 'Sensual')
# ]
# shows = {
# 	'casa': {
# 		'shows': [
# 			('/gnt/decora', 'Decora', 'http://s2.glbimg.com/osSGNhWnxbMNU8KltUtyxlTyJvX1YyMbN4p3vhlt3KJZQblVq4UZG8Ffw4DT_GNo/s.glbimg.com/vi/mk/program/5175/logotipo_xs/1/45x34.png'),
# 			('/gnt/santa-ajuda', 'Santa Ajuda', 'http://s2.glbimg.com/oiMg9JpHwvcr3pKt2h2gd3vTX3t-VKtScLVWRVHbIRxJ4mUeOno74eCC-mSjQIyk/s.glbimg.com/vi/mk/program/5362/logotipo_xs/1/45x34.png'),
# 			('/gnt/casa-brasileira', 'Casa Brasileira', 'http://s2.glbimg.com/T2RYVFbY8KR4q-DU_K8u1KwXdmR12ZhuiSTIBhrcIFsrK5lJAoOIa2fX3cxw6zd3/s.glbimg.com/vi/mk/program/5059/logotipo_xs/1/45x34.png'),
# 			('/gnt/casa-gnt', 'Casa GNT', 'http://s2.glbimg.com/RZVtihJ4UuHgoR5mlHRCc8uhu33YVEXtuBSyvoo3YCS_QK2-fqmneorSeoIhaCoT/s.glbimg.com/vi/mk/program/5406/logotipo_xs/1/45x34.png'),
# 			('/gnt/nos-trinques', 'Nos Trinques', 'http://s2.glbimg.com/49g2lpfSqVNDI1klksfQTBjMO-zv8Ws8Di_Fch_C3OgVxvCImDslzDGgDlLo1YbE/s.glbimg.com/vi/mk/program/5164/logotipo_xs/1/45x34.png'),
# 			('/gnt/lar-doce-lar', 'Lar Doce Lar', 'http://s2.glbimg.com/TvwlckRKa45AYC5ARiNXRVwgMeIomfNnW0ByO6fdErJZy-nHXflz0Sjf5zLwgrNu/s.glbimg.com/vi/mk/program/5502/logotipo_xs/1/45x34.png')],
# 		'title': 'Casa' },
# 	'comportamento': {
# 		'shows': [
# 			('/gnt/sessao-de-terapia', 'Sess\xc3\xa3o de Terapia', 'http://s2.glbimg.com/eyt1bTYWHS3GdLWsW5cmgfcaW9pK1gRBYrbP7giXZ5aK7OKxK6ARnbAAj-TGMMxB/s.glbimg.com/vi/mk/program/7004/logotipo_xs/2/45x34.png'),
# 			('/gnt/chegadas-e-partidas', 'Chegadas e Partidas', 'http://s2.glbimg.com/bBoCr_rN13qPCGXb2OfnqagPCL-Mxcsb1SrGpddPbLpd-u-4nPmaT1zPYsY1G-sq/s.glbimg.com/vi/mk/program/5176/logotipo_xs/2/45x34.png'),
# 			('/gnt/amor-e-sexo-gnt', 'Amor e Sexo GNT', 'http://s2.glbimg.com/LLiHgQ2ysvcbsXRN7VgvaFrTJwyWBiPF46dk3hVa9v444QVJnlT4SfigYDpGGDOu/s.glbimg.com/vi/mk/program/5405/logotipo_xs/1/45x34.png'),
# 			('/gnt/viver-com-fe', 'Viver com F\xc3\xa9', 'http://s2.glbimg.com/rEBi4af300zWGhZpx-9OGw2lmdV5E7XtEeJAGJGLaEMO1cD8v_En36ikFY7oXECU/s.glbimg.com/vi/mk/program/5781/logotipo_xs/1/45x34.png'),
# 			('/gnt/chuva-de-arroz', 'Chuva de Arroz', 'http://s2.glbimg.com/eTYiVv09y3xWFL3lMvrIftFyCNe7VaTm3HRx-idVecEnDvLmIm867n3L4TgBOmqp/s.glbimg.com/vi/mk/program/5561/logotipo_xs/1/45x34.png'),
# 			('/gnt/saia-justa', 'Saia Justa', 'http://s2.glbimg.com/x_6u8pDatB3FuGNdOFq0a6nccePscw2rVxmmjKGge-z8c-AntPzs0HdbfuT63EfK/s.glbimg.com/vi/mk/program/2673/logotipo_xs/1/45x34.png'),
# 			('/gnt/cartas-na-mesa', 'Cartas na Mesa', 'http://s2.glbimg.com/PHSTT_idDnq24tJc6yE8sVRg4RPIjkNJw51E4bFLWgQXa_d_gmWm_GPruSOQtSBc/s.glbimg.com/vi/mk/program/6952/logotipo_xs/1/45x34.png'),
# 			('/gnt/viva-voz', 'Viva Voz', 'http://s2.glbimg.com/at-_b3QzVi_W6HFVDkozlriZAu-Q22zLxK4QeQxh_Wyb1scdKFocjBuwTp83gHSb/s.glbimg.com/vi/mk/program/5324/logotipo_xs/1/45x34.png'),
# 			('/canal-off/off-films', 'Off Films', 'http://s2.glbimg.com/kP9gTXNOJo_rSFeI8Vl-JBc8KV7nC5Shy9JSKNZ2AYqFElWUWC_K3j4Njf3c-qH7/s.glbimg.com/vi/mk/program/5582/logotipo_xs/1/45x34.png'),
# 			('/canal-off/pela-rua', 'Pela Rua', 'http://s2.glbimg.com/B3HTlZMd9L14CTsXZOAuqXfhbn2i3D-BbqTNcanjo_P0ks0fuLXZqdbMrc6tyZ4_/s.glbimg.com/vi/mk/program/5574/logotipo_xs/2/45x34.png'),
# 			('/canal-off/off-mais', 'Off Mais', 'http://s2.glbimg.com/pHDSPDnubzv1ElEZTLcIeWW9ggBIFCLA4Eug7j8Go9ldJpcJyn9_yjF89mwOlKib/s.glbimg.com/vi/mk/program/5779/logotipo_xs/1/45x34.png'),
# 			('/canal-off/na-onda', 'Na Onda', 'http://s2.glbimg.com/4spgM4x8Qv5sGTcHXUozTN1hHPtNqR1NC-LWyXw_-m4VTj4eeYJnL4Hr7Ttdvyaq/s.glbimg.com/vi/mk/program/5726/logotipo_xs/2/45x34.png'),
# 			('/multishow/bastidores', 'Bastidores', 'http://s2.glbimg.com/bwtvlCsrVnpBoXhzZgx665OUO8oEwa479vDxE3jer_NFxfCSBbKltjsSNxNXKr10/s.glbimg.com/vi/mk/program/3446/logotipo_xs/1/45x34.png'),
# 			('/multishow/conexoes-urbanas', 'Conex\xc3\xb5es Urbanas', 'http://s2.glbimg.com/By3xwrf9z5kQsp2wNFyMNKySmsf3RP6dHFEVEJm2UPOS7WBwlDR9PFfBkgFdoTpz/s.glbimg.com/vi/mk/program/4588/logotipo_xs/1/45x34.png'),
# 			('/canal-off/secret-spots', 'Secret Spots', 'http://s2.glbimg.com/thVnRh9rzQBpMMrtbg2Sd-UKpIfXvGLHxwq-E-SvgAEDeu8_PrVCFYxrFrbygYBF/s.glbimg.com/vi/mk/program/5577/logotipo_xs/2/45x34.png'),
# 			('/canal-off/a-vida-que-eu-queria', 'A Vida Que Eu Queria', 'http://s2.glbimg.com/TdEdGRVG9W5nYCHz2MzIt4DeHb5ADmMK1DoH2BrZ5DjJIDYKXmk_H0lUixMwN_JC/s.glbimg.com/vi/mk/program/5576/logotipo_xs/2/45x34.png'),
# 			('/canal-off/off-docs', 'Off Docs', 'http://s2.glbimg.com/ufJIvBvkmWIC0Kim3kFho6qTT9H7_GxYYuSuIo8nw7jwc3LTKx1f9pjPJCZ6j0Zp/s.glbimg.com/vi/mk/program/5581/logotipo_xs/1/45x34.png'),
# 			('/canal-off/submerso', 'Submerso', 'http://s2.glbimg.com/qFm95reBYZs8uLC7afCGbOl9IQX0RS-QZrG4oHZQRxVBw-C3Sq3y5rnlgH2yztwR/s.glbimg.com/vi/mk/program/5580/logotipo_xs/2/45x34.png'),
# 			('/canal-off/snow-camp', 'Snow Camp', 'http://s2.glbimg.com/T4e5OxHrnAvfpn-9Xoz63QlZ3LNZk6A-WdPok3_TiXF4o-O_qfaUMqT2DyDJ_s8E/s.glbimg.com/vi/mk/program/5578/logotipo_xs/2/45x34.png'),
# 			('/multishow/papo-de-policia', 'Papo de Pol\xc3\xadcia', 'http://s2.glbimg.com/MTCmBwvwfFvj5GZTU64f2orf8MRVgswzzC7gbGqrPOL6EqFlBp_LTLFzXzKLKBua/s.glbimg.com/vi/mk/program/5142/logotipo_xs/2/45x34.png'),
# 			('/canal-off/desejar-profundo', 'Desejar Profundo', 'http://s2.glbimg.com/42oxjVaUwAyM3gVucpREp7MJnqCQFmVaatBeiPQiwoKOjKrUS_NZDpLITRLo3oec/s.glbimg.com/vi/mk/program/5575/logotipo_xs/2/45x34.png'),
# 			('/multishow/serguei-rock-show', 'Serguei Rock Show', 'http://s2.glbimg.com/DXSeuPVGudnQksEiojcL584svZxqRiiSi8-Iy67vRbHOr484WSWQhEI2du64CuHo/s.glbimg.com/vi/mk/program/5177/logotipo_xs/1/45x34.png'),
# 			('/canal-off/off-kaiak', 'Off Kaiak', 'http://s2.glbimg.com/_cT42N6GH78KX9isybVLwzQ3FAnvvnND7lW3Y8cfmaHE-sDfFlxnQr8pvM1OT5iF/s.glbimg.com/vi/mk/program/5583/logotipo_xs/2/45x34.png'),
# 			('/canal-off/focused', 'Focused', 'http://s2.glbimg.com/OlFJ8Bnfznt981pqXE4pNshJKRiZEwvu7F2Usn8XlcejuJXnbjZa73Tbq54tqncZ/s.glbimg.com/vi/mk/program/5791/logotipo_xs/1/45x34.png'),
# 			('/gnt/londres-assim', 'Londres Assim', 'http://s2.glbimg.com/G6xOERJcnA8V-tDrbkUo6k_eaHjXQ2sfTCHp8RgoOy6e_byM3KB2TtFAzgtSTQ7S/s.glbimg.com/vi/mk/program/6968/logotipo_xs/1/45x34.png'),
# 			('/canal-off/sem-asas', 'Sem Asas', 'http://s2.glbimg.com/nhQX-ihbyhk3cwDyFL_87SrwsGgpQ_M4Xyz-1MzH8rzobF2B24s7R66NEMZqd-Bb/s.glbimg.com/vi/mk/program/5579/logotipo_xs/2/45x34.png'),
# 			('/gnt/pirei', 'Pirei', 'http://s2.glbimg.com/lZUZNmijHxgZK-3-FJbsavOK9vLcw7JQHLSg4IobZsapJfdiTpWJLK5SDe-N5dAl/s.glbimg.com/vi/mk/program/4821/logotipo_xs/1/45x34.png'),
# 			('/gnt/em-busca-do-pai', 'Em Busca do Pai', 'http://s2.glbimg.com/dvAAO790jdba4KknkinEwiqWPVg5WzMB2s2o7ylnfxPteXPp1mt-r-FyZ3hvctnX/s.glbimg.com/vi/mk/program/7005/logotipo_xs/1/45x34.png'),
# 			('/canal-off/nomads', 'Nomads', 'http://s2.glbimg.com/xEhIG-ardRHmVNn83YHJNHjbpAYnx2MZ--VfY7nbrxLcFHPvx_qPHWCjcGx-QKUq/s.glbimg.com/vi/mk/program/5798/logotipo_xs/1/45x34.png'),
# 			('/canal-off/asp-mens-world-tour', 'ASP Men\xc2\xb4s World Tour', 'http://s2.glbimg.com/-K7tzun9KVweo12bkvBwXlxoQtezhnrymFf4Y1TdWbpSFq8kZHKqEGNyH9Ecva4A/s.glbimg.com/vi/mk/program/5572/logotipo_xs/1/45x34.png'),
# 			('/multishow/skins', 'Skins', 'http://s2.glbimg.com/tOWZyidptQB8VVsCktZB-KCilu9qZIZLXAs1HLFuOOoaL6TqCe1cSB6E7s9GX3ex/s.glbimg.com/vi/mk/program/5556/logotipo_xs/1/45x34.png'),
# 			('/canal-off/4-surfing', '4 Surfing', 'http://s2.glbimg.com/as0rsF8_Bzs50jINoLw3WAdsWW3jZyEssi2ALjUHReNRUydn1fazq0yEF9A_z0il/s.glbimg.com/vi/mk/program/5567/logotipo_xs/1/45x34.png'),
# 			('/canal-off/summer-dew-tour', 'Summer Dew Tour', 'http://s2.glbimg.com/-bboqKESAeh1aUNHN-JxVjPT1JgePJV2FO3VMDzf04n8SNe5qeSrUFPfO2laitw4/s.glbimg.com/vi/mk/program/5640/logotipo_xs/1/45x34.png'),
# 			('/gnt/detox-do-amor', 'Detox do Amor', 'http://s2.glbimg.com/OGEicHlTizORSvDDc39qWCg4cmI7JhxnH1uid8iNNWlO44wEuQuAQMYfZ3wgoc6s/s.glbimg.com/vi/mk/program/5313/logotipo_xs/1/45x34.png'),
# 			('/multishow/bicicleta-e-melancia', 'Bicicleta e Melancia', 'http://s2.glbimg.com/GZVkrJvbdeXR9dzgycKfY48oTaE-mXSlLiYK1lyp9ndDbc2Z7dWAmZbqVrHpa62o/s.glbimg.com/vi/mk/program/5060/logotipo_xs/2/45x34.png'),
# 			('/canal-off/cliff-diving-world-series', 'Cliff Diving World Series', 'http://s2.glbimg.com/CBozehG75ZUEMYnFq6aQUARbdP5AS6OSvIMTVJQttMzDEJhAnncPS7Sc1x5JhtgS/s.glbimg.com/vi/mk/program/5570/logotipo_xs/3/45x34.png'),
# 			('/gnt/marias', 'Marias', 'http://s2.glbimg.com/2MiXw2SXEvU-QK4OgD9HJhZ-5HdIPvAJysXC3whLCAf2Fuo32qSPPgEeF_TXEZSE/s.glbimg.com/vi/mk/program/7185/logotipo_xs/1/45x34.png'),
# 			('/canal-off/winter-dew-tour', 'Winter Dew Tour', 'http://s2.glbimg.com/1kX2r8VEoS9H-3kw1HEpbGPbHisMvCkdqHU_QIv2ySHD_JbEA1tI6J31S53n9hoI/s.glbimg.com/vi/mk/program/5655/logotipo_xs/2/45x34.png'),
# 			('/canal-off/on-the-loose', 'On the Loose', 'http://s2.glbimg.com/CyVz9uy9zRa_mJId8GD3GXic5jQpP76hOmsZ4MOjcIltlDrg8cQucI31MinBjbwV/s.glbimg.com/vi/mk/program/5568/logotipo_xs/2/45x34.png')],
# 		'title': 'Comportamento' },
# 	'educacao': {
# 		'shows': [
# 			('/rede-globo/globo-ciencia', 'Globo Ci\xc3\xaancia', 'http://s2.glbimg.com/1_iMfnCj_ZpvP8tPmjrQyqS5z9NOn2h8FxpLVrimRykAaUFOPsnV8jDMUZdVQ85c/s.glbimg.com/vi/mk/program/2528/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/globo-universidade', 'Globo Universidade', 'http://s2.glbimg.com/2ojo74AyUePWj3LQ-wv6JAdgo5YjhioOpYZh2HU-Ig-cbh5iYI6abojQAPh6hgq8/s.glbimg.com/vi/mk/program/3663/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/globo-ecologia', 'Globo Ecologia', 'http://s2.glbimg.com/PnqrTb0CqvlBVrbFYOqOSsLMeoAks6SnOk64r_r0xiTelFEzNYHIlRUf4SRlPdsT/s.glbimg.com/vi/mk/program/2530/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/acao', 'A\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/DBPvnV4r4sVvuc9e9pESsKPhLkBeFYpk9hTnmQnmyRrpgOJpVNwCCmFZMDJ5NhKx/s.glbimg.com/vi/mk/program/2514/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/globo-educacao', 'Globo Educa\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/8PHAuAZUxR8fLezFexzAJtoV_rcpKvJNG8VO_xG3IRZCMR0YLnJZ55hRzlbWD0O3/s.glbimg.com/vi/mk/program/2531/logotipo_xs/2/45x34.png')],
# 		'title': 'Educa\xc3\xa7\xc3\xa3o' },
# 	'esportes': {
# 		'shows': [
# 			('/sportv/combate', 'Combate', 'http://s2.glbimg.com/rlGRONOph_oiaR32EpQrVdpjcxBs3QCYPk0E9P1B4XwkydvgWiu1J4r6Htgv94ff/s.glbimg.com/vi/mk/program/4692/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/globo-esporte-rj', 'Globo Esporte RJ', 'http://s2.glbimg.com/Pv-zhL_N4Q9Ncu7B1LglImY--zWUNYiblVPM2muEua-4zEM9F6HAys_8qSO25dh2/s.glbimg.com/vi/mk/program/5229/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/globo-esporte-sp', 'Globo Esporte SP', 'http://s2.glbimg.com/LWVoYA4loOzJqFt7jcoKcZONxj9UylYshakugDG5gN2wHcp9guD8pvLh7ur2nj2X/s.glbimg.com/vi/mk/program/4868/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/globo-esporte', 'Globo Esporte', 'http://s2.glbimg.com/UJycKxF8QIbp_p6-G4JGNcEL9hR-LJiOwdPh2k5K1XAq3Knko6h0wkaqdoqnNOHu/s.glbimg.com/vi/mk/program/815/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/formula-1', 'F\xc3\xb3rmula 1', 'http://s2.glbimg.com/dCOVJ7EaiOzDnwgS6gFp_JqCDuLUWPXc8UhbNmY3gffZBFMnqT7xvNTytLtnFHpZ/s.glbimg.com/vi/mk/program/3653/logotipo_xs/1/45x34.png'),
# 			('/sportv/sportvnews', 'SporTVNews', 'http://s2.glbimg.com/BAZzqKlvgPx0XFcd67gM_padBRQIHw6QStbDrfrMoNtASN0S7uyAHt04wjbGdNlU/s.glbimg.com/vi/mk/program/2674/logotipo_xs/1/45x34.png'),
# 			('/sportv/troca-de-passes', 'Troca de Passes', 'http://s2.glbimg.com/hVFdxoTMrjU9NMJ11B1Ve565c0vediMuBj3boVr06iFQi5hHQc6iGgb_oxFdw-ED/s.glbimg.com/vi/mk/program/3854/logotipo_xs/2/45x34.png'),
# 			('/sportv/redacao-sportv', 'Reda\xc3\xa7\xc3\xa3o SporTV', 'http://s2.glbimg.com/8COwyFzxysaWfcxTEzCFUX2lh3nT988usvbwfz27uKlIkf1mkkNhshSpJlV2K99p/s.glbimg.com/vi/mk/program/3849/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/globo-esporte-mg', 'Globo Esporte MG', 'http://s2.glbimg.com/sqBpiWimOz0tJEZWiTM0hsd1Dzxx4HImZ4SOJXvdX3R3TyCATDlYJ_XtD9of193o/s.glbimg.com/vi/mk/program/4222/logotipo_xs/1/45x34.png'),
# 			('/sportv/e-gol', '\xc3\x89 Gol!!!', 'http://s2.glbimg.com/hdnoBWWahP7amvGyoVvZgui_V-K9W6krQvK5cDDr3ebnIvtIskvcsrMwuKeKV-hX/s.glbimg.com/vi/mk/program/4784/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/globo-esporte-pe', 'Globo Esporte PE', 'http://s2.glbimg.com/3X5GWZZ68MW7oyai37DonsPB8fIUpLWEcm8bL2SW5LdI_toczz2Q9ss4MKC9qzNl/s.glbimg.com/vi/mk/program/5474/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/esporte-espetacular', 'Esporte Espetacular', 'http://s2.glbimg.com/QiBEJ7oJUUu_zF1PgzFFOZqG5A05dE1cqtm5BZ3O-KLO-p5FGB-tLscI0TOT5O-d/s.glbimg.com/vi/mk/program/813/logotipo_xs/1/45x34.png'),
# 			('/sportv/ta-na-area', 'T\xc3\xa1 na \xc3\x81rea', 'http://s2.glbimg.com/dzKuKHcdUKPUxE0KjqUHGLYYqWApIVodtaEJEupaboqmZOOpGt99Kx0obFnB1Nzj/s.glbimg.com/vi/mk/program/3862/logotipo_xs/2/45x34.png'),
# 			('/sportv/arena-sportv', 'Arena SporTV', 'http://s2.glbimg.com/BTPBL_rycUCtMcHXZiOCucYuSotQs_owoTzNF8SepVYnJnejEVrts91-tmBkgyFC/s.glbimg.com/vi/mk/program/3850/logotipo_xs/5/45x34.png'),
# 			('/sportv/bem-amigos', 'Bem, Amigos!', 'http://s2.glbimg.com/M8xqur3xXsGLmhynojZnRmzC0o1oXJ27pAPW2p3pYtCJHEQfPpK464l7k4XBYjW2/s.glbimg.com/vi/mk/program/3855/logotipo_xs/1/45x34.png'),
# 			('/sportv/sensei-sportv', 'Sensei SporTV', 'http://s2.glbimg.com/6Gt3x3oihSs7mTPffLt5fmso6lvj44aFhk7acA-d61jeT4rnFdQfJw2GHCL0FNnX/s.glbimg.com/vi/mk/program/4604/logotipo_xs/3/45x34.png'),
# 			('/sportv/sportv-reporter', 'SporTV Reporter', 'http://s2.glbimg.com/vi2lCd_G3FO-gqdrGSqg9kFtF7wvVW3QcHP2RiDVT372Q0_0J4HEoXsHED90NSqX/s.glbimg.com/vi/mk/program/4257/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/corujao-do-esporte', 'Coruj\xc3\xa3o do Esporte', 'http://s2.glbimg.com/Zsq_mH-g1uM4yBZhrXAsPsW5iTsgjTTyBWxF1Yga8aK5gsdc7mIDbvZx2xKwqAQn/s.glbimg.com/vi/mk/program/5149/logotipo_xs/1/45x34.png'),
# 			('/sportv/linha-de-chegada', 'Linha de Chegada', 'http://s2.glbimg.com/rmIw_IY6tWYkP34vTKMUw1pumFhYmX8amZxJzFM2EvdI4RLvCdAtFp_6-xnQe9Di/s.glbimg.com/vi/mk/program/3851/logotipo_xs/1/45x34.png'),
# 			('/sportv/zona-de-impacto', 'Zona de Impacto', 'http://s2.glbimg.com/ijcK6lfMD4w1TYMDCqANJs4YU5plaTDhE0mwSynYX4bf0TZIZFHWptI3PJy_J9-I/s.glbimg.com/vi/mk/program/3483/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/the-ultimate-fighter-brasil', 'The Ultimate Fighter Brasil', 'http://s2.glbimg.com/JG4rWcWD373FTkjAJeT49G1Wwe05T7zv1KicxLeawg51e8KBOOr32Id7j_h5biZy/s.glbimg.com/vi/mk/program/5774/logotipo_xs/1/45x34.png'),
# 			('/sportv/programa-do-socio', 'Programa do S\xc3\xb3cio', 'http://s2.glbimg.com/GVnBFoplIIPk70jWn21tsoYoKpa3S8M7DSVQVla_ReGLvqjeX6NwANBb-ksC2HZ6/s.glbimg.com/vi/mk/program/5012/logotipo_xs/1/45x34.png'),
# 			('/sportv/expresso-do-esporte', 'Expresso do Esporte', 'http://s2.glbimg.com/VkkCMe8onad9dhSMHKFAzOS0d3oSKHYPNFY019XsZsJsxxRo_KdeHHUj7aPmagPJ/s.glbimg.com/vi/mk/program/3738/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/brasileirao-2012', 'Brasileir\xc3\xa3o 2012', 'http://s2.glbimg.com/nY2sQ4Arv9sCr2pn0XD4uVL4cjz4NAd17f66OtgXQXgGSPXysB0dKD4jH0DTYjrM/s.glbimg.com/vi/mk/program/7169/logotipo_xs/2/45x34.png'),
# 			('/sportv/camarote', 'Camarote', 'http://s2.glbimg.com/cbSqrf_K4sDYLkqJ0agqSdVz5UVfa2KvRNBU9EwXa38KFLtUWGgoXGVaRn7X2C6z/s.glbimg.com/vi/mk/program/5041/logotipo_xs/1/45x34.png'),
# 			('/sportv/fora-do-eixo', 'Fora do Eixo', 'http://s2.glbimg.com/gHY_yVsBKgcjwRAeMpOC1Badu-HvZx5QO9HmQXDxJRpx5Nl51C3Ujwt1NaNMwg5y/s.glbimg.com/vi/mk/program/4158/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/jogos-para-sempre', 'Jogos para Sempre', 'http://s2.glbimg.com/YxN7ifK3KnATrKHD3xJmoJFNiGNn494vTXKgjm8mOBWOuGSRXk9KNx_nXNXM6SNz/s.glbimg.com/vi/mk/program/7066/logotipo_xs/1/45x34.png'),
# 			('/sportv/rumo-a-londres', 'Rumo a Londres', 'http://s2.glbimg.com/6nhaPiXnni_ZOjMmsOxO3of04kOEPmbPfBciWPd3KrTkdDzjVnnV-Szb8aWkpoO_/s.glbimg.com/vi/mk/program/5040/logotipo_xs/1/45x34.png')],
# 		'title': 'Esportes' },
# 	'humor': {
# 		'shows': [
# 			('/multishow/220-volts', '220 Volts', 'http://s2.glbimg.com/N9xibVr2T1OrMEUUiqYmp932eMrs_JXYxawhkYbIQdMUTlvxLtBqF2Tzbcao5vZb/s.glbimg.com/vi/mk/program/5489/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/larica-total', 'Larica Total', 'http://s2.glbimg.com/uJvxvkPUTrW-R60y4EzeD7w4uvA1PYz0kZ4VqX57Iq1uR4arYfDgqs1pwCjftoon/s.glbimg.com/vi/mk/program/4647/logotipo_xs/1/45x34.png'),
# 			('/multishow/sensacionalista', 'Sensacionalista', 'http://s2.glbimg.com/8a2iBHOnEa5tJanGoCjdWDfVbQgddv1VGxQ7eftMAgfp-R8nYUjCjMlTpDFbJ6Q2/s.glbimg.com/vi/mk/program/5168/logotipo_xs/1/45x34.png'),
# 			('/multishow/cilada', 'Cilada', 'http://s2.glbimg.com/lA6EimsMI6fRcw1kxTlV2M614bePJ79yJlpywLMDRolBT4i_9oYGmQMpvGgRz5td/s.glbimg.com/vi/mk/program/3956/logotipo_xs/2/45x34.png'),
# 			('/multishow/olivias-na-tv', 'Ol\xc3\xadvias na TV', 'http://s2.glbimg.com/NRzLtRM1f8B26fyHEYmrGAD6sDTyob4eCP0d7s5CQ7gWi8yFptfBjjIUN47CCY00/s.glbimg.com/vi/mk/program/5254/logotipo_xs/1/45x34.png'),
# 			('/multishow/ate-que-faz-sentido', 'At\xc3\xa9 Que Faz Sentido', 'http://s2.glbimg.com/kr9QMs70IeSOikftUVK8Yp2fUCO5iOyiwE-MAbaaOfiq7uodW83wFCTDkmJcBdOc/s.glbimg.com/vi/mk/program/5344/logotipo_xs/2/45x34.png'),
# 			('/multishow/vida-de-mallandro', 'Vida de Mallandro', 'http://s2.glbimg.com/VY0esGpjyjUzJXVRiq2bIQhV3p-NE1eCA9bA-9am2vDsIfUqZHWcKPkUlAlLwwJG/s.glbimg.com/vi/mk/program/5788/logotipo_xs/1/45x34.png'),
# 			('/multishow/i-love-my-nerd', 'I Love My Nerd', 'http://s2.glbimg.com/QC_GkP2GGjseXwFNbHj7VXZposzF1XAZGu9nPTLFaWeqUMMRmJ7_lILPlTQQdISq/s.glbimg.com/vi/mk/program/5065/logotipo_xs/1/45x34.png'),
# 			('/multishow/adoravel-psicose', 'Ador\xc3\xa1vel Psicose', 'http://s2.glbimg.com/UIjt7Kw5SqVjD9cg4oUCrSUFDVMCmAY-bZ7HrbFYBw4WSI9wzdXeHFq8_lCsjPZo/s.glbimg.com/vi/mk/program/5051/logotipo_xs/1/45x34.png'),
# 			('/multishow/morando-sozinho', 'Morando Sozinho', 'http://s2.glbimg.com/7psCyjU-BWm50AgYB-mIOajSGa7lAVkGMoXk4YXEygyrbj9fe9-wCR3LE-IhiMmn/s.glbimg.com/vi/mk/program/5055/logotipo_xs/1/45x34.png'),
# 			('/multishow/de-cara-limpa', 'De Cara Limpa', 'http://s2.glbimg.com/sa5q0TS0rnpYZSGLvxIxWLAPvYu9FCkOjAzx88W5co0pgP1UTqsfqClhWsYggt5G/s.glbimg.com/vi/mk/program/4871/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/mateus-o-balconista', 'Mateus, O Balconista', 'http://s2.glbimg.com/OacmGQMqM5jR6JqfCx3nBZpQIUU9uxo2a8AKsRCtfY0UVBw6Yd1PbFmXdDN11KeM/s.glbimg.com/vi/mk/program/5440/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/sem-frescura', 'Sem Frescura', 'http://s2.glbimg.com/020k0ENLMrUlmLdemmuYar2fds0g1SgvvSM5-hSDgI1SdzkFMPnb2QEGUbD9N_Od/s.glbimg.com/vi/mk/program/4631/logotipo_xs/2/45x34.png'),
# 			('/multishow/os-buchas', 'Os buchas', 'http://s2.glbimg.com/zwAkznbbF1ocmqvqZDyQaoy06etwPFDrrAOUbDUDs4mwqv4T6LrjwKu-XQd7rG0L/s.glbimg.com/vi/mk/program/5776/logotipo_xs/1/45x34.png'),
# 			('/multishow/ed-mort', 'Ed Mort', 'http://s2.glbimg.com/CyVYF0jxIv7zWy2W3QV7rscoNv8F2Dn0A5dEmydfxf_rsJ_XJHxbPQbBEgps2SaB/s.glbimg.com/vi/mk/program/5555/logotipo_xs/1/45x34.png'),
# 			('/multishow/sera-que-faz-sentido', 'Ser\xc3\xa1 que faz sentido?', 'http://s2.glbimg.com/wLqoUIO26flwnob9Ng7zJZMzFJcyjkTHYfbamRshOSbun1ibFR5CCF8A8pzyuQnt/s.glbimg.com/vi/mk/program/5085/logotipo_xs/2/45x34.png'),
# 			('/multishow/os-gozadores', 'Os Gozadores', 'http://s2.glbimg.com/8ljYCDmtjlKaeSxKRWIRA9z92H30kvdX00Rbba8DbH_Pc3yJMN0CO8bUvXDotSYT/s.glbimg.com/vi/mk/program/5057/logotipo_xs/1/45x34.png'),
# 			('/multishow/open-bar', 'Open Bar', 'http://s2.glbimg.com/Lb77oHP75v8VjhCzQikd-adHwcXdpK-VIoZXMYRpO-UrFMlEGFZuCXWxXSy_zl5E/s.glbimg.com/vi/mk/program/5010/logotipo_xs/1/45x34.png'),
# 			('/multishow/muito-giro', 'Muito Giro', 'http://s2.glbimg.com/Jv15Jbw15zkvjRVjqGSF6lj-yDk6rUdG5zf_mB_PTBUXqZwvrazt1k7QJr8J4_Ov/s.glbimg.com/vi/mk/program/5437/logotipo_xs/1/45x34.png'),
# 			('/multishow/na-fama-e-na-lama', 'Na fama e na lama', 'http://s2.glbimg.com/UW1rw_L9HbOzuY2pXnlDlocslBS7TofNs1CEa72dHvaTE5p9Fgv5Mdd1LAzDVoDa/s.glbimg.com/vi/mk/program/5042/logotipo_xs/1/45x34.png'),
# 			('/multishow/de-cabelo-em-pe', 'De Cabelo em P\xc3\xa9', 'http://s2.glbimg.com/JrvfIjcQooSMKyaI4tJpAhA7-NJ2n2DNyw8UznzHtxQuI6eiJ_r9PtI6VrKsQTBw/s.glbimg.com/vi/mk/program/5345/logotipo_xs/1/45x34.png'),
# 			('/multishow/desenrola-ai', 'Desenrola a\xc3\xad', 'http://s2.glbimg.com/g6we-EsnBlh2TLUxb6nAv7miUDmZhIntGSTpIq6sUPo834MfyfIFACSiUZq6IWO5/s.glbimg.com/vi/mk/program/5066/logotipo_xs/1/45x34.png'),
# 			('/multishow/os-figuras', 'Os figuras', 'http://s2.glbimg.com/T3M1zEGyN61QsB1ygBB33tXEJGMalOazHP0jmivxugo358_gIt0Dgj6tlOSCnTqx/s.glbimg.com/vi/mk/program/5317/logotipo_xs/1/45x34.png')],
# 		'title': 'Humor' },
# 	'jornalismo': {
# 		'shows': [
# 			('/rede-globo/fantastico', 'Fant\xc3\xa1stico', 'http://s2.glbimg.com/QFBVEm6gI_BN-wBpiSsl-1gJ-Ch18jcPgY-xhAgEVaxc527SPloed08JQAVE3wWN/s.glbimg.com/vi/mk/program/814/logotipo_xs/1/45x34.png'),
# 			('/globo-news/jornal-globo-news', 'Jornal Globo News', 'http://s2.glbimg.com/jnrcfup_J-AR3OaaoirYgkwtWqnIX3xjChDtXfkSK0lJMwuReKMps2eyGyGPM5wo/s.glbimg.com/vi/mk/program/5050/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/jornal-nacional', 'Jornal Nacional', 'http://s2.glbimg.com/H9BWno1R8i7CptdA5j8q500qsdk3aq_tgGjvD3nRaeBFvP1sLqsg2yKDHPjtoF_3/s.glbimg.com/vi/mk/program/819/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/jornal-hoje', 'Jornal Hoje', 'http://s2.glbimg.com/lecTjhw36WSuMkaCfSbGXxFxH6SVvEP7Zv3CveThZ7XiijpJb3n30g5GYRePcj2F/s.glbimg.com/vi/mk/program/818/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/bom-dia-brasil', 'Bom Dia Brasil', 'http://s2.glbimg.com/iHDJO-NmwJiV33oqsWrAY7BVMVuN_95YLkX0YdlQ6e7fvih9Dhi5OqfO0e8c6a1U/s.glbimg.com/vi/mk/program/810/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/autoesporte', 'AutoEsporte', 'http://s2.glbimg.com/SWdqoPc45H3dUpJsoB1PfbcFcdLaC8KVixlytKKHVgDvvuaJGIi5RnAp-F6X8hWf/s.glbimg.com/vi/mk/program/2517/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/bem-estar', 'Bem Estar', 'http://s2.glbimg.com/-JCGTwmy_R1WtW2PQiiNJwuk35skXC6kZNx1herZRHjruM3Eae1XY7g8I_0TgS4-/s.glbimg.com/vi/mk/program/5147/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/globo-rural', 'Globo Rural', 'http://s2.glbimg.com/s8z4PVGEGS9CgrpuWfQRK4eaXsYN4Zqgq4S_9XUGrNgtCNn8KUeR9_Bevj0cJ3Wn/s.glbimg.com/vi/mk/program/1937/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/rjtv-1a-edicao', 'RJTV 1\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/vC61Y_mw8UA2q3c0-JlKpA16UuNz-QNTsCzRu-cNjVxMGJ5Q9ouBCr7WSDRTmaKT/s.glbimg.com/vi/mk/program/820/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/bom-dia-rio', 'Bom Dia Rio', 'http://s2.glbimg.com/DBrUWZDqrDKdW0qo9oPwSZrO9X_xOD2Fp-2FvNHQUG5Pncg5Ge-cm1vPiCFBI7Tm/s.glbimg.com/vi/mk/program/811/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/jornal-da-globo', 'Jornal da Globo', 'http://s2.glbimg.com/maYnEDklJ-tbHDCYiDIHrt1Y7FNSt3BmhDNRVMXuEUoy8fzw028X1-78wpiptfrD/s.glbimg.com/vi/mk/program/817/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/sptv-1a-edicao', 'SPTV 1\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/qKF6Amls_X8nf3UUkNveXfkGsxWsHaIy7wkSHPDoj_0qNqS5SKV1b3bhDMN1rPOq/s.glbimg.com/vi/mk/program/821/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/netv-1a-edicao', 'NETV - 1\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/lHjj04Ama0ass2OnRX6e65a3c-pBjRGabCex-qVIinqoj01miGv8IcY03V2J_dbW/s.glbimg.com/vi/mk/program/5456/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/mgtv-1a-edicao', 'MGTV 1\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/XFRV_i9ZUZOXOnsaerfr9WJWaTVWVGE4lPfqPXKchtGmO0hI4R-BjB0ulQgLJWJy/s.glbimg.com/vi/mk/program/2669/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/bom-dia-sao-paulo', 'Bom Dia S\xc3\xa3o Paulo', 'http://s2.glbimg.com/i4d3fnJA0l7a2DNm0nDyKNlZ1YqxWlOmkB1HaJw18gTGto544YPOOqLFLycxocbP/s.glbimg.com/vi/mk/program/812/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/sptv-2a-edicao', 'SPTV 2\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/GXSqJfBi2ljGi0Pxm9UDFUbvGUXmZu0sT-D5XE8bn1OdBUtaSft7ng82woBZaO9s/s.glbimg.com/vi/mk/program/4501/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/rjtv-2a-edicao', 'RJTV 2\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/cXMVQxxKTZvOSKbR5T84kuaH44A5anBPSxcznNfuvcZaFmgCjbhjPbUvKQZ1zQwj/s.glbimg.com/vi/mk/program/4388/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/bom-dia-minas', 'Bom Dia Minas', 'http://s2.glbimg.com/4PTNIq13lNi-0mC8q3Dkj-8hklRCC7cmFUMfypYmu263eQQvmPgWeOA699sFJQI4/s.glbimg.com/vi/mk/program/2664/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/mgtv-2a-edicao', 'MGTV 2\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/l6O-QshIKa7myimdY2jXWTrZdi0oIPDSNtZ7DasoOAlyeJAD4ZRJF-1tZe50HywX/s.glbimg.com/vi/mk/program/4365/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/globo-reporter', 'Globo Rep\xc3\xb3rter', 'http://s2.glbimg.com/FlOR_V9u4wzm96pJhZrF3XGAcNd8XhMX19hF3Fyn0eOZlHCxnW73qYw0zXzehn43/s.glbimg.com/vi/mk/program/816/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/profissao-reporter', 'Profiss\xc3\xa3o Rep\xc3\xb3rter', 'http://s2.glbimg.com/PQELq_OskAMn6DCfK9xzFyCEjrrYY5URvpT_XKmDiO3ouFSkxjqy4dLZokvWuG7_/s.glbimg.com/vi/mk/program/4263/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/dftv-2a-edicao', 'DFTV 2\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/VWj-ifYge2_lhRQyXYgX1XvGerPkvOEbXYWPWQvZQMkmbkSBUGFuuHrfeJWjgB8E/s.glbimg.com/vi/mk/program/4452/logotipo_xs/1/45x34.png'),
# 			('/globo-news/jornal-das-dez', 'Jornal das Dez', 'http://s2.glbimg.com/QrSBkbhq9kiAS9hWdQmWu5u6rU2hUjTxtiSQd4aMKzK6Xg5-unNaBVtx27AufoMP/s.glbimg.com/vi/mk/program/1702/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/pequenas-empresas-grandes-negocios', 'Pequenas Empresas, Grandes Neg\xc3\xb3cios', 'http://s2.glbimg.com/NxkEB-r1bG1Ry8cnIchtMEOtBshxYz5cKXE66GK2rIVStuOYohvJIa1ouQlnUkjR/s.glbimg.com/vi/mk/program/2537/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/netv-2a-edicao', 'NETV - 2\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/9LUeRA9y7KIDvW67pHnDbE_8bbDabAyVpHHg3xXyBsdMJWTe5V_h5oE8uxI95rqp/s.glbimg.com/vi/mk/program/5459/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/dftv-1a-edicao', 'DFTV 1\xc2\xaa Edi\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/PHjuHhQv9Kk4ZOn0Oo2_TG9gd-LQZVqtu2uTwfnBzf--JQOsd2m7qsQ-VwMKkJ_f/s.glbimg.com/vi/mk/program/3268/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/bom-dia-pe', 'Bom Dia PE', 'http://s2.glbimg.com/CVV_K7vb3k9RgSaVHHNMToBzjPudyevkBdTRnST8HiFnayTlBrlBOXrCCycv6vby/s.glbimg.com/vi/mk/program/5453/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/bom-dia-df', 'Bom Dia DF', 'http://s2.glbimg.com/P2XQONQGI7iJyyfHGfeX1IRlBeUjrw9-Lxza_QgD5T6MgkOHm-t9FBFZfew5KwhE/s.glbimg.com/vi/mk/program/3269/logotipo_xs/1/45x34.png'),
# 			('/globo-news/estudio-i', 'Est\xc3\xbadio i', 'http://s2.glbimg.com/j61Kc1X4b2JJH_2GqVgVWtM0xF7lwx7SUd92EmS1s36X2H_sSf80VHWCHAh5PoOn/s.glbimg.com/vi/mk/program/4585/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/terra-de-minas', 'Terra de Minas', 'http://s2.glbimg.com/9TrOZHSwKDtXKzViUzMgi23h5K9euZAUwbK_L0KYaQSeDUyCWXbT1B1yc2RqQd66/s.glbimg.com/vi/mk/program/4210/logotipo_xs/1/45x34.png'),
# 			('/globo-news/conta-corrente', 'Conta Corrente', 'http://s2.glbimg.com/cjdZBFRu7a4kdOHUJXvOT0xM0w1z2NDzbxcYhBpXE2dKIFXGbdY5Oog2Zum94zpG/s.glbimg.com/vi/mk/program/991/logotipo_xs/1/45x34.png'),
# 			('/globo-news/manhattan-connection', 'Manhattan Connection', 'http://s2.glbimg.com/xo1RlPPOo7yTwsZEdy9bo6KUuthx1-A5BZmNnRfYi84Jromdo55sGxO1blSjZiom/s.glbimg.com/vi/mk/program/5117/logotipo_xs/1/45x34.png'),
# 			('/globo-news/mundo-sa', 'Mundo S/A', 'http://s2.glbimg.com/p21wekso04tBTvi_GYGSJEz-THyEKeo5--T80ZgTtPFdESgzty5yKqsO8sOqEdNV/s.glbimg.com/vi/mk/program/4237/logotipo_xs/1/45x34.png'),
# 			('/globo-news/globo-news-em-pauta', 'Globo News em Pauta', 'http://s2.glbimg.com/TII2QjtiuMRafqjf6rexxXuJjPGzPsTQK2xb_pdIHLrd11ttRv_hdHGKK1925G1X/s.glbimg.com/vi/mk/program/4996/logotipo_xs/3/45x34.png'),
# 			('/globo-news/globo-news-painel', 'Globo News Painel', 'http://s2.glbimg.com/NMVjnL7luR2PSB4VexSs-M_GfC03_Wsp7AIU1690WhqMFNOCo_HBRjI8GyoFhsnB/s.glbimg.com/vi/mk/program/2507/logotipo_xs/1/45x34.png'),
# 			('/globo-news/arquivo-n', 'Arquivo N', 'http://s2.glbimg.com/AbsjuXVqgMRXxnuIhkpgKeTSimj5wBt75Rs62ixPw-3yTuzn4WIXRxVm_0qxzVXs/s.glbimg.com/vi/mk/program/992/logotipo_xs/3/45x34.png'),
# 			('/globo-news/globo-news-ciencia-e-tecnologia', 'Globo News Ci\xc3\xaancia e Tecnologia', 'http://s2.glbimg.com/Hvo2Ul0fdqlfAwtKyBi8sYEJ0IHfox9JZ3VKmVpQOsppEGVa32ThnDFz_xMT10HQ/s.glbimg.com/vi/mk/program/4231/logotipo_xs/1/45x34.png'),
# 			('/globo-news/cidades-e-solucoes', 'Cidades e Solu\xc3\xa7\xc3\xb5es', 'http://s2.glbimg.com/aHAc0JtBqxkvQdrgjXoUz_A1rBpkWh_gNNO323Fyv6Ev6vFZLEOXowcr1kNrtxKu/s.glbimg.com/vi/mk/program/4229/logotipo_xs/1/45x34.png'),
# 			('/globo-news/globo-news-especial', 'Globo News Especial', 'http://s2.glbimg.com/f-Tnf-_UIzrdQaF138IzLCRu9wLOatVIVOvi-HEYG6bNUN6ZZEfLt_7PncSpAgYv/s.glbimg.com/vi/mk/program/2670/logotipo_xs/4/45x34.png'),
# 			('/globo-news/milenio', 'Mil\xc3\xaanio', 'http://s2.glbimg.com/20KBfF_k7ckY_trv0_qF_rWJFLgE25zbFtHhgpDS2X51A2ZL5Bcu-ik06BEOmbhb/s.glbimg.com/vi/mk/program/2509/logotipo_xs/1/45x34.png'),
# 			('/globo-news/via-brasil', 'Via Brasil', 'http://s2.glbimg.com/QY603D7eeu1yLgcp035TWsTzcZj_-2ea7vMiiXJA_Geggmp413_0S9YXxWPRjMsM/s.glbimg.com/vi/mk/program/988/logotipo_xs/1/45x34.png'),
# 			('/globo-news/globo-news-saude', 'Globo News Sa\xc3\xbade', 'http://s2.glbimg.com/t03gUibmWXlIoJycJEtP7aaWykw-VteZwg0eplLaQimy1MoyULDrhQPbiH_OkL5z/s.glbimg.com/vi/mk/program/5143/logotipo_xs/1/45x34.png'),
# 			('/globo-news/globo-news-literatura', 'Globo News Literatura', 'http://s2.glbimg.com/257_K3eNXnvD8WZp12QcwP0dv5wMGB0FwFpLvLnBr9ATHZEkJFS6NpPdCgK02N5m/s.glbimg.com/vi/mk/program/4234/logotipo_xs/1/45x34.png'),
# 			('/globo-news/sem-fronteiras', 'Sem Fronteiras', 'http://s2.glbimg.com/ghJVqckG6Oqoa_x-EYLhzNtouJJAJuyIanFp2SFhTOFHTK1vWXQk48UYBMO2tNs5/s.glbimg.com/vi/mk/program/2510/logotipo_xs/1/45x34.png'),
# 			('/globo-news/sarau', 'Sarau', 'http://s2.glbimg.com/TvRbWvyxgBiOLfBUOs_rPietlDTsBeTfsSFuL1WYlEkLz-r28BSKxcdizH--fHFU/s.glbimg.com/vi/mk/program/4236/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/antena-paulista', 'Antena Paulista', 'http://s2.glbimg.com/W2Ut-8aRC3E1j69_dMGnjRqYOlLyhUAqktjLdhWwIbfBbZs7XISfKXkNYFBUC6Es/s.glbimg.com/vi/mk/program/3700/logotipo_xs/1/45x34.png'),
# 			('/globo-news/globo-news-economia', 'Globo News Miriam Leit\xc3\xa3o', 'http://s2.glbimg.com/4gvDaIPOa-uutImBFGDtYtyTFVJdgc6kV1lbkOUeOaq7eanh95aEd4bs4yKZ-tK0/s.glbimg.com/vi/mk/program/4232/logotipo_xs/4/45x34.png'),
# 			('/globo-news/pelo-mundo', 'Pelo Mundo', 'http://s2.glbimg.com/x4R_duSBwi9hTjujacoX0vtqrVqWnjCTqsULeTXA8BqPMQvUt73m3nePib1HkY2s/s.glbimg.com/vi/mk/program/989/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/globo-mar', 'Globo Mar', 'http://s2.glbimg.com/iMd7Xau9XP9z9Cs4xTwN9-zCVkwqfiwZ9JtrWN04YGweH8f5dWWKEJ42ab7olpp9/s.glbimg.com/vi/mk/program/4844/logotipo_xs/1/45x34.png'),
# 			('/globo-news/entre-aspas', 'Entre Aspas', 'http://s2.glbimg.com/0hE_b1iCQ5auIL9btWgeZGtX6ax2SqlwEEwEx9xFEJ4okip-UEbKSvb-BC6X19I_/s.glbimg.com/vi/mk/program/4230/logotipo_xs/2/45x34.png'),
# 			('/globo-news/globo-news-dossie', 'Globo News Dossi\xc3\xaa', 'http://s2.glbimg.com/Ua-8fmvGJItNKFhITIh4zFpKApqmpYwzJmd_4es-Nd8BZYbh7ScoBpFdJLbT8ctd/s.glbimg.com/vi/mk/program/4805/logotipo_xs/2/45x34.png'),
# 			('/globo-news/starte', 'Starte', 'http://s2.glbimg.com/V0hnMHgYv9FZHVHShMl3_v_C52uz6RM7JwF_tAegg8B8VeLPOgUU3a27MW_0vrHl/s.glbimg.com/vi/mk/program/2511/logotipo_xs/1/45x34.png'),
# 			('/globo-news/fatos-e-versoes', 'Fatos e Vers\xc3\xb5es', 'http://s2.glbimg.com/X0fVEBs699ic8BPC0CXuaRyrvBOmxbMQ3-tXXNIsuj6MQLk9Z7-lsyF1syaq3AXN/s.glbimg.com/vi/mk/program/3404/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/globo-horizonte', 'Globo Horizonte', 'http://s2.glbimg.com/tSMeW0NAhHTcwOT_cSGvs3uN6CfNDd9pqwlenUYVcaydQzDDAz1mul0GlyYQGKA4/s.glbimg.com/vi/mk/program/4211/logotipo_xs/1/45x34.png'),
# 			('/globo-news/globo-news-politica', 'Globo News Alexandre Garcia', 'http://s2.glbimg.com/QmLsc82T86TqEv5AjGsDuogfAXvoakS5eGNn4VyA0mltC3IcnFtypbtxJtN3CMnG/s.glbimg.com/vi/mk/program/4235/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/globo-mar-2010', 'Globo Mar 2010', 'http://s2.glbimg.com/e3aFfOJiBS1YzAvnSVFuwrsFVZt0IaM4h-_8pf7AJjvQUP76lTZc4PrH8BY_DZf4/s.glbimg.com/vi/mk/program/7122/logotipo_xs/1/45x34.png'),
# 			('/globo-news/acervo', 'Acervo', 'http://s2.glbimg.com/b3aJPor7RGMdPuypeG3wPhtF_CoUbcL-RvOmA3g79VIrp07LL3EI8UCY-h9rWlES/s.glbimg.com/vi/mk/program/7107/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/sangue-latino', 'Sangue Latino', 'http://s2.glbimg.com/jV41JjiezXvh3kwOjtjGgCzgysD1wDXnZy9ncHnwDnEaJadbO23pSviILmB3RsUV/s.glbimg.com/vi/mk/program/4865/logotipo_xs/1/45x34.png')],
# 		'title': 'Jornalismo' },
# 	'moda-e-beleza': {
# 		'shows': [
# 			('/gnt/vamos-combinar', 'Vamos Combinar Seu Estilo', 'http://s2.glbimg.com/q05ICyV1tJiJDqEVLHIv0Z0FSdfOIUIWQMnRC2c5E0knqqIN88KGWuaCSh4BBwdz/s.glbimg.com/vi/mk/program/5172/logotipo_xs/4/45x34.png'),
# 			('/gnt/base-aliada', 'Base Aliada', 'http://s2.glbimg.com/DNf3xCwBG_8Gf1fcKMEcsLRwtzgFSkSNq_G_VXYMYZi7OI4znT3Xh3R9miQ8DVcC/s.glbimg.com/vi/mk/program/5165/logotipo_xs/1/45x34.png'),
# 			('/gnt/superbonita', 'Superbonita', 'http://s2.glbimg.com/tyASn6HtT4D2sAER5akJl4CUlP1UqKiIZJIygpaL14VcAsvjqqO5jPImvWBFHgYu/s.glbimg.com/vi/mk/program/2812/logotipo_xs/1/45x34.png'),
# 			('/gnt/desafio-da-beleza', 'Desafio da Beleza', 'http://s2.glbimg.com/Z2VcvPdU4XGbV-cXDVZQk-N8RLue_q4fDCfBgF24YNtXQbWTYYWEdGQLAW1stHKG/s.glbimg.com/vi/mk/program/7026/logotipo_xs/1/45x34.png'),
# 			('/gnt/gnt-fashion', 'GNT Fashion', 'http://s2.glbimg.com/QA4WtE0KAJxkJ1ER_3xJu81qiS7zAlpdmdCRtjCDV69Nw0pZ-DYwEZ5fcS9s7DNK/s.glbimg.com/vi/mk/program/2813/logotipo_xs/2/45x34.png'),
# 			('/gnt/beleza-gnt', 'Beleza GNT', 'http://s2.glbimg.com/uCiD1ajV9BanjpGZJ5IQEdFEAfipbK7IzudTeBpfm3WHn6WfZbBaj-oflXLJ-TS1/s.glbimg.com/vi/mk/program/5404/logotipo_xs/1/45x34.png'),
# 			('/gnt/moda-gnt', 'Moda GNT', 'http://s2.glbimg.com/9XqKXSPkMucLbA5jQqdzSua1nPGu1G7bjTBmiYi0N72TEw8EIHsA0FeBDb9Ba4oO/s.glbimg.com/vi/mk/program/4720/logotipo_xs/1/45x34.png'),
# 			('/gnt/fashion-rio', 'Fashion Rio', 'http://s2.glbimg.com/BJVO1WP_FtUdMeiyRVaDMSEt2efBirjtRN6qqp1MigSCdrq2UDRrZ0gRrDqqFGg2/s.glbimg.com/vi/mk/program/4603/logotipo_xs/2/45x34.png'),
# 			('/gnt/fashion-television', 'Fashion Television', 'http://s2.glbimg.com/JNZ59U8udKdueJNbv7hI50bDU45EDOYDqKxrLMr169MkJyVV8WT9yHUgDBnaUZNq/s.glbimg.com/vi/mk/program/4801/logotipo_xs/1/45x34.png')],
# 		'title': 'Moda e Beleza' },
# 	'musica': {
# 		'shows': [
# 			('/canal-brasil/zoombido', 'Zoombido', 'http://s2.glbimg.com/JZRC19LEjj4QyhsK2Jg72MOw5dtZYhQT1mwj2-4FHSEFehVUfohl20IKDaXXm7pv/s.glbimg.com/vi/mk/program/4637/logotipo_xs/1/45x34.png'),
# 			('/multishow/tvz', 'TVZ', 'http://s2.glbimg.com/Uubsr89r18Lg0mvCmuZz6hy2EyXW4TfMldP74tdWuUt53CA0YtoNjlzQ8vAVRduA/s.glbimg.com/vi/mk/program/2671/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/faixa-musical', 'Faixa Musical', 'http://s2.glbimg.com/VUz05-s1IunQwtL_RhZstqph0YhD_z4hrDN_g-Zn_DpRPiaVheRkHFPL2ztO5-wc/s.glbimg.com/vi/mk/program/4762/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/som-do-vinil', 'Som do Vinil', 'http://s2.glbimg.com/tbEMs68FkNmur1LfOKwCFsCLm_9O3fzhMzduadbA8dsTh44_KZm2LFyxQIYE0Z6h/s.glbimg.com/vi/mk/program/4639/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/estudio-66', 'Est\xc3\xbadio 66', 'http://s2.glbimg.com/fLh9btvAeVfnp5lWTbXUMRiy96XLWxeGusI8qEcbIj77JqkF_HLlJK8JmgasM2Qo/s.glbimg.com/vi/mk/program/4643/logotipo_xs/1/45x34.png'),
# 			('/multishow/experimente', 'Experimente', 'http://s2.glbimg.com/b1LIgkHIjZKWpQ6xAG4M2Lx2nCVO-2Ju6HcBX0GbNbjrOFgcKwKJJ1K2iw409z-J/s.glbimg.com/vi/mk/program/4726/logotipo_xs/1/45x34.png'),
# 			('/multishow/um-chope-com', 'Um Chope Com', 'http://s2.glbimg.com/LdykLkMbjt7WE6Of-LWPUyvNbOR304glWeZevn1tvktWVodgypVE389s7pOWlRAs/s.glbimg.com/vi/mk/program/4791/logotipo_xs/1/45x34.png'),
# 			('/multishow/geleia-do-rock-2011', 'Geleia do Rock 2011', 'http://s2.glbimg.com/B5KQ_mcKsAUeCd4gOvbhUDGzN2R4AcYWspxXaoTUqB_rLBSGSRbsqegwfAfHrZIY/s.glbimg.com/vi/mk/program/5268/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/mpbambas', 'MPBambas', 'http://s2.glbimg.com/HwIqCR2zgKXVZdfZfncy_X1skExfSrJKXyrtb6_5uGlhR4HPZ2AzF3nx7-ztMU0e/s.glbimg.com/vi/mk/program/4741/logotipo_xs/1/45x34.png'),
# 			('/multishow/rock-estrada', 'Rock Estrada', 'http://s2.glbimg.com/thQH5CUtA83W-g_ijTsfOxGbtTpV1L8uQnwYTQaqI0vE2YQVjnEX2J6Uo5Ftxaez/s.glbimg.com/vi/mk/program/4812/logotipo_xs/1/45x34.png'),
# 			('/multishow/em-busca-da-balada-perfeita', 'Em busca da balada perfeita', 'http://s2.glbimg.com/jBNpOKs3Bpe-pw80GDIDTkdjszVCJYU1c4rpA016YHQirmbknV2QbcCiZnz-iaku/s.glbimg.com/vi/mk/program/4775/logotipo_xs/1/45x34.png')],
# 		'title': 'M\xc3\xbasica' },
# 	'novelas': {
# 		'shows': [
# 			('/rede-globo/salve-jorge', 'Salve Jorge', 'http://s2.glbimg.com/l9Ak4jSp56hx-9bktGIaoK_bTYSziGHUT672wAHx4BC-14BZ8FhmTGJVHs315gfz/s.glbimg.com/vi/mk/program/7124/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/lado-a-lado', 'Lado a Lado', 'http://s2.glbimg.com/MBZYgF7t_hZ2SqzHa8Y-Yqqu5PTF0vgSYkFX0MhPGiu-Bd5-t7twTxYdPpbKp1pW/s.glbimg.com/vi/mk/program/7044/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/malhacao-2012', 'Malha\xc3\xa7\xc3\xa3o 2012', 'http://s2.glbimg.com/tMzAZiTIOVoTXt0RdXZYA-f8mm12WeIUtu8prWTUgsand-8McTu-yAJtBdl8VUAK/s.glbimg.com/vi/mk/program/6969/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/guerra-dos-sexos', 'Guerra dos Sexos', 'http://s2.glbimg.com/aXhixgJ017p9bMmFxJGdrOKLhuVVwwPO8EcqWvXjRDpeDDtYpBNRbuh9TKSUCuxh/s.glbimg.com/vi/mk/program/2641/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/avenida-brasil', 'Avenida Brasil', 'http://s2.glbimg.com/1sz8D7PWOGcroic8HQlUHbZlSgzpJRaSuVFVJ8PL_JqFW0P4DQ4e8hn3wn9nuwnT/s.glbimg.com/vi/mk/program/5727/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/gabriela', 'Gabriela', 'http://s2.glbimg.com/7UcYwZPY-AFxKk0-TsPWqHbOy98-R1sNd4tq9anHp_9VgRJ_OoxTPGA8El4CIDaw/s.glbimg.com/vi/mk/program/2697/logotipo_xs/5/45x34.png'),
# 			('/rede-globo/da-cor-do-pecado', 'Da Cor do Pecado', 'http://s2.glbimg.com/YfXGdqpaeCVgQbGQ5UasdVhfuoJhv7tpBSf7j4FeKipL7ffOg15lSAY-snXwouv9/s.glbimg.com/vi/mk/program/3325/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/cheias-de-charme', 'Cheias de Charme', 'http://s2.glbimg.com/ZZjDqC-qJtjsXK1xQ1_UbajcY1TaQYIZINgfdzNTQTeo9lX5bdKL2DpNDe8wmTT1/s.glbimg.com/vi/mk/program/5764/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/fina-estampa', 'Fina Estampa', 'http://s2.glbimg.com/eH91hNQ1vuOacW7PQVzTw0MMwC3qIIUmKgMKXgYRgZ7jtXAOCuXgDkrbW4bgXzAB/s.glbimg.com/vi/mk/program/5371/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/amor-eterno-amor', 'Amor Eterno Amor', 'http://s2.glbimg.com/OIT5cle1ITQj7Lf_cx9z-xXbf-Jmsker2U2LXfpzIbiFk6G97-_gWpjnZnlq4y8Y/s.glbimg.com/vi/mk/program/5682/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/a-vida-da-gente', 'A Vida da Gente', 'http://s2.glbimg.com/bfZo86rwO1aqgwEFSXzl3-mgDrVPvy2-aeQYhWGTRiF60CJpBkIybBBlBRI_65qn/s.glbimg.com/vi/mk/program/5426/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/insensato-coracao', 'Insensato Cora\xc3\xa7\xc3\xa3o', 'http://s2.glbimg.com/T0o6U3MRf8Ia9StAp_USQQJsh2xg2DUSkzbU6rTORBAaNwJAGjSf3w-CYyN80bsz/s.glbimg.com/vi/mk/program/5090/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/malhacao-2011', 'Malha\xc3\xa7\xc3\xa3o 2011', 'http://s2.glbimg.com/KLW8LBbS5G5jbWbRqeCsPeZCNijbs6gpa-D8beQz_ch4LOO9n1u2uFzT57e_qVrU/s.glbimg.com/vi/mk/program/5409/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/malhacao-2010', 'Malha\xc3\xa7\xc3\xa3o 2010', 'http://s2.glbimg.com/ATI2f58MV1T7yoj378f-OTNacl7hJJLBDTxH0-4s1mpf7pcyC7556IZ1dkLXnB-X/s.glbimg.com/vi/mk/program/2534/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/cordel-encantado', 'Cordel Encantado', 'http://s2.glbimg.com/oRpdhcM_xJ3zcWKhPkL6qK-8cN9ICJMedQYhijiNcDQsXn0O4oAJOxsF2VTQcf9s/s.glbimg.com/vi/mk/program/5173/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/aquele-beijo', 'Aquele Beijo', 'http://s2.glbimg.com/2xbQve9F8awwNSMhCwwf0rkLFYmV55oXsa2Z9cQf7CENX-dyYmifjJbAhSl8ENZc/s.glbimg.com/vi/mk/program/5427/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/o-astro', 'O Astro', 'http://s2.glbimg.com/U4U1NdqrODsAAvQGPSDmwJcwY2Nq0Dd09cUykpIt6hmcxiGF3GHL85ZaR-y81SZu/s.glbimg.com/vi/mk/program/5342/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/chocolate-com-pimenta', 'Chocolate com Pimenta', 'http://s2.glbimg.com/mcUcfCwbSwfCky9_sUmeOW_2DGCeOW-feEUko2I_vnPqpeMhig0o4N0ACGlLSI-l/s.glbimg.com/vi/mk/program/3171/logotipo_xs/6/45x34.png'),
# 			('/rede-globo/morde-e-assopra', 'Morde e Assopra', 'http://s2.glbimg.com/RgTnFn3Aaw7jI-U6UN3ZDgbD9bB8TcdjaMLTYN44R-LYw_w_LNXxPpxegL59x5QO/s.glbimg.com/vi/mk/program/5150/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/mulheres-de-areia', 'Mulheres de Areia', 'http://s2.glbimg.com/1zyOf753zp6zTiCAEa5QgpcFpwgzDz9kYKCsMN5I0XLJBeKoi-lFzgF-9C34eVtS/s.glbimg.com/vi/mk/program/2680/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/ti-ti-ti', 'Ti-ti-ti', 'http://s2.glbimg.com/36UCgge2KrCQMNZVLAuAAHh4vA70IspSODVZKW7dtXODGcOkMHho3FdE18U9u657/s.glbimg.com/vi/mk/program/4947/logotipo_xs/1/45x34.png')],
# 		'title': 'Novelas' },
# 	'receitas': {
# 		'shows': [
# 			('/gnt/cozinha-pratica', 'Cozinha Pr\xc3\xa1tica', 'http://s2.glbimg.com/ouOkYCieGJeKPedJ2l7cJVwcVVG4HtIxwoTQIrZ9OBrB2Vwf022lBosTyoRAyRwJ/s.glbimg.com/vi/mk/program/5800/logotipo_xs/1/45x34.png'),
# 			('/gnt/que-marravilha', 'Que Marravilha!', 'http://s2.glbimg.com/MaRwyQU3vEn6rRkso-E14qwCXWZUV227g7bEJ55IYuXgfkT0QDsKguoDziVCWSIc/s.glbimg.com/vi/mk/program/4811/logotipo_xs/1/45x34.png'),
# 			('/gnt/diario-do-olivier', 'Di\xc3\xa1rio do Olivier', 'http://s2.glbimg.com/o037KokaFi_sFSC_m9OpT7UKqj0K2QCR5q3I4G64-MpRlIYA_y2oWKH296TzsmVa/s.glbimg.com/vi/mk/program/2814/logotipo_xs/1/45x34.png'),
# 			('/gnt/receitas-gnt', 'Receitas GNT', 'http://s2.glbimg.com/3VQs2Nk8YzXABIo4CyyLDZ38qxIgoWp_avumW7bE1tANZZ0oztXxBC6H64Pn_lF9/s.glbimg.com/vi/mk/program/4718/logotipo_xs/1/45x34.png'),
# 			('/gnt/jamie-oliver', 'Jamie Oliver', 'http://s2.glbimg.com/wj3hZ419BvoXcradH96-m6g3DEU2gbjhZ9orVv6LBXYZ9t4KQWl2o1r6oL62cB3J/s.glbimg.com/vi/mk/program/4864/logotipo_xs/1/45x34.png'),
# 			('/gnt/receitas-de-chuck', 'Receitas de Chuck', 'http://s2.glbimg.com/HpYaOLeB6wCSaiutxNQJIjqiimIkdHMKyO7BRWIOcHCoQ4JWCl56D8p1U3NzMb__/s.glbimg.com/vi/mk/program/4997/logotipo_xs/1/45x34.png'),
# 			('/gnt/4-ingredientes', '4 Ingredientes', 'http://s2.glbimg.com/43e5lLie5f-mUPutanyBBdxQ88yN3AWi7k_Vt1lVVflhM6lplSel1jucE08dtp1W/s.glbimg.com/vi/mk/program/5315/logotipo_xs/1/45x34.png'),
# 			('/gnt/nigella', 'Nigella', 'http://s2.glbimg.com/zqFvsY8o_-HoKGg3l-Y5sp6cZ-mJIkdYn5sbDwFy-yc5kmZnc-W0tuK6LTfu0DB5/s.glbimg.com/vi/mk/program/5082/logotipo_xs/1/45x34.png'),
# 			('/gnt/a-cozinha-caseira-de-annabel', 'A Cozinha Caseira de Annabel', 'http://s2.glbimg.com/KzjxIbydvk-7LIiDIsi4pqQKuUT3T_AhN8u6CuyabibaABXtNjwy_W7f1LV-rl7Q/s.glbimg.com/vi/mk/program/5166/logotipo_xs/1/45x34.png'),
# 			('/gnt/cozinha-mediterranea', 'Cozinha Mediterr\xc3\xa2nea', 'http://s2.glbimg.com/nktG7EJxdoKDUArgqIHPfOCXvT0cCQCz-FRT15X5gu2gFgAWpAx2InjeTyiaYwy6/s.glbimg.com/vi/mk/program/5018/logotipo_xs/1/45x34.png')],
# 		'title': 'Receitas' },
# 	'saude': {
# 		'shows': [
# 			('/gnt/alternativa-saude', 'Alternativa: Sa\xc3\xbade', 'http://s2.glbimg.com/CqsEi7ghf6Fs1N906hn-raCrVXINhL9b882m9pmc9Foh8fQ_Q9U5ByWdvdGtyrbr/s.glbimg.com/vi/mk/program/2811/logotipo_xs/3/45x34.png'),
# 			('/gnt/boas-vindas', 'Boas Vindas', 'http://s2.glbimg.com/HX9ugtHVrxowHALnv8nyKQj3p3b-Wk7_3_8n2uILlayMFdphxeeoK7eWcF7N9pXJ/s.glbimg.com/vi/mk/program/5733/logotipo_xs/1/45x34.png'),
# 			('/gnt/ate-quando-voce-quer-viver', 'At\xc3\xa9 quando voc\xc3\xaa quer viver?', 'http://s2.glbimg.com/IUIWMSgoSOnhD_dt3mLhaSObZpYNge6RgFA-s7_YIH0HSbJh8gh2hjjMb4ByfanP/s.glbimg.com/vi/mk/program/7183/logotipo_xs/1/45x34.png'),
# 			('/gnt/medida-certa-o-fenomeno', 'Medida Certa - O Fen\xc3\xb4meno', 'http://s2.glbimg.com/BHPeaDbOcWx5WNEZdNnCY0HiEPLdDV5ZjHcXbJ5LJAlb1Zb71q0P6oAONb5rS-2N/s.glbimg.com/vi/mk/program/7181/logotipo_xs/1/45x34.png'),
# 			('/gnt/maes-gnt', 'M\xc3\xa3es GNT', 'http://s2.glbimg.com/oT-1Dc6EmcFq02JjwNciOiWjPgOgSMTAKMpUM75ijOGdyilK4dzsNRVerx5rdN87/s.glbimg.com/vi/mk/program/5403/logotipo_xs/1/45x34.png'),
# 			('/gnt/quebra-cabeca', 'Quebra-Cabe\xc3\xa7a - Vida de Crian\xc3\xa7a', 'http://s2.glbimg.com/dkB0dmQzFM67QSzGGrA9vXCUY8I8GTDtI9o3jUis_GMbZn_OlSnqeTPI-SFmdxU9/s.glbimg.com/vi/mk/program/5270/logotipo_xs/2/45x34.png'),
# 			('/gnt/mae-e-mae', 'M\xc3\xa3e \xc3\xa9 M\xc3\xa3e', 'http://s2.glbimg.com/k_2tfx9wYiL4Fs3YRfrGyUL9eRBvP2iEZZyNEk-RXD4UQs7UezEJyp-xnsYMbTdO/s.glbimg.com/vi/mk/program/5780/logotipo_xs/2/45x34.png'),
# 			('/gnt/perdas-e-ganhos', 'Perdas &amp; Ganhos', 'http://s2.glbimg.com/95k5D3PuRzqLI6M8KLW1s8MZggjB14IiSpKAS-EE5GsWonXWxSDqwGo_5OdLjjxw/s.glbimg.com/vi/mk/program/5167/logotipo_xs/1/45x34.png'),
# 			('/gnt/novas-familias', 'Novas Fam\xc3\xadlias', 'http://s2.glbimg.com/FBLjU3hccgPr8C9kkcjvf4u4SlAoi5XO2QSU2HzYApZEAqpotepmtluj4LzZbvwU/s.glbimg.com/vi/mk/program/5732/logotipo_xs/1/45x34.png')],
# 		'title': 'Sa\xc3\xbade'},
# 	'sensual': {
# 		'shows': [
# 			('/multishow/malicia', 'Mal\xc3\xadcia', 'http://s2.glbimg.com/OnBYh2F3KJlxaOpDYXJxl_GLgqcNtZReHbHzUTHBEIj_GZ4GARJxiEJ6dPTAv0ju/s.glbimg.com/vi/mk/program/5358/logotipo_xs/1/45x34.png'),
# 			('/multishow/casa-bonita-4', 'Casa Bonita 4', 'http://s2.glbimg.com/vqkmHiu_EEoZRVlRjhL-fHelgupqffEJg4dcpQNAOut9VpDGFijjcwWed6ZBdYOU/s.glbimg.com/vi/mk/program/5836/logotipo_xs/1/45x34.png'),
# 			('/multishow/papo-calcinha', 'Papo Calcinha', 'http://s2.glbimg.com/DHbEmPyNpCCWVrXDiSzm8W4sICmo3Pt19kgMDLcqolAkR6BeApNyya9SZrOYvaG3/s.glbimg.com/vi/mk/program/4795/logotipo_xs/1/45x34.png'),
# 			('/multishow/casa-bonita-3', 'Casa Bonita 3', 'http://s2.glbimg.com/nxQzhSBuQWRouGrx4ZsQH-w2tyUFAao7Wop7Tf6xMXdNxbECfFVAjQubE3jVnrfQ/s.glbimg.com/vi/mk/program/5287/logotipo_xs/1/45x34.png')],
# 		'title': 'Sensual'},
# 	'series': {
# 		'shows': [
# 			('/rede-globo/suburbia', 'Suburbia', 'http://s2.glbimg.com/4naHVV07r6ME8yfWEj-ff6hNc3iRJTNbtwKob5r_vexBERUcFuourv8-vfyJx18R/s.glbimg.com/vi/mk/program/7188/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/como-aproveitar-o-fim-do-mundo', 'Como aproveitar o fim do mundo', 'http://s2.glbimg.com/5ZfrNOEx0cdo75BK0GXz3MzZAPozBanfZ_adFr_qZ532EOCKtCMhcfRVZqy-DuMS/s.glbimg.com/vi/mk/program/7179/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/a-grande-familia', 'A Grande Fam\xc3\xadlia', 'http://s2.glbimg.com/r08e7DXU_JkTDcwXOfb_BIgnnVPmlhUZIeeeU_D3VPaio_mWKR4BO0EOm3oWD-5h/s.glbimg.com/vi/mk/program/2512/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/tapas-e-beijos', 'Tapas e Beijos', 'http://s2.glbimg.com/nR1vyooFU7dnWIR1Hy447OfiMYgRFK0xHbrDRD8NdaT1wQ6_ijcQT_ZiWeQAKzcT/s.glbimg.com/vi/mk/program/5221/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/louco-por-elas', 'Louco por Elas', 'http://s2.glbimg.com/fWr3YZeQDoQystJOZ8Jb-W38DukHnHHJSwXNKeX2x3Rx_7b_U6scm-jaBrhF_4MB/s.glbimg.com/vi/mk/program/5728/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/os-caras-de-pau', 'Os Caras de Pau', 'http://s2.glbimg.com/_AQBIyOuB3A8L3_7673FmMiAVDatzT8F53g6nhFuU9LeWW6whw9xP8aZPB2H8iQs/s.glbimg.com/vi/mk/program/4262/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/as-brasileiras', 'As Brasileiras', 'http://s2.glbimg.com/p3p57RyRdzPRVG-dSMuBzAe7d30q6sSfDaT8nJF3tgovn1opksIi2oSoeNc46MML/s.glbimg.com/vi/mk/program/5676/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/os-normais', 'Os Normais', 'http://s2.glbimg.com/dKT7yLdTUfhAG7mLQi-5hMeGq0xBg8TMLF7DHhG8Fo6VAjbpT8N8lkrS09I60sB-/s.glbimg.com/vi/mk/program/2536/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/a-mulher-invisivel', 'A Mulher Invis\xc3\xadvel', 'http://s2.glbimg.com/ONbN5Zi-Rc4au9-EQcarTQT1qFqOrIAqgdgeJJLotH_ZbExffzPJ96mKHSuPucoq/s.glbimg.com/vi/mk/program/5303/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/a-cura', 'A Cura', 'http://s2.glbimg.com/jltUOwM_ZHjjhm7NjWcx1XdmayaxnGoniBmWZeg1a_CToWuz-mxxMJbEeQIbF7q-/s.glbimg.com/vi/mk/program/4978/logotipo_xs/1/45x34.png'),
# 			('/universal-channel/house', 'House', 'http://s2.glbimg.com/Eybktj_nvsZ097QxT_Fwr5EqoxGuaFyY4NmIlFOKFK9tKaU6e0n0Z7FzYasYTpMq/s.glbimg.com/vi/mk/program/3791/logotipo_xs/1/45x34.png'),
# 			('/universal-channel/law-and-order-svu', 'Law and Order - SVU', 'http://s2.glbimg.com/_n_qCs07HfeHm4mMWBCFb1D_zRIrwA7Ho2Xq360bHO_q2KoVz6P4Xo7vYC0T8fT3/s.glbimg.com/vi/mk/program/3584/logotipo_xs/1/45x34.png'),
# 			('/universal-channel/grimm', 'Grimm', 'http://s2.glbimg.com/S9A5yecBJUIm-VVaqrPN29KdK0PQB0H1V0kh-aYYNc6GwvH2-z3r-yVe9rlDO9GD/s.glbimg.com/vi/mk/program/5473/logotipo_xs/1/45x34.png'),
# 			('/multishow/oscar-freire-279', 'Oscar Freire 279', 'http://s2.glbimg.com/IEOgsxxU084mprOCFc1EVfoq7MOsDqNLIW_s2e8JxrzasQ4zN5HdK1KgrFCTCUvH/s.glbimg.com/vi/mk/program/5422/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/dercy-de-verdade', 'Dercy de verdade', 'http://s2.glbimg.com/Za4roN8PRz81I8OOfhnnSvEvzvrSEMt-oC2g0cYrF4XoybGI-FQsovmjAwkRhh3v/s.glbimg.com/vi/mk/program/5633/logotipo_xs/2/45x34.png'),
# 			('/universal-channel/whats-on', 'What\xc2\xb4s On', 'http://s2.glbimg.com/xjqsTl7XTLLsmI0H2y4IHvja_XkSlSR8cD5ZA7TF5Tt_ly1RpRDC9vyyw_u7bxoc/s.glbimg.com/vi/mk/program/3587/logotipo_xs/2/45x34.png'),
# 			('/universal-channel/smash', 'Smash', 'http://s2.glbimg.com/pr14fBgLFS0daLV9c-vdqDjUMqFQPj7wuaziDNerx4AId98_eGFpvWHCmZmRF4Z8/s.glbimg.com/vi/mk/program/5651/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/o-brado-retumbante', 'O Brado Retumbante', 'http://s2.glbimg.com/AQn1T5lYgL_YWyG0gnKC3VsVAwuS180IzBgg-AlHIrQZEKvDQ81MenDa-U2q7Frv/s.glbimg.com/vi/mk/program/5634/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/macho-man', 'Macho Man', 'http://s2.glbimg.com/Lk8I63gPcRA50rdEpJQWLmuzUwK9MZZrPJLWma-obJVhHQjmiwnrb7btM23Wuvyz/s.glbimg.com/vi/mk/program/5220/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/vampiro-carioca', 'Vampiro Carioca', 'http://s2.glbimg.com/mCbk0OPGtCcKQJNxYiAw8Da5oVCUfD9Uglb-KvJTJ1PQibrmgKMO1YnEtoCfvrTe/s.glbimg.com/vi/mk/program/4977/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/projeto-sumir', 'Projeto Sumir', 'http://s2.glbimg.com/OIIXsWbf0VHw4VnpC1w3GP-HlOj7DqxJnsr5K9ZbhhVnIFm3Z1_HEv3V8IAC76TJ/s.glbimg.com/vi/mk/program/5209/logotipo_xs/1/45x34.png'),
# 			('/universal-channel/a-gifted-man', 'A Gifted Man', 'http://s2.glbimg.com/XVm6TqbbO5sI469I87Nce6u0KbsZP6-T4P-h8kaEt6WYZkIAbdZzt9FtECjgrozX/s.glbimg.com/vi/mk/program/5472/logotipo_xs/1/45x34.png'),
# 			('/universal-channel/the-good-wife', 'The Good Wife', 'http://s2.glbimg.com/LE83zbzCN9hMDscIr3idoL5Xz0dw8PssTeWgqABVH-ciAjN5Lj1aNCdYehgPGIKu/s.glbimg.com/vi/mk/program/4782/logotipo_xs/1/45x34.png'),
# 			('/universal-channel/rookie-blue', 'Rookie Blue', 'http://s2.glbimg.com/Bzt5Djc1qdE5ZCugprtVuINAgy-fIUO6rmz120fGfSFYpr01gwoHeN_iRz1U_kZj/s.glbimg.com/vi/mk/program/4980/logotipo_xs/2/45x34.png')],
# 		'title': 'S\xc3\xa9ries'},
# 	'variedades': {
# 		'shows': [
# 			('/rede-globo/the-voice-brasil', 'The Voice Brasil', 'http://s2.glbimg.com/7zc1D8ol6-ATiWom5tYuR5y43EgfigDNeIUTNSXcvq1MDFkNA0Z1W7lbCYw4XDNS/s.glbimg.com/vi/mk/program/5821/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/mais-voce', 'Mais Voc\xc3\xaa', 'http://s2.glbimg.com/xr-d_WC-TWfSOGyIzLGnY5mXYohGYJaJI9OxDVOsISONstNmVgLgJMpY7uwFl3t5/s.glbimg.com/vi/mk/program/2533/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/domingao-do-faustao', 'Doming\xc3\xa3o do Faust\xc3\xa3o', 'http://s2.glbimg.com/KAiX0K-QO8L_LVW3AO5LjfHOLE6W57tI-wD1oyRUXb7fHFuDkTvHjxp-Qez7Fzk8/s.glbimg.com/vi/mk/program/2523/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/video-show', 'V\xc3\xaddeo Show', 'http://s2.glbimg.com/VNuBG6aAceMxDEQGDFimIK_i_jS3peC02ousf0WjKPMWJmaWugtzqRd0X46Xu7ZJ/s.glbimg.com/vi/mk/program/990/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/encontro-com-fatima-bernardes', 'Encontro com F\xc3\xa1tima Bernardes', 'http://s2.glbimg.com/5m-1W0MdYdoqGKiKTXelRgROkShDkbcEw6ztDy69i07GiiKKx3WPJ9VWu-eAG38H/s.glbimg.com/vi/mk/program/5885/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/programa-do-jo', 'Programa do J\xc3\xb4', 'http://s2.glbimg.com/ZaC2eLw0kcYL966uo7wCDBuhDW-WykKFzySi1TPJhaI_6kmbwsprnSrM9FGpU_M1/s.glbimg.com/vi/mk/program/2538/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/caldeirao-do-huck', 'Caldeir\xc3\xa3o do Huck', 'http://s2.glbimg.com/mXF8OeoRT7FdH2vjHVXVv1Xgc2skcnneH9Nk7cbDP-9Ux-vEke2nUIGpTtvL7mz0/s.glbimg.com/vi/mk/program/2521/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/tv-xuxa', 'TV Xuxa', 'http://s2.glbimg.com/CR37qAIXjO4W1ijbTler6gWYfPob-zxfGLuVXZmlZQ9ps4PHHln78tj2SaEaZ2H8/s.glbimg.com/vi/mk/program/3779/logotipo_xs/4/45x34.png'),
# 			('/rede-globo/altas-horas', 'Altas Horas', 'http://s2.glbimg.com/p5UWFg1LDTlrvI6wELqPqGY4G-NFEOOXHJ9rfTWMJwVd2S_JSSzaWJxRLECe0xw8/s.glbimg.com/vi/mk/program/2515/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/estrelas', 'Estrelas', 'http://s2.glbimg.com/M68ig03Hahh4b1Yzji463q3934WXaiH4qa4-xqcNYF3jpT2SwWvhLdEeJV5a5FLP/s.glbimg.com/vi/mk/program/4069/logotipo_xs/3/45x34.png'),
# 			('/rede-globo/zorra-total', 'Zorra Total', 'http://s2.glbimg.com/sZLv_QN_Y4cnshUY6wBzam0_D-mJomrGdfEG4U8E3luiaqp_poTtN_gpYExvvEnd/s.glbimg.com/vi/mk/program/2546/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/big-brother-brasil', 'Big Brother Brasil', 'http://s2.glbimg.com/nOYCorUZNdu0Lb_dmWMhOLHvw0rBNQk6Ooy8LeOunYiRXy-cIwSYUC7M0ojdDeAE/s.glbimg.com/vi/mk/program/5562/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/casseta-planeta-vai-fundo', 'Casseta &amp; Planeta Vai Fundo', 'http://s2.glbimg.com/MuVbfdsBNeh5xnTjgP7s-ld7CP3dWAtMH-wNN36HlNvVk4gFSpUzWYekrxI19uSX/s.glbimg.com/vi/mk/program/5751/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/amor-sexo', 'Amor &amp; Sexo', 'http://s2.glbimg.com/1z6sqgqSFSRk-bwRJQ8DJyXVDj5RbisxznQHOFA_vBAYRGD35xZwnsHwIL63F_ui/s.glbimg.com/vi/mk/program/4715/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/as-aventuras-do-didi', 'As Aventuras do Didi', 'http://s2.glbimg.com/QJWBXRv5kPJjAI4UcqoYqdSoeeRRd099F__FSUimhAI8-rylLNEpMUS9ud5IjxDu/s.glbimg.com/vi/mk/program/4854/logotipo_xs/2/45x34.png'),
# 			('/rede-globo/som-brasil', 'Som Brasil', 'http://s2.glbimg.com/6NCGa4iHcg0BXtr2PlG2ov_UQ0vtnP711w1WjcL7lPpkuQ2X7oznSBCdsEwwbK2V/s.glbimg.com/vi/mk/program/3467/logotipo_xs/1/45x34.png'),
# 			('/gnt/marilia-gabriela-entrevista', 'Mar\xc3\xadlia Gabriela Entrevista', 'http://s2.glbimg.com/Cfn_byOYFFMGrix-aMNlODCw7jEi-ZYRfJe0z1JY4RGK9Ogp8RR-uEMKfDenGoO7/s.glbimg.com/vi/mk/program/2815/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/esquenta', 'Esquenta!', 'http://s2.glbimg.com/ALYobhpChHEiE8R-q65b0h91nZuIyly-RtpdjARsi4kcY8tdlA1C4IczO9GjxZhB/s.glbimg.com/vi/mk/program/5088/logotipo_xs/2/45x34.png'),
# 			('/gnt/spfw', 'SPFW', 'http://s2.glbimg.com/SPwXtclvGLZtGgGfAMMYFCY4pBSh5LtNbA_S5_zXZUB9V2oIhIPota824zAF8dvo/s.glbimg.com/vi/mk/program/4602/logotipo_xs/2/45x34.png'),
# 			('/gnt/gntdoc', 'GNT.Doc', 'http://s2.glbimg.com/eT6g8vz3VPW0Q1EcBVPZi-qJzwvFmCMrIsgrNLp_kkxeuoIyIokaHu-NgTlL8_22/s.glbimg.com/vi/mk/program/3606/logotipo_xs/1/45x34.png'),
# 			('/rede-globo/na-moral', 'Na Moral', 'http://s2.glbimg.com/cA_iIdDjW3bTrOEoT3RhHDkTNeJf6pJAMAxBFmSfgbzrr3teB6HW3IkQ7B8rGWCa/s.glbimg.com/vi/mk/program/5950/logotipo_xs/1/45x34.png'),
# 			('/gnt/mulheres-de-aco', 'Mulheres de A\xc3\xa7o', 'http://s2.glbimg.com/88Ttm5pMG3d0YQZdifzHgwAlQYZ_2zHjrZcqdMqNB0jGQBTNWGn_pPeuXRNdssYm/s.glbimg.com/vi/mk/program/7184/logotipo_xs/1/45x34.png'),
# 			('/gnt/the-ellen-degeneres-show', 'The Ellen DeGeneres Show', 'http://s2.glbimg.com/5-swyxGZYyV9F3VbsjbNbxbhCiLDdvF2s-4oyz16V7090L8RDC0YMG0xjooSiZGi/s.glbimg.com/vi/mk/program/5451/logotipo_xs/1/45x34.png'),
# 			('/gnt/confissoes-do-apocalipse', 'Confiss\xc3\xb5es do Apocalipse', 'http://s2.glbimg.com/Rt5YRQVSDs0X-HHg7ZZCvG9CUixQ0vBDjGJAzBS4A4y7JhGbZdaZd50EsfxUCS0j/s.glbimg.com/vi/mk/program/5868/logotipo_xs/1/45x34.png'),
# 			('/gnt/perfumes-da-vida', 'Perfumes da Vida', 'http://s2.glbimg.com/bvMRqmlDNgFEh_2LqG8U7Ac8R4kQwbLzHCTkZKGDswMd1urlnC2dxi0g624FJwV-/s.glbimg.com/vi/mk/program/7182/logotipo_xs/1/45x34.png'),
# 			('/gnt/no-astral', 'No Astral', 'http://s2.glbimg.com/pNl_XlXGXov308pngIAJeT7yxqLPgsCI82C18ntDMoFF8kFtsyoNZ1jsMMYlWQeY/s.glbimg.com/vi/mk/program/5170/logotipo_xs/1/45x34.png'),
# 			('/gnt/por-um-fio', 'Por um Fio', 'http://s2.glbimg.com/z0-LYKqQMWAIP5VquAln0kZIb1ojbQwQ7HiNjtwiHTnVHqD3zJ9wGM0XBVySCxt6/s.glbimg.com/vi/mk/program/5004/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/espelho', 'Espelho', 'http://s2.glbimg.com/VXTKEtLyhtoi4yeBP9SIR211_oC6S_iadhlxbWF6LFr6DI9fA9yi5bqkD0yQEwv7/s.glbimg.com/vi/mk/program/4628/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/e-tudo-verdade', '\xc3\x89 tudo verdade', 'http://s2.glbimg.com/TXjJ0VgX30-APFSS6FqHUdMbwYO3ZbGS5H5tx4Bgt_aTGhS08THRHaoT_DDz7nhk/s.glbimg.com/vi/mk/program/4753/logotipo_xs/2/45x34.png'),
# 			('/canal-brasil/o-estranho-mundo-de-ze-do-caixao', 'O Estranho Mundo de Z\xc3\xa9 do Caix\xc3\xa3o', 'http://s2.glbimg.com/gLLeSLV-N4j4LR_e4D_3PXLvqsxXlE7tWrbPKjHc2srZslsgcheeRxZrJ97ueHXO/s.glbimg.com/vi/mk/program/4633/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/coisas-pelas-quais-vale-a-pena-viver', 'Coisas Pelas Quais Vale A Pena Viver', 'http://s2.glbimg.com/mwNfBjX-fgegDCA45hx2h_HZHQ8h9PIrT504eN_1Z9BoHHZJJekmjTt9B6OnHCDp/s.glbimg.com/vi/mk/program/4832/logotipo_xs/2/45x34.png'),
# 			('/gnt/homens-possiveis', 'Homens Poss\xc3\xadveis', 'http://s2.glbimg.com/6GDseG4h3dFO8ae3w36IrsdvKlRJnuGQ28x_ToiMTrNyG-SmSzqd1A4j0keg0roB/s.glbimg.com/vi/mk/program/5801/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/cone-sul', 'Cone Sul', 'http://s2.glbimg.com/nfA1LqbwR-xiWq0am43ro-KQ1yd01De9A89c7C7roIFRIxAILHoqaVIl5UAOEis4/s.glbimg.com/vi/mk/program/4759/logotipo_xs/1/45x34.png'),
# 			('/gnt/sem-filtro', 'Sem Filtro', 'http://s2.glbimg.com/RtEBJ7w1IH-1XZaNiGEcWLotaxC41GGaJHpccl6H7F27OVsRbOLjuQOhbroOSHhf/s.glbimg.com/vi/mk/program/5639/logotipo_xs/1/45x34.png'),
# 			('/gnt/faixa-de-areia', 'Faixa de Areia', 'http://s2.glbimg.com/NHKdCjxTr2Y2Bz5ScnwW6m_w5WdreLCkwCC6R5AjJtfIpPrabN7k0nTeoczjcLKL/s.glbimg.com/vi/mk/program/5635/logotipo_xs/1/45x34.png'),
# 			('/canal-brasil/album-de-retratos', '\xc3\x81lbum de Retratos', 'http://s2.glbimg.com/f2FkVSjRRjcbQmm3zj3oVnU9rHprbdn4AXLyh89uG7HJRv_F1ZI9gJkbFV-Tqg2m/s.glbimg.com/vi/mk/program/5564/logotipo_xs/1/45x34.png')],
# 		'title': 'Variedades'},
# 	'viagens': {
# 		'shows': [
# 			('/multishow/volta-ao-mundo', 'Volta ao Mundo', 'http://s2.glbimg.com/mKEZxER2v7wtzrU2_F5XdCvbTlx1CLdqOvF2RhpCQS5douDrSy0NT8kkvDAX1MCS/s.glbimg.com/vi/mk/program/5507/logotipo_xs/1/45x34.png'),
# 			('/multishow/nalu-pelo-mundo', 'Nalu pelo mundo', 'http://s2.glbimg.com/CeP5DSKsakczDz4RNt2qYpSYP16UMLoT9UrLmjpfYl4Cl4mv0zMtULsN9H7N1icb/s.glbimg.com/vi/mk/program/4696/logotipo_xs/1/45x34.png'),
# 			('/multishow/vai-pra-onde', 'Vai Pra Onde?', 'http://s2.glbimg.com/yb8OlBV5EkV8vLWseHGCkmSHofr-CxJm4_QtExVbVxTe0j_c-62zlO-4Bk2jJr7R/s.glbimg.com/vi/mk/program/4315/logotipo_xs/1/45x34.png'),
# 			('/multishow/lugar-incomum', 'Lugar Incomum', 'http://s2.glbimg.com/1F3VAsnwpALxV2-x1P4HDQvbBQolqBnb5p50kPlp0KMJKpjmW7DzS4WVh_y_x8Lr/s.glbimg.com/vi/mk/program/4101/logotipo_xs/1/45x34.png'),
# 			('/multishow/sem-destino', 'Sem Destino', 'http://s2.glbimg.com/4unUxFqgMZVJy05bdbxs1Sun7VZ3oU8wo69Bt6_8ldA4a5lg9Mh1mMeqyuqahwtE/s.glbimg.com/vi/mk/program/4794/logotipo_xs/1/45x34.png'),
# 			('/multishow/nao-conta-la-em-casa', 'N\xc3\xa3o conta l\xc3\xa1 em casa', 'http://s2.glbimg.com/nXN7ErZKKh3yXh4N-wi8ARu81Irl1qCcty9pnJGjks9B0i_V895HyvYiP82gKaog/s.glbimg.com/vi/mk/program/4773/logotipo_xs/1/45x34.png'),
# 			('/multishow/verao-que-vem', 'Ver\xc3\xa3o Que Vem', 'http://s2.glbimg.com/SqD1nAFxFYfDcDcG4nBVVNTAfCe5Wvf1VUpfpyQufsRFC239Qt_WTM9jibkt5Eym/s.glbimg.com/vi/mk/program/5647/logotipo_xs/1/45x34.png'),
# 			('/multishow/viajandona', 'Viajandona', 'http://s2.glbimg.com/Asq2wZP1H0JEMFw5WfqFM0xPQ-DqEPmsjpXB0k03Cu12_4IF4CiZ7trlz_MAiSaf/s.glbimg.com/vi/mk/program/5794/logotipo_xs/1/45x34.png'),
# 			('/multishow/embarcados', 'Embarcados', 'http://s2.glbimg.com/Npj5xYet7yAaNmmijo9MAE69hTWyubfF7DuN5h8rB0ALmV5lrFw3b3V8hAkuxyww/s.glbimg.com/vi/mk/program/5795/logotipo_xs/1/45x34.png'),
# 			('/multishow/no-caminho', 'No caminho', 'http://s2.glbimg.com/luhym7Gqe-pq_dchdEavzGaEHS2upgx0OvJGWVtXRneYIV1-hbQsnV3PLY9ohUz0/s.glbimg.com/vi/mk/program/4697/logotipo_xs/1/45x34.png'),
# 			('/multishow/viagem-sem-fim', 'Viagem Sem Fim', 'http://s2.glbimg.com/R7UJXVbKWGcu8yhrxvVpcazc_HUI9exe-DEmTaZl7Im5kz8uJbljqoN8ZIWt7dUM/s.glbimg.com/vi/mk/program/4840/logotipo_xs/1/45x34.png'),
# 			('/multishow/dois-elementos', 'Dois Elementos', 'http://s2.glbimg.com/Buo4Eb5Ol5GSyqWeen021FQQgmMWCZUW8HXnWFV__B3APmIX-dIuUVooVBvBXvOW/s.glbimg.com/vi/mk/program/5407/logotipo_xs/1/45x34.png'),
# 			('/multishow/kaiak', 'Kaiak', 'http://s2.glbimg.com/GeqVMny8sVvCzEpmCyetDOFOnxg9SmOO7G4eFUGp1p7GJOQGwYaj8Asly_FuDW2P/s.glbimg.com/vi/mk/program/4908/logotipo_xs/1/45x34.png')],
# 		'title': 'Viagens'}}


print '+ Test for videos "rail"s'

category = shows[match[randrange(len(match))][0]]
show = category['shows'][randrange(len(category['shows']))]
print 'Category:', category['title']
print 'Show:', show[1]
print show_url % show[0]

req = urllib2.Request(show_url % show[0])
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
response = urllib2.urlopen(req)
link=response.read()
response.close()
# match video 'rail's
rails = re.compile('data-trilho-id="(.+?)"[\s\S]+?<h2.*title="(.+?)"').findall(link)
# for r in rails:
# 	print 'Rail:', r[1], 'id:', r[0]
if not rails:
	print 'no rails found'
	sys.exit()
else:
	print rails
print


print '+ Test for videos of a random rail'
rail = rails[randrange(len(rails))]
print 'Rail:', rail[1], 'id:', rail[0]
req = urllib2.Request(rail_url % (show[0], rail[0], '1'))
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
response = urllib2.urlopen(req)
link = response.read()
response.close()
regExp = '<li.*data-video-title="(.+?)"[\s]+data-video-id="(.+?)"[\s]+data-video-data-exibicao="(.+?)">[\s\S]+?' \
		 + '<img.+src="(.+?)"[\s\S]+?' \
		 + '<span class="duracao">(.+?)</span>[\s\S]+?' \
		 + 'div class="balao">[\s]+?<p>[\s]+?([\w].+?)[\s]+?</p>'
videos=re.compile(regExp).findall(link)
for v in videos:
	print v
if not videos:
	print 'no videos found'
	sys.exit()
print

print '+ Test for links of a random video'
vTitle, vId, vDate, vThumb, vDuration, vDescr = videos[randrange(len(videos))]
print '%s - %s [%s] (%s)' % (vId, vTitle, vDate, vDuration)
req = urllib2.Request(info_url % vId)
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
response = urllib2.urlopen(req)
link = response.read()
response.close()
content = json.loads(link[23:-2])['videos'][0]
if 'children' in content:
	print 'Children videos:'
	for c in content['children']:
		print '- ', c['id'], c['resources'][0]['url']
if 'resources' in content:
	vUrl = ''
	for res in content['resources']:
		if 'iphone' in res['url']:
			vUrl = res['url']
			break
	print 'video url:', vUrl


# info_url % video[1]
# for vTitle, vId, vDate, vThumb, vDuration, vDescr in videos:
# 	# get link for the stream
# 	print '%s - %s [%s] (%s)' % (vId, vTitle, vDate, vDuration)
# 	req = urllib2.Request('http://api.globovideos.com/videos/%s/playlist/callback/wmPlayerPlaylistLoaded' % vId)
# 	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
# 	response = urllib2.urlopen(req)
# 	link = response.read()
# 	response.close()
# 	content = json.loads(link[23:-2])['videos'][0]
# 	if 'children' in content:
# 		print 'Children videos:'
# 		for c in content['children']:
# 			print '- ', c['id'], c['resources'][0]['url']
# 		break
# 	if 'resources' in content:
# 		vUrl = ''
# 		for res in content['resources']:
# 			if 'iphone' in res['url']:
# 				vUrl = res['url']
# 				break
# 		print 'video url:', vUrl

# shows = {}
# if not len(match):
# 	print 'no shows found'
# for vTitle, vId, vDate, vThumb, vDuration, vDescr in match:
# 	# get link for the stream
# 	print '%s - %s [%s] (%s)' % (vId, vTitle, vDate, vDuration)
# 	req = urllib2.Request('http://api.globovideos.com/videos/%s/playlist/callback/wmPlayerPlaylistLoaded' % vId)
# 	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
# 	response = urllib2.urlopen(req)
# 	link = response.read()
# 	response.close()
# 	content = json.loads(link[23:-2])['videos'][0]
# 	if 'children' in content:
# 		print 'Children videos:'
# 		for c in content['children']:
# 			print '- ', c['id'], c['resources'][0]['url']
# 		break
# 	if 'resources' in content:
# 		vUrl = ''
# 		for res in content['resources']:
# 			if 'iphone' in res['url']:
# 				vUrl = res['url']
# 				break
# 		print 'video url:', vUrl
print

# check for more videos
# <a rel="nofollow" id="previous-4ee8a553910891381700000e" class="botao-anterior-pq previous botao-cor-personalizada tiptip ui-sliding-prev disabled" href="/multishow/volta-ao-mundo/_/trilhos/4ee8a553910891381700000e/page/previous">
#     <span class="esconder">Anterior</span>
# </a>


# print '+ Testa retorno dos videos e episodios'
# pgr = match[randrange(len(match))]
# print '--', pgr[2]
# url_args = pgr[1].split('/')[:-1]
# url_args.append('videos')
# url = '/'.join(url_args)
# req = urllib2.Request(url)
# req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
# response = urllib2.urlopen(req)
# link=unicode(response.read(), 'ISO-8859-1')
# response.close()
# match=re.compile('<a href="'+url+'/([^ ]+?)"[\s\S.]+?<img class="imageThumb" src="[#](.+?)"[\s\S.]+?<div class="titulo">(.+?)</div>[\s]+?<div class="subtitulo">[\s]+?([^\t\r\n]*)[\s]+?</div>').findall(link)
# for _url, tb, title, desc in match:
# 	try:
# 		video_id = re.search('\d+', _url).group()
# 	except:
# 		print 'no videos found'
# 		break
# 	# get link for the stream
# 	req = urllib2.Request('http://api.globovideos.com/videos/%s/playlist/callback/wmPlayerPlaylistLoaded' % video_id)
# 	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
# 	response = urllib2.urlopen(req)
# 	link = response.read()
# 	response.close()
# 	contents = json.loads(link[23:-2])
# 	video_url = ''
# 	for res in contents['videos'][0]['resources']:
# 		if 'flash' in res['url']:
# 			video_url = res['url']
# 			break
# 	print """- Titulo: %s
#   Descr: %s
#   PageUrl: %s/%s 
#   Thumb: %s
#   Video: %s""" % (title, desc, url, _url, tb, video_url)




# print len(match), 'videos encontrados'
# print
