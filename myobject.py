from line import Line
from vertex import Vertex
from graph import Graph

class MyObject:
	__myvertex=[]
	__myline=[]
	__mymst=[]
	__intmax=1000000000000
	def PushMyVertex(self,carry):
		self.__myvertex.append(carry)

	def PushMyLine(self,carry):
		self.__myline.append(carry)
	
	def GetMyVertexSize(self):
		return len(self.__myvertex)
	
	def GetMyLineSize(self):
		return len(self.__myline)
	
	def GetMyVertexAt(self,i):
		if (i<len(self.__myvertex)):
			return self.__myvertex[i]
		else:
			return -1
	
	def GetMyLineAt(self,i):
		if (i<len(self.__myline)):
			return self.__myline[i]
		else:
			return -1
	
	def DelMyVertexAt(self,i):
		#del myvertex with index i
		del self.__myvertex[i]
	
	def DelMyLineAt(self,i):
		#del myline with index i
		del self.__myline[i]
	
	def DelMyVertexAll(self):
		del self.__myvertex[:]
		self.__myvertex=[]
	
	def DelMyLineAll(self):
		del self.__myline[:]
		self.__myline=[]
	
	def GetMyMstAt(self,i):
		if (i<len(self.__mymst)):
			return self.__mymst[i]
	
	def DelMyMstAll(self):
		del self.__mymst[:]
		self.__mymst=[]
	
	def GetMyMstSize(self):
		return len(self.__mymst)
	
	def Compute(self,algorithm,val1,val2):
		if(algorithm=="Kruskal"):
			#Creating MST using Kruskal, steps :
			# 1. Sort it based on its weight
			# 2. Push from the smallest to the highest with no cyclic
			self.DelMyMstAll()
			cyclicchecker=Graph(len(self.__myvertex))
			for i in range(0,len(self.__myline)):
				index = i 
				temp = self.__myline[i].GetWeight()
				for j in range(i+1,len(self.__myline)):
					temp2 = self.__myline[j].GetWeight()
					if (temp2<temp):
						temp=temp2
						index=j
				temp = self.__myline[i]
				self.__myline[i]=self.__myline[index]
				self.__myline[index]=temp
				#print(self.__myline[i].GetWeight())

			for i in range(0,len(self.__myline)):
				cyclicchecker.addEdge(self.__myline[i].GetVstart(),self.__myline[i].GetVend())
				if (cyclicchecker.isCyclic()):
					cyclicchecker.deleteEdge(self.__myline[i].GetVstart(),self.__myline[i].GetVend())
				else:
					self.__mymst.append(self.__myline[i])
			del cyclicchecker
		elif (algorithm=="Djikstra"):
			self.DelMyMstAll()
			#
			dist=[]
			predecessor=[]
			visited=[]
			route=[]
			for x in range(0,len(self.__myvertex)):
				dist.append(self.__intmax)
				visited.append(False)
				predecessor.append(-1)
				route.append([])
			dist[val1]=0
			predecessor[val1]=val1
			predec=val1

			for i in range(0,len(self.__myvertex)):
				
				#find minimum dist of current spt
				hold=self.__intmax
				u=0
				for j in range(0,len(self.__myvertex)):
					if (visited[j]==False and hold>dist[j]):
						hold=dist[j]
						u=j

				# predecessor[u]=predec

				if (i==0):
					route[val1].append(val1)
				else:
					idx=predecessor[u]
					#print(str(u) +" "+str(idx)+" "+ str(route[idx]))
					for j in range(0,len(route[idx])):
						route[u].append(route[idx][j])
					route[u].append(u)

				#set true since it's selected to be the next spt
				visited[u]=True

				#updating distance
				for j in range(0,len(self.__myline)):
					vstart=self.__myline[j].GetVstart()
					vend=self.__myline[j].GetVend()
					if(u==vstart and u!=vend):
						v=vend
						if (visited[v]==False and dist[u]!=self.__intmax and dist[u]+self.__myline[j].GetWeight()<dist[v]):
							dist[v]=dist[u]+self.__myline[j].GetWeight()
							predecessor[v]=u
					elif(u==vend and u!=vstart):
						v=vstart
						if (visited[v]==False and dist[u]!=self.__intmax and dist[u]+self.__myline[j].GetWeight()<dist[v]):
							dist[v]=dist[u]+self.__myline[j].GetWeight()
							predecessor[v]=u

				predec=u
			print(route[val2])


		elif(algorithm=="Prims"):
			self.DelMyMstAll()
			visited=[]
			mylist=[]
			mylist_cyclic=[]
			for i in range (0,len(self.__myvertex)):
				visited.append(False)

			visited[val1]=True

			for i in range (0, len(self.__myline)):
				if (self.__myline[i].GetVstart()==val1 or self.__myline[i].GetVend()==val1):
					mylist.append(i)
					# i-th line with 0 means not yet taken
			cyclicchecker=Graph(len(self.__myvertex))

			while(len(mylist)!=0):
				smallest=self.__intmax
				idx=0
				for i in range(0,len(mylist)):
					if (smallest>self.__myline[mylist[i]].GetWeight()):
						smallest=self.__myline[mylist[i]].GetWeight()
						idx=i

				cyclicchecker.addEdge(self.__myline[mylist[idx]].GetVstart(),self.__myline[mylist[idx]].GetVend())
				
				if (cyclicchecker.isCyclic()):
					cyclicchecker.deleteEdge(self.__myline[mylist[idx]].GetVstart(),self.__myline[mylist[idx]].GetVend())
					mylist_cyclic.append(mylist[idx])
					del mylist[idx]

				else:
					self.__mymst.append(self.__myline[mylist[idx]])
					target=0
					if (visited[self.__myline[mylist[idx]].GetVstart()]==True):
						target=self.__myline[mylist[idx]].GetVend()
						visited[target]=True
					else:
						target=self.__myline[mylist[idx]].GetVstart()
						visited[target]=True

					

					for j in range(0,len(self.__myline)):
						if (self.__myline[j].GetVstart()==target and visited[self.__myline[j].GetVend()]==False):
							mylist.append(j)
							
						elif (self.__myline[j].GetVend()==target and visited[self.__myline[j].GetVstart()]==False):
							mylist.append(j)
		
			
					visited[target]=True
					del mylist[idx]
			del cyclicchecker
		elif (algorithm=="coloring"):
			
		for i in range(0,len(self.__mymst)):
			print(str(self.__mymst[i].GetVstart()) + " " + str(self.__mymst[i].GetVend()))
		#end of conditional algorithm
	#end of compute method
#end of class