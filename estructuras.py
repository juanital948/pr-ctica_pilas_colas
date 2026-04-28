
import random

class Node:
  __slots__ = ('__value','__next')

  def __init__(self,value):
    self.__value = value
    self.__next = None

  def __str__(self):
    return str(self.__value)

  @property
  def next(self):
    return self.__next

  @next.setter
  def next(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("next debe ser un objeto tipo nodo ó None")
    self.__next = node

  @property
  def value(self):
    return self.__value

  @value.setter
  def value(self,newValue):
    if newValue is None:
      raise TypeError("el nuevo valor debe ser diferente de None")
    self.__value = newValue


class LinkedList:

  def __init__(self):
    self.__head = None
    self.__tail = None
    self.__size = 0

  @property
  def head(self):
    return self.__head

  @property
  def tail(self):
    return self.__tail

  @property
  def size(self):
    return self.__size

  @head.setter
  def head(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("Head debe ser un objeto tipo nodo ó None")
    self.__head = node

  @tail.setter
  def tail(self,node):
    if node is not None and not isinstance(node,Node):
      raise TypeError("Tail debe ser un objeto tipo nodo ó None")
    self.__tail = node

  @size.setter
  def size(self,num):
    self.__size = num

  def __str__(self):
    result = [str(nodo.value) for nodo in self]
    return ' <--> '.join(result)

  def __iter__(self):
    current = self.__head
    while current is not None:
      yield current
      current = current.next

  def append(self,value):
    newnode = Node(value)
    if self.__head is None:
      self.__head = newnode
      self.__tail = newnode
    else:
      self.__tail.next = newnode
      self.__tail = newnode
    self.__size += 1

  def popfirst(self):
    tempNode = self.__head
    if self.__head is None:
      return None
    elif self.__size == 1:
      self.__head = None
      self.__tail = None
      self.__size = 0
    else:
      self.__head = self.__head.next
      self.__size -= 1

    tempNode.next = None
    return tempNode

  def pop(self):
    if self.__head is None:
      return None
    elif self.__size == 1:
      popped_node = self.__head
      self.__head = None
      self.__tail = None
      self.__size = 0
      return popped_node
    else:
      popped_node = self.__tail
      current_node = self.__head
      for _ in range(self.__size-2):
        current_node = current_node.next
      current_node.next = None
      self.__tail = current_node
      self.__size -= 1
      return popped_node


class Queue:

  def __init__(self):
    self.__queue = LinkedList()

  def enqueue(self, e):
    self.__queue.append(e)

  def dequeue(self):
    if self.is_empty():
      return None
    else:
      return self.__queue.popfirst().value

  def is_empty(self):
    return self.__queue.size == 0

  def len(self):
    return self.__queue.size

  def __str__(self):
    result = [str(nodo.value) for nodo in self.__queue]
    return ' -- '.join(result)


class Stack:

  def __init__(self):
    self.__stack = LinkedList()

  def push(self, e):
    self.__stack.append(e)

  def pop(self):
    if self.is_empty():
      return None
    else:
      return self.__stack.pop().value

  def is_empty(self):
    return self.__stack.size == 0

  def len(self):
    return self.__stack.size

  def top(self):
    return self.__stack.tail.value

  def __str__(self):
    result = [str(nodo.value) for nodo in self.__stack]
    return ' | '.join(reversed(result))