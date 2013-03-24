'''
scrape player tables from yahoo

@author: Ted Natoli
@email: ted.e.natoli@gmail.com
'''

from pattern.web import URL, DOM
from pattern.db import Datasheet
import glob, re


urls = glob.glob('/Users/tnatoli/Desktop/pages/*.html')
headers = ['player', 'pos', 'team', 'owner']

f = open('player_table.txt', 'w')
f.write('\t'.join(headers) + '\n')

for u in urls:
    url = URL(u)
    dom = DOM(url.download(cached=False))
    tbody = dom.by_id('statTable0').by_tag('tbody')[0]
    for tr in tbody.by_tag('tr'):
        pname = tr.by_class('ysf-player-name')[0].by_tag('a')[0].content
        team_pos = tr.by_class('ysf-player-team-pos')[0].by_tag('span')[0].content
        team = re.sub('\(', '', team_pos.split(' - ')[0])
        pos = re.sub('\)', '', team_pos.split(' - ')[1])
        owner_links = tr.by_class('owner')[0].by_tag('a')
        if owner_links:
            owner = owner_links[0].content
        else:
            owner = 'FA'
        line = '\t'.join([pname, team, pos, owner])
        print line
        for l in line:
            try:
                l.encode('ascii')
            except:
                print l
                line = re.sub(l, '', line)
        f.write(line + '\n')

f.close()


