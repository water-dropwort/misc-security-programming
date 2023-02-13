import queue
import threading
import os
import urllib.request
import urllib.error

threads = 10

target = "https://water-dropwort.github.io/hugo-pages-test"
directory = "./hugo-pages-test/docs" # ex. JoomlaなどのCMSのフォルダを指定する
filters = [".png"]

os.chdir(directory)

web_paths = queue.Queue()

# directory内のファイルをweb_pathsに格納する。
for r,d,f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r,files)
        # 先頭の「.」を取り除く
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        # filtersに定義した拡張子はキューに格納しない
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib.request.Request(url)

        try:
            response = urllib.request.urlopen(request)
            content = response.read()

            print("[%d] => %s" % (response.code, path))
            response.close()
        except urllib.error.HTTPError as error:
            pass

for i in range(threads):
    print("Spawning thread: %d" % (i))
    t = threading.Thread(target=test_remote)
    t.start()
