class Line:
	#saving start & end point
	__xstart=-1
	__ystart=-1
	__xend=-1
	__yend=-1
	__gradien=-1
	#saving weight
	__weight=-1

	#saving which vertex its connected to
	__vstart=-1
	__vend=-1


	def SetStartPoint(self,carry):
		self.__xstart=carry[0]
		self.__ystart=carry[1]

	def GetStartPoint(self):
		return (self.__xstart,self.__ystart)

	def SetEndPoint(self,carry):
		self.__xend=carry[0]
		self.__yend=carry[0]

	def GetEndPoint(self):
		return (self.__xend,self.__yend)

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

	def IsIntersect(self,xclick,yclick):
		self.__gradien=(self.__yend-self.__ystart)/(self.__xend-self.__xstart)
		gradientarget=(yclick-self.__ystart)/(xclick-self.__xstart)
