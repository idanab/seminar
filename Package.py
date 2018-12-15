import requests


class Package(object):
    libraries_api_key = "f57c0371f0625d43906febde2009033b"

    def __init__(self, name):
        self.name = name
        self.exists = True
        response = requests.get("https://libraries.io/api/pypi/{}?api_key={}".format(name, Package.libraries_api_key))
        try:
            info = response.json()
        except:
            raise ConnectionAbortedError("api error")
        if info == {"message":"ActiveRecord::RecordNotFound"}:
            self.exists = False
            self.stars = -1
            self.forks = -1
        else:
            self.description = info['description']
            self.stars = info['stars']
            self.forks = info['forks']

    def __gt__(self, other):
        try:
            return self.stars > other.stars or self.forks > other.forks
        except Exception as e:
            print(self, other)
            raise e

    def __repr__(self):
        return "NullPackage" if not self.exists else "{} (stars: {}, forks:{})".format(self.name, self.stars, self.forks)

    def __bool__(self):
        return self.exists