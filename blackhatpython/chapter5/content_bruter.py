import urllib.request
import urllib.parse
import threading
import queue

target_url    = "https://water-dropwort.github.io/hugo-pages-test"
wordlist_file = "wordlist.txt"
resume        = b"init"
threads       = 5

def build_wordlist(wordlist_file):
    # 単語の辞書を読み取る
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words        = queue.Queue()

    # 単語をキューに格納する
    # resumeに単語が入っているときはその単語以降の単語をキューに格納する
    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            elif word == resume:
                found_resume = True
                print("Resuming wordlist from: %s" % (resume))
        else:
            words.put(word)
    return words

def dir_bruter(word_queue, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []
        # ファイル拡張子があるかどうかをチェックする。
        # もしなければディレクトリのパスとして総当たり攻撃の対象とする。
        if b"." not in attempt:
            attempt_list.append("/%s/" % (attempt.decode()))
        else:
            attempt_list.append("/%s" % (attempt.decode()))

        # 拡張子の総当りをしたい場合
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt.decode(), extension))

        # 作成したリストの最後まで繰り返す
        for brute in attempt_list:
            url = "%s%s" % (target_url, urllib.parse.quote(brute))
            print(url)
            try:
                r = urllib.request.Request(url)

                response = urllib.request.urlopen(r)

                if len(response.read()):
                    print("[%d] => %s" % (response.code, url))
            except urllib.error.URLError as e:
                if hasattr(e, "code") and e.code != 404:
                    print("!!! %d => %s" % (e.code, url))
                pass

word_queue = build_wordlist(wordlist_file)
extensions = [".txt",".xml", ".html"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter, args=(word_queue, extensions,))
    t.start()
