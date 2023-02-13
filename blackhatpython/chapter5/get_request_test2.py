import urllib.request

url = "https://example.com"

headers = {}
headers["User-Agent"] = "Googlebot"

request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)

print(response.getheaders())
print(response.read())
print(type(response))
response.close()
