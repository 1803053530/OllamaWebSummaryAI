import threading
import time
import random
from tqdm import tqdm

class ProgressController:
    def __init__(self):
        self.pbar = None          # 进度条实例
        self._running = False     # 控制线程运行的标志
        self._lock = threading.Lock()  # 线程锁

    def start(self):
        """启动进度条线程"""
        self._running = True
        self.pbar = tqdm(total=100, desc="处理进度")
        # 启动独立线程更新进度
        threading.Thread(target=self._auto_update, daemon=True).start()

    def _auto_update(self):
        """后台自动更新进度"""
        while self._running and self.pbar.n < 100:
            with self._lock:  # 获取锁保证线程安全
                increment = random.uniform(0.5, 2.5)  # 随机增量更自然
                self.pbar.update(increment)
            time.sleep(random.randint(2,5))  # 更新间隔0.1秒

    def complete(self):
        """完成进度条"""
        with self._lock:
            if self._running:
                self._running = False  # 停止线程
                # 补满剩余进度
                remaining = 100 - self.pbar.n
                if remaining > 0:
                    self.pbar.update(remaining)
                self.pbar.close()  # 关闭进度条