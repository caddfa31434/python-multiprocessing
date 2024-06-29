import time
import asyncio
from multiproc_worker_utils import ResultHandler, ProcessWorkerWrapper, WorkerMonitor

class SimpleWorker:
    def __init__(self):
        pass

    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


def main():
    # 初始化结果处理器
    result_handler = ResultHandler()
    result_handler.start()

    # 创建工作进程包装器
    worker = ProcessWorkerWrapper(result_handler, SimpleWorker)

    # 创建监控线程
    monitor = WorkerMonitor([worker], result_handler)
    monitor.start()

    # 同步执行任务
    future1 = worker.execute_method('add', 1, 2)
    future2 = worker.execute_method('multiply', 3, 4)

    # 获取并打印结果
    print(f"Result of add(1, 2): {future1.get()}")
    print(f"Result of multiply(3, 4): {future2.get()}")

    # 异步执行任务
    async def async_test():
        result = await worker.execute_method_async('add', 5, 6)
        print(f"Result of add(5, 6): {result}")

    asyncio.run(async_test())

    # 清理工作进程和监控器
    monitor.close()
    result_handler.close()

    # 等待所有线程结束
    monitor.join()
    result_handler.join()

if __name__ == "__main__":
    main()

