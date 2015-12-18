
import urllib2

def geturl(url, defaultRes=None, silent=False):
    try:
        response = urllib2.urlopen(url)
        response_read = response.read()
        return response_read
    except urllib2.URLError as e:
        if not silent:
            print("URLError: "+ str(e.reason))
    except urllib2.HTTPError as e:
        if not silent:
            print("HTTPError: "+ str(e.code))
            print("HTTPError: "+ str(e.read()))
    return defaultRes

def encodeURIComponent(uricomp):
    return urllib2.quote(uricomp.encode("utf-8"))
