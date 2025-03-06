# progress.py
import random

from tqdm import tqdm
import time
import threading

class ProgressController:
    def __init__(self, total=100):
        self.total = total
        self._progress = 0
        self._running = False
        self._lock = threading.Lock()
        self.thread = None

    def _update_progress(self):
        with tqdm(total=self.total) as pbar:
            while self._running and self._progress < self.total:
                with self._lock:
                    pbar.n = self._progress
                    pbar.refresh()
                time.sleep(0.1)  # 更新间隔
            # 强制完成
            if self._progress < self.total:
                pbar.n = self.total
                pbar.refresh()

    def start(self):
        self._running = True
        self.thread = threading.Thread(target=self._update_progress)
        self.thread.start()

    def update(self, increment=1):
        with self._lock:
            self._progress = min(self._progress + increment, self.total)
    def complete(self):
        with self._lock:
            self._progress = self.total
            self._running = False
        if self.thread:
            self.thread.join()

class SimpleProgress:
    def __init__(self):
        self.pbar = None
        self.stop_flag = False

    def start(self):
        """启动进度条线程"""
        self.pbar = tqdm(total=100)
        # 启动独立线程更新进度
        threading.Thread(target=self._auto_update).start()

    def _auto_update(self):
        """后台自动更新进度"""
        while not self.stop_flag and self.pbar.n < 100:
            increment = random.uniform(0.5, 2.5)  # 随机增量
            self.pbar.update(increment)
            time.sleep(0.1)  # 更新间隔
        # 强制完成
        if self.pbar.n < 100:
            self.pbar.update(100 - self.pbar.n)
        self.pbar.close()

    def complete(self):
        """标记进度完成"""
        self.stop_flag = True