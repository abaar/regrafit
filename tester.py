from myobject import MyObject
from line import Line
from vertex import Vertex

A=Line()
A.SetStartPoint((0,1))
A.SetWeight(10)
A.SetVAll((1,2))
print(A.GetStartPoint())

B=Vertex()
B.SetPosition((0,1))
print(B.GetPosition())

C=MyObject()
C.PushMyVertex(B)
C.PushMyLine(A)
C.Compute("Kruskal")
print(C.GetMyMstAt(0).GetStartPoint())

C.DelMyLineAll()
print(C.GetMyLineAt(0))