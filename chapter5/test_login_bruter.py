from login_bruter import Bruter
from login_bruter_test_server import TestHandler
from http.server import HTTPServer
from threading import Thread
from queue import Queue

def list_to_queue(list):
    q = Queue()
    for item in list:
        q.put(item)
    return q

httpd = None
try:
    # start test server
    handler = TestHandler
    httpd = HTTPServer(('', 1234), handler)
    t = Thread(target=httpd.serve_forever)
    t.start()
    print("[*] Test server started.")

    # start bruteforce attack
    pswd_list = ["Tarou", "Taro", "tarou", "taro", "tarou0101", "taro0101", "Tarou0101", "Taro0101"]
    bruter = Bruter(user_name     = "test.tarou@example.com",
                    words         = list_to_queue(pswd_list),
                    user_thread   = 3,
                    target_url    = "http://localhost:1234",
                    target_post   = "http://localhost:1234",
                    success_check = "Welcome")
    bruter.run_bruteforce()
    while True:
        if bruter.attack_completed():
            print("[*] attack completed")
            break;
    
finally:
    if httpd is not None:
        httpd.shutdown()
        print("[*] Test server closed.")
