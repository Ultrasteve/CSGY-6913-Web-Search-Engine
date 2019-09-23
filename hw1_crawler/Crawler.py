import urllib
import datetime
import time
import threading
from urllib import request
from WebQueue import WebQueue
from Log import Log
from RobotParse import RobotParse
from BlackList import BlackList
from bs4 import BeautifulSoup
from urllib import parse
from atomicCounter import AtomicCounter
from concurrent.futures import ThreadPoolExecutor

'''
爬虫
目标是提高吞吐量
尝试使用普通线程，线程池，协程
'''
class Crawler:

	#初始化参数，优先队列（筛选策略），新鲜度和入度的邻接表
	def __init__(self, num, queue):
		self.__webQueue = queue
		self.__siteNum = num
		self.__log = Log(num)
		self.__robotparser = RobotParse()
		self.__blacklist = BlackList()
		self._totalSize = 0
		self._numOfHttpError = AtomicCounter()
		self._numOfError = AtomicCounter()

	#启动爬虫 使用线程池来管理getPage线程，并注册回调parseData
	def run(self):
		with ThreadPoolExecutor(max_workers=10) as pool: 
			# 线程池 submit
			totalsubmit = 0
			while totalsubmit - self._numOfError.get() <= self.__siteNum:
				# print(e.url)
				totalsubmit += 1
				handler = pool.submit(self.getPage)
				handler.add_done_callback(self.parseData)
			print("完成了")
			self.__log.flush()
			pool.shutdown(wait=False)

		# for i in range(10):
		# 	try:
		# 		t = threading.Thread(target=self.getPage)
		# 		t.setName("MyThread-" + str(i))
		# 		t.start()
		# 		# thread.start_new_thread(getPage)
		# 	except Exception as e:
		# 		print(e)

	# 采集器
	# def getPage(self):
	# 	while self.__log.getLogNum() < self.__siteNum:
	# 		print("getPage now!")
	# 		e = self.__webQueue.poll()
	# 		try:
	# 			req = urllib.request.Request(e.url)
	# 			response = request.urlopen(req, timeout=5)
	# 			if response.getcode() == 404:
	# 				self._numOfHttpError.incr()
	# 		except Exception as e:
	# 			print("Crawler.getPage:")
	# 			print(e)
	# 			return False
	# 		else:
	# 			# msg (url, depth, size, priority, timestemp)
	# 			data = response.read()
	# 			self._totalSize += len(data)
	# 			msg = (e.url, str(len(data)) + 'B', e.depth, response.getcode(), e.score, time.asctime(time.localtime()))
	# 			self.__log.insert(msg)
	# 			self.parseData(e, data.decode('utf-8'))
	def getPage(self):
		print("getPage now!")
		if self.__log.getLogNum() >= self.__siteNum:
			return
		e = self.__webQueue.poll()
		try:
			req = urllib.request.Request(e.url)
			response = request.urlopen(req, timeout=1)
			if response.getcode() == 404:
				self._numOfHttpError.incr()
		except Exception as e:
			print("Crawler.getPage:")
			print(e)
			self._numOfError.incr()
			return False
		else:
			# msg (url, depth, size, priority, timestemp)
			data = response.read()
			self._totalSize += len(data)
			msg = (e.url, str(len(data)) + 'B', e.depth, response.getcode(), e.score, time.asctime(time.localtime()))
			print(e.url)
			self.__log.insert(msg)
			return e, data.decode('utf-8')
	
	# def parseData(self, e, data):
	# 	# result = future.result()
	# 	url = e.url
	# 	prevDepth = e.depth
		
	# 	soup = BeautifulSoup(data, "html5lib")
	# 	site = self.__getSite(url)
	# 	for a in soup.find_all('a', href=True):
	# 		curUrl = parse.urljoin(site, a['href'])
	# 		try:
	# 			if self.__robotparser.canFetch(curUrl) and self.__blacklist.isValid(curUrl):
	# 				self.__webQueue.offer(curUrl, prevDepth)
	# 		except Exception as e:
	# 			print("Crawler.parseData:")
	# 			print(e)
	def parseData(self, future):
		print('parseData now')
		if self.__log.getLogNum() >= self.__siteNum:
			return
		result = future.result()
		if result is False:
			print("get出错了")
			return
		if self.__webQueue.queueSize() > 300:
			return
		url = result[0].url
		data = result[1]
		prevDepth = result[0].depth
		soup = BeautifulSoup(data, "html5lib")
		site = self.__getSite(url)
		for a in soup.find_all('a', href=True):
			curUrl = parse.urljoin(site, a['href'])
			try:
				#这一块的错误需要好好处理
				if self.__webQueue.queueSize() > 300:
					break
				if self.__robotparser.canFetch(curUrl) and self.__blacklist.isValid(curUrl):
					# print('finish robot')
					# print(time.asctime(time.localtime()))
					self.__webQueue.offer(curUrl, prevDepth)
			except Exception as e:
				print("Crawler.parseData:")
				print(e)


	def __getSite(self, url):
		result = parse.urlparse(url)
		return 'http://' + result.netloc

		

