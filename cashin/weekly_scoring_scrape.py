'''
A script to scrape the cashin webpages, grab the weekly point total for every rostered player,
and write them to a tab-delimited text file

@author: Ted Natoli
@email: ted.e.natoli@gmail.com
'''

__author__ = 'tnatoli'

from BeautifulSoup import BeautifulSoup
import urllib2, re

base_url = 'http://football26.myfantasyleague.com/2012/weekly?L=42632&W='
outfile = 'cashin_weekly_scrape.txt'


if __name__ == '__main__':

    f = open(outfile, 'w')
    f.write('week' + '\t' + 'player' + '\t' +  'pos' + '\t' + 'points' + '\t' + 'salary' + '\n')

    for i in xrange(16):
        week = i + 1
        url = base_url + str(week)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        player_tags = soup.findAll('td', attrs={'class' : 'player'})
        #points_tags = soup.findAll('td', attrs={'class' : 'points'})

        for player_tag in player_tags:
            player_strings = player_tag.text.split()
            player_name = ' '.join(player_strings[:-1])
            pos = player_strings[-1]
            # salary data is link's title attribute
            # second element when splitting on whitespace
            link = player_tag.find('a')
            title_parts = link.get('title').split()
            salary = re.sub(r'\$', '', title_parts[1])
            salary = re.sub(r',', '', salary)
            # points data found in tag's next sibling
            f.write(str(week) + '\t' + player_name + '\t' + pos + '\t' + player_tag.findNextSibling().text + '\t' + salary + '\n')

    f.close()

