class Vertex:
	__xposition=0
	__yposition=0
	__radius=0

	def __init__(self):
		__radius=5

	def SetPosition(self,carry):
		self.__xposition=carry[0]
		self.__yposition=carry[1]

	def GetPosition(self):
		return (self.__xposition,self.__yposition)

	def IsIntersect(self,xclick,yclick):
		xhold=self.__xposition-xclick
		yhold=self.__yposition-yclick

		#Geometry
		#if r > d which d is root(power2of(xhold)+power2of(yhold))
		#	then position / (xclick,yclick) is outside the circle

		xhold=xhold*xhold
		yhold=yhold*yhold

		if(radius*radius >(xhold+yhold)):
			return True
		else:
			return False