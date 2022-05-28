from cgi import test
from concurrent.futures import thread
import utils.multi_threader
import utils.requester
import time

def test_multithreader():
    # Make sure multithreader can run two threads printing time
    def funct1():
        print(time.time())
    def funct2():
        time.sleep(1)
        print(time.time())


    threads = [utils.multi_threader.Thread(funct1), utils.multi_threader.Thread(funct2)]

    for i in threads:
        i.start()
        i.join()

def test_multithreader_params():
    def funct1(thread_name):
        print(thread_name,time.time())
    def funct2(thread_name):
        time.sleep(1)
        print(thread_name,time.time())


    threads = [utils.multi_threader.Thread(funct1, "1"), utils.multi_threader.Thread(funct2, "2")]

    for i in threads:
        i.start()
        i.join()


def test_requester():
    requester = utils.requester.Requester()
    requester.connect_and_get_data()
    print(requester.status)
    print(requester.string[0:100])





if __name__ == "__main__":
    test_multithreader()
    print("Testing Threading Complete")
    test_multithreader_params()
    print("Testing Threading parameters Complete")
    test_requester()
    print("Testing Requester Complete")
