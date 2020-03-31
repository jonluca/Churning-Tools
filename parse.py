import os
import re
from queue import Queue
from threading import Thread

from bs4 import BeautifulSoup


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


direc = '../mar2020/'
directory = os.fsencode(direc)
values = []


def do_thing(filename):
  with open(direc + filename) as file:
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
      fee = re.split('\. This|,|Intro',
                     af.parent.parent.parent.next_sibling.contents[0].text)[0]
    except:
      pass
    # contents = table.contents[1].text or ''
    images = []
    if loc:
      images = loc.find_all('img', alt=True)
      if not images:
        loc = soup.find_all('div', {
          'class': lambda x: x and 'chaseui-pagelogo' in x.split()})
        if loc:
            images = loc[0].find_all('img', alt=True)

    for img in images:
      print(filename.split('.')[0] + ',' + img[
        'alt'] + ',' + apr + ',' + fee.strip())
    if not images:
      title = soup.find_all('div', {
        'class': lambda x: x and 'jpui-aoo-card-name' in x.split()})
      if title:
        title = title[0].text
      else:
        title = "unknown"
      print(filename.split('.')[
              0] + ',' + title.strip() + ',' + apr + ',' + fee.strip())


all_files = os.listdir(directory)
all_files.sort()

for file in all_files:
  filename = os.fsdecode(file)
  if filename.endswith(".html"):
    do_thing(filename)
  else:
    continue
