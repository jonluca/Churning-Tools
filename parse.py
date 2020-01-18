import os

from bs4 import BeautifulSoup
import re
from queue import Queue

from threading import Thread


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()


directory = os.fsencode('./html')
values = []


def do_thing(filename):
    with open('html/' + filename) as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')
        loc = soup.find(id='section-cardart-image')
        a = soup.find(text='Purchase Annual Percentage Rate (APR)')
        apr = ''
        try:
            sibl = a.parent.parent.parent.next_sibling.contents
            all_text = ''
            for entry in sibl:
                all_text += entry.text

            ind = 0
            if 'Intro APR' in all_text:
                ind = 1
            apr = re.split('\. This|,|that, ', all_text)[ind]
            apr = apr.strip()
        except:
            pass

        af = soup.find(text='Annual Membership Fee')
        fee = ''
        try:
            fee = re.split('\. This|,|Intro', af.parent.parent.parent.next_sibling.contents[0].text)[0]
        except:
            pass
        bon = soup.find(text='after you spend ')
        possible_bonus = ''
        try:
            print(bon)
        except:
            pass
        # contents = table.contents[1].text or ''
        for img in loc.find_all('img', alt=True):
            print(filename.split('.')[0] + ',' + img['alt'] + ',' + apr + ',' + fee.strip())


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".html"):
        values.append(filename)

    else:
        continue
pool = ThreadPool(1)

pool.map(do_thing, values)
pool.wait_completion()  # NB. Original query string below. It seems impossible to parse and  # reproduce query strings 100% accurately so the one below is given  # in case the reproduced version is not "correct".  # response = requests.get('https://applynow.chase.com/FlexAppWeb/Secured/renderApp.do?Chase3FramedPage=true&cipDomain=secure05c.chase.com&SPID=FZ6R', headers=headers, cookies=cookies)
