#!/usr/bin/env python2
import re
import sys
import urllib2
import urlparse
from sets import Set
from collections import deque
from pprint import pprint
from BeautifulSoup import BeautifulSoup

try:
    seedurl = sys.argv[1]
    maxdepth = int(sys.argv[2])
    searchString = sys.argv[3]
except:


urlset = Set([seedurl])
savedurls = Set()
q = deque([(0, seedurl)])

output = open('output.txt','w')

# f = urllib2.urlopen(seedurl, timeout=10)
# soup = BeautifulSoup(f.read())
# tags = soup('a')
# pprint([x.get('href') for x in tags], indent = 2)


while q:
    current_depth, url = q.popleft()
    print current_depth, url

    try:
        f = urllib2.urlopen(url, timeout=10)
        content = f.read()
        f.close()
        soup = BeautifulSoup(content)
        tags = soup('a')
        if re.search(searchString, content):
            savedurls.add(url)
            output.flush()
        if current_depth >= maxdepth:
            continue
        for tag in tags:
            newurl = tag.get('href')
            if newurl is not None:
                newurl = urlparse.urljoin(url, newurl)
                if not newurl in urlset:
                    urlset.add(newurl)
                    q.append((current_depth+1, newurl))
    except:
        print >> sys.stderr, "ERROR, could not acess %s" % url
        print >> sys.stderr, sys.exc_info()

output.close()