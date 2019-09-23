from queue import Queue
from Element import Element
from urllib.parse import urlparse

# 还需要看看那里需要加同步锁 要import queue element
class BfsQueue:
	
	def __init__(self):
		# queue
		self.type = 'bfs'
		self.__queue = Queue()
		self.__visitedSet = set()

	def offer(self, url, depth):
		if url in self.__visitedSet:
			return
		self.__queue.put(Element(self, url, depth + 1))
		# print("queue size:" + str(self.__queue.qsize()))
		self.__visitedSet.add(url)

	def poll(self):
		res = self.__queue.get()
		return res

	def queueSize(self):
		return self.__queue.qsize()
	
