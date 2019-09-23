from os.path import isfile
from atomicCounter import AtomicCounter
from threading import RLock


class Log:
	def __init__(self, num):
		self.__cache = []
		self.__logNum = AtomicCounter()
		fileNum = 1
		while isfile('log' + str(fileNum) + '.txt'):
			fileNum += 1
		self.__fileName = 'log' + str(fileNum) + '.txt'
		self.__lock = RLock()
		self.__roundNum = num / 50
		self.__roundCnt = 0

	# 插入msg到log中 
	# msg所有信息都是外部传进来的
	def insert(self, msg):
		self.__lock.acquire()
		if self.__roundNum == self.__roundCnt:
			self.flush()
			self.__lock.release()
			return
		self.__cache.append(msg)
		cnt = self.__logNum.incr()
		print("log insert!")
		print(len(self.__cache))
		if len(self.__cache) >= 50:
			file = open(self.__fileName, 'a')
			print("saving...")
			for idx, m in enumerate(self.__cache):
				st = ", ".join(str(s) for s in m) + ", " + str(cnt - 50 + idx + 1) + '\n'
				file.write(st)
			self.__cache.clear()
			file.close()
			self.__roundCnt += 1
			print("finish")
		
		self.__lock.release()

	# 获取日志条目数量
	def getLogNum(self):
		return self.__logNum.get()

	#在程序要退出的时候flush缓冲区
	def flush(self):
		if len(self.__cache) == 0:
			return
		file = open(self.__fileName, 'a')
		for idx, m in enumerate(self.__cache):
			st = ", ".join(str(s) for s in m) + ", " + str(self.__logNum.get() - 10 + idx) + '\n'
			file.write(st)
		self.__cache.clear()
		file.close()