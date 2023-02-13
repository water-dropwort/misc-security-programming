import urllib.request

body = urllib.request.urlopen("https://example.com")

print(body.read())
