from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from functools import lru_cache
import time
import socket

socket.setdefaulttimeout(2.0) 

class RobotParse:

	def canFetch(self, url):
		# print(time.asctime(time.localtime()))
		rp = self.__getParser(self.__getSite(url))
		# print("RobotParse now!" + url)
		if rp is False:
			return True
		return rp.can_fetch('*', url)

	@lru_cache(maxsize=50)
	def __getParser(self, url):
		if url == '':
			return False
		site = 'https://' + url + '/robots.txt'
		# print("robotparse: " + site)
		try:
			rp = RobotFileParser(site)
			rp.read()
		except Exception as e:
			return False
		else:	
			return rp

	def __getSite(self, url):
		result = urlparse(url)
		return result.netloc