import time
class TimerClass:
    def __init__(self):
        self.start_time = time.time()

    def tic(self):
        self.start_time = time.time()

    def toc(self):
        elapsed = time.time() - self.start_time
        return elapsed

    def toc_str(self):
        elapsed = time.time() - self.start_time
        return '{:4.02f}'.format(elapsed)
    
    def toc_print(self):
        print(self.toc_str())
        return self.toc()

if __name__ == '__main__':
    import random

    timer = TimerClass()
    timer.tic()
    print('starting...')
    time.sleep(random.random() * 10)
    print('elapsed time:', timer.toc_str())
