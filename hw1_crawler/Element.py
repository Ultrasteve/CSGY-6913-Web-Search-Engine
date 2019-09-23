class Element:
	def __init__(self, obj, url, depth):
		if obj.type == 'priority':
			self.obj = obj
			self.url = url
			self.site = self.obj._getSite(self.url)
			self.depth = depth
			self.score = self.obj._indegreeDict[self.url] - 0.8*len(self.obj._novaltyDict[self.site])
		else:
			self.url = url
			self.depth = depth
			self.score = 0
    # python 内部类访问外部私有变量 --- 需要传入外部类的引用
    # py到底是大根堆还是小根堆 --- 小根堆
	def __lt__(self, other):
		return self.score > other.score