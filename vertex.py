class Vertex:
	__tag='unset'
	__idx=-1
	def SetTag(self,carry):
		self.__tag=carry
		self.__idx=carry[0][1:]

	def GetTag(self):
		return self.__tag

	def SetIdx(self,carry):
		self.__idx=carry

	def GetIdx(self):
		return self.__idx