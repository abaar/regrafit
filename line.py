class Line:
	#saving start & end point
	__gradien=-1
	#saving weight
	__weight=-1

	#saving which vertex its connected to
	__vstart=-1
	__vend=-1
	__tag='unset'

	def SetTag(self,carry):
		self.__tag=carry

	def GetTag(self):
		return self.__tag

	def GetVstart(self):
		return self.__vstart

	def GetVend(self):
		return self.__vend

	def GetWeight(self):
		return self.__weight

	def SetWeight(self,carry):
		self.__weight=carry

	def SetVAll(self,carry):
		self.__vstart=carry[0]
		self.__vend=carry[1]