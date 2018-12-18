
from Queue import Queue
from threading import Event


class Task:
    def __init__(self, definition, *args, **kwargs):
        self.definition = definition
        self.args = args
        self.kwargs = {}
        if kwargs:
            self.kwargs = kwargs


class MultiThreadingSupport:
    QUEUE_CHECK_TIME = 2000

    def __init__(self, master):
        self.master = master
        self.queue = Queue()
        self.event = Event()
        self.async_task_dict = {}

    def start(self):
        self.master.after(MultiThreadingSupport.QUEUE_CHECK_TIME, self.check_queue)

    def process_queue(self):
        while self.queue.qsize():
            task = self.queue.get()
            result = task.definition(*task.args, **task.kwargs)
            if task in self.async_task_dict:
                self.async_task_dict[task] = result
                self.event.set()

    def put_task(self, task):
        self.queue.put(task)

    def evaluate_task(self, task):
        self.async_task_dict[task] = None
        self.queue.put(task)
        self.event.wait()
        self.event.clear()
        return self.async_task_dict.pop(task, None)

    def check_queue(self):
        if self.queue.qsize():
            self.process_queue()
        self.master.after(MultiThreadingSupport.QUEUE_CHECK_TIME, self.check_queue)


MULTI_THREADING_SUPPORT = None


def set_master(master):
    global MULTI_THREADING_SUPPORT
    MULTI_THREADING_SUPPORT = MultiThreadingSupport(master)
    MULTI_THREADING_SUPPORT.start()


def put(definition, *args, **kwargs):
    if MULTI_THREADING_SUPPORT:
        MULTI_THREADING_SUPPORT.put_task(Task(definition, *args, **kwargs))


def evaluate(definition, *args, **kwargs):
    if MULTI_THREADING_SUPPORT:
        MULTI_THREADING_SUPPORT.evaluate_task(Task(definition, *args, **kwargs))
