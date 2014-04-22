import codecs
import hashlib
import os
import urllib2

API_URL = "http://www.vam.ac.uk/api/json/museumobject/"


class VACrawl:

    def __init__(self, api_url=None):

        if api_url:
            self.api_url = api_url
        else:
            self.api_url = API_URL

    def hash_to_dirs(self, hash):
        n = 2
        dirs = [hash[i:i + n] for i in range(0, len(hash), n)]
        return dirs

    def crawl(self, update=False):

        for i in range(0, 2000000):

            filename = "O%d.json" % (i)
            print filename
            h = hashlib.new('sha1')
            h.update(filename)
            dirs = self.hash_to_dirs(h.hexdigest()[0:4])
            dir_path = os.path.join(*dirs)

            file_path = os.path.join(dir_path, filename)
            if update is False and os.path.exists(file_path):
                print "Skipping", filename
                continue

            req_url = "%sO%d" % (self.api_url, i)
            try:
                resp = urllib2.urlopen(req_url, timeout=5)
                json = resp.read()
                os.makedirs(dir_path)
                f = codecs.open(file_path, 'w', 'utf8')
                f.write(json)
                f.close()
            except urllib2.HTTPError, e:
                if e.code == 404:
                    print 'Not found'
                    continue
            except os.error, e:
                print 'path exists'

            yield file_path

if __name__ == "__main__":

    u = "http://localhost/~barrettsmall/Sites/fake/"
    c = VACrawl(api_url=u)

    for n in c.crawl():
        print n
