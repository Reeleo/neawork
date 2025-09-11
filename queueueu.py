
class Queue:
    def __init__(self):
        self.items = []
        self.front = 0
        self.rear = 0
        self.maxSize = 5

    
    def isEmpty(self):
        if len(self.items) == 0:
            return True
        return False
    
    def isFull(self):
        if len(self.items) >= 5:
            return True
        return False
    
    def enqueue(self,newitem):
        if not self.isFull():
            self.items.append(newitem)
            self.rear += 1
        else:
            print("Queue is too full")
    
    def dequeue(self):
        if not self.isEmpty():
            self.items.pop(0)
            self.rear -= 1
        else:
            print("Queue is empty")
        
    def display(self):
        print(self.items)


        
queue = Queue()
queue.enqueue("hi")
queue.enqueue("hello")
queue.dequeue()
queue.isEmpty()
queue.isFull()
queue.display()
