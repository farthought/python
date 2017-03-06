class Node:  
    next = None  
    data = None  
    def __init__(self,nodeData):  
        self.data = nodeData  
  
class List:  
    root = None  
    size = 0;  
    def __init__(self,newRoot):  
        self.root = newRoot  
    def __init__(self):  
        self.root = None  
        size = 0  
          
    #delete node from root  
    def __del__(self):  
        if self.root is None:  
            return  
        curNode = self.root  
        while curNode.next is not None:  
            tempNode = curNode  
            curNode = curNode.next  
            tempNode = None  
        curNode = None  
    
    #Insert a new node to the list  
    def Insert(self,newData):  
        newNode = Node(newData)  
        if self.root is None:  
            self.root = newNode  
            return  
        tempNode = self.root  
        while tempNode.next is not None:  
            tempNode = tempNode.next  
        tempNode.next = newNode  
        self.size += 1  
          
    #def Get data of Position pos  
    def GetData(self,pos):  
        if pos > self.size or pos < 0:  
            return None  
        else:  
            tempNode = self.root  
            for i in range(0,pos):  
                tempNode = tempNode.next  
            return tempNode.data  
      
    #Remove a certain node  
    def Remove(self,theData):  
        curNode = self.root  
        if curNode is None:  
            return  
        if self.size == 1 and curNode.data == theData:  
            curNode.data = None  
            curNode = None  
            self.size -= 1  
            return  
        while curNode.next is not None:  
            if curNode.next.data == theData:  
                tempNode = curNode.next  
                curNode.next = curNode.next.next  
                tempNode = None  #remove the node,but curNode stays still  
                self.size -= 1  
            else:  
                curNode = curNode.next  
                  
    #Get Root Node  
    def GetRoot(self):  
        return self.root  
          
    #def Get Size  
    def GetSize(self):  
        return self.size  
      
    #print the data of the list  
    def Print(self):  
        tempNode = self.root  
        while tempNode is not None:  
            print (tempNode.data)  
            tempNode = tempNode.next        
