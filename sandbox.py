import concurrent.futures
import time

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class Sandbox():
    def run(self):
        future = thread_pool.submit(self.long_task)

    def long_task(self):
        time.sleep(3)
        print('Done')


sandbox = Sandbox()
sandbox.run()
print('Hello')
