#!/usr/bin/python
import urllib2
import htmllib
import re
import time

class URLdescription():
    def unescape(self, s):
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()

    def text_html(self, page):
        inTitle=False
        title=''
        for html in page.readlines():
            match = re.search('\<title.*?\>(.*?)\<\/title\>', html)
            if match:
                title=match.group(1)
                break
            match = re.search('\<title.*?\>', html)
            if match:
                inTitle=True
            match = re.search('\<title.*?\>(.*?)', html)
            if match:
                title=title+match.group(1)
                continue
            match = re.search('(.*?)\<\/title\>', html)
            if match:
                title=title+match.group(1)
                break
            if inTitle:
                title=title+' '+html
        title=title.strip()
        title=self.unescape(title).strip()
        try:
            title=re.sub(r'[^\x00-\x7f]',r'', title)
        except Exception, e:
            print e
        finally:
            pass

        return title

    def fetchtitle(self, url):
        url = url.strip()
        match = re.search('haskell.org|github.com/ghc/|github.com/haskell/', url)
        if not match
            or url.startswith('https://phabricator.haskell.org/harbormaster/build/'
            or url.startswith('https://ghc.haskell.org/trac/ghc/wiki/'):
            return url

        # Don't use github blobs
        match = re.search('github.com/.+/blob/.+', url)
        if match:
            return url;

        try:
            page = urllib2.urlopen(url)
        except urllib2.URLError, e:
            print int(time.time()),'Error reason: ' + str(e.reason)
            print int(time.time()),"I'm sorry dave..."
            return ""
        except urllib2.HTTPError, e:
            print int(time.time()),'Error code: ' + str(e.code)
            print int(time.time()),"I'm sorry dave..."
            return ""

        content_type = page.info()['content-type']
        print "DEBUG: content-type", content_type

        match = re.search('text/html|application/xhtml\+xml', content_type)
        if match:
            return self.text_html(page)

        match = re.search('^image', content_type)
        if match:
            return url

        return url
