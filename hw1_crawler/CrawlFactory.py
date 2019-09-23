from WebQueue import WebQueue
from Crawler import Crawler
from googlesearch import search 
from bfsQueue import BfsQueue

class CrawlFactory:

	# 获取top10 url, 返回list
	def __getTop10(self, keyWord):
		res = []
		for url in search(keyWord, num=10, pause=2, stop=10):
			res.append(url)
		return res

	def build(self, keyWord, num, bfs=False):
		if bfs is False:
			queue = WebQueue()
		else:
			queue = BfsQueue()
		top10List = self.__getTop10(keyWord)
		for url in top10List:
			queue.offer(url, 0)
		return Crawler(num, queue)
		