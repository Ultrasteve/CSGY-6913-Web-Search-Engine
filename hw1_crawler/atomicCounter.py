from threading import RLock
import threading

class AtomicCounter:
	def __init__(self):
		self.__lock = RLock()
		self.__cnt = 0

	def incr(self):
		self.__lock.acquire()
		# print("log increase: " + threading.Thread().getName())
		self.__cnt += 1
		self.__lock.release()
		return self.__cnt

	def get(self):
		self.__lock.acquire()
		# print("log check: " + threading.Thread().getName())
		res = self.__cnt
		self.__lock.release()
		return res