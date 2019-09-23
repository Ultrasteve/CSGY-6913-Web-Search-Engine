import re

class BlackList:
	def __init__(self):
		list = ['.mp4','.mp3','.jpg','.gif','.avi','.mov','.navi','.rm','.asf','.flv','.3gp','.wma','.rmvb','.mpg','.mkv','.png','.jpeg','.svg','.tif','.js']
		self.__blacklist = set(list)

	def isValid(self, url):
		# if re.match('^(http|https).*', url) is None:
		# 	return False
		suffix = self.__getSuffix(url)
		if len(suffix) == 0:
			return True
		return self.__contains(suffix) is False

	def __getSuffix(self, url):
		res = re.findall(r'\/.+(\.[a-z]+)', url)
		if len(res) > 0:
			return res[0]
		return res

	def __contains(self, suffix):
		return suffix.lower() in self.__blacklist