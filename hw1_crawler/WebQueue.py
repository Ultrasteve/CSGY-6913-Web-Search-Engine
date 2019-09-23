from queue import PriorityQueue
from Element import Element
from urllib.parse import urlparse
from threading import RLock


# 还需要看看那里需要加同步锁 要import queue element
class WebQueue:
	
	def __init__(self):
		self.type = 'priority'
		# {siteName: urlSet}
		self._novaltyDict = {}
		# {url: indegree}
		self._indegreeDict = {}
		self.__priorityQueue = PriorityQueue() 
		self.__visitedSet = set()
		self.__lock = RLock()

	# 更新两个dict的内部函数
	def offer(self, url, depth):
		# undate novalty
		site = self._getSite(url)
		# self.__lock.acquire()
		if site not in self._novaltyDict:
			self._novaltyDict[site] = set()
		self._novaltyDict[site].add(url)
		#已经被poll过了
		if url in self.__visitedSet:
			self.__updateQueue()
			return
		# update indegree
		if url not in self._indegreeDict:
			self._indegreeDict[url] = 1
			self.__priorityQueue.put(Element(self, url, depth + 1))
		else:
			self._indegreeDict[url] += 1

		self.__updateQueue()
		# self.__lock.release()
		
	def poll(self):
		# self.__lock.acquire()
		res = self.__priorityQueue.get()
		url = res.url
		# 被poll过的进入set
		try:
			self.__visitedSet.add(url)
			# 需要在indegreeDict，novaltyDict里删除
			self._novaltyDict[self._getSite(url)].remove(url)
			del self._indegreeDict[url]
			# 并更新priorityqueue
			self.__updateQueue()
			# self.__lock.release()
		except Exception as e:
			print(e)
		return res

	# todo 是正则表达式parse相关的
	def _getSite(self, url):
		result = urlparse(url)
		return result.netloc

	# 把set里面的remove然后再offer进去
	def __updateQueue(self):
		pqList = list(self.__priorityQueue.queue)
		self.__priorityQueue = PriorityQueue()
		for e in pqList:
			self.__priorityQueue.put(e)
