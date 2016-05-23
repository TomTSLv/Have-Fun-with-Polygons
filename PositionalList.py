# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class PositionalList:
  """A sequential container of elements allowing positional access."""
  #-------------------------- nested _Node class --------------------------
  # nested _Node class
  class _Node:
    """Lightweight, nonpublic class for storing a doubly linked node."""
    __slots__ = '_element', '_prev', '_next'            # streamline memory

    def __init__(self, element, prev, next):            # initialize node's fields
      self._element = element                           # user's element
      self._prev = prev                                 # previous node reference
      self._next = next                                 # next node reference


  #-------------------------- nested Position class --------------------------
  class Position:
    """An abstraction representing the location of a single element.

    Note that two position instaces may represent the same inherent
    location in the list.  Therefore, users should always rely on
    syntax 'p == q' rather than 'p is q' when testing equivalence of
    positions.
    """

    def __init__(self, container, node):
      """Constructor should not be invoked by user."""
      self._container = container
      self._node = node
    
    def element(self):
      """Return the element stored at this Position."""
      return self._node._element
      
    def __eq__(self, other):
      """Return True if other is a Position representing the same location."""
      return type(other) is type(self) and other._node is self._node

    def __ne__(self, other):
      """Return True if other does not represent the same location."""
      return not (self == other)               # opposite of __eq__

  #-------------------------- list constructor --------------------------

  def __init__(self):
    """Create an empty list."""
    self._header = self._Node(None, None, None)
    self._trailer = self._Node(None, None, None)
    self._header._next = self._trailer                  # trailer is after header
    self._trailer._prev = self._header                  # header is before trailer
    self._size = 0                                      # number of elements
    self._reverse=False

  #-------------------------- public accessors --------------------------

  def __len__(self):
    """Return the number of elements in the list."""
    return self._size

  def is_empty(self):
    """Return True if list is empty."""
    return self._size == 0

  #-------------------------- nonpublic utilities --------------------------

  def _insert_between(self, e, predecessor, successor):
    """Add element e between two existing nodes and return new node."""
    newest = self._Node(e, predecessor, successor)      # linked to neighbors
    predecessor._next = newest
    successor._prev = newest
    self._size += 1
    return self._make_position(newest)

  def _delete_node(self, node):
    """Delete nonsentinel node from the list and return its element."""
    predecessor = node._prev
    successor = node._next
    predecessor._next = successor
    successor._prev = predecessor
    self._size -= 1
    element = node._element                             # record deleted element
    node._prev = node._next = node._element = None      # deprecate node
    return element                                      # return deleted element
    
  #------------------------------- utility methods -------------------------------
  def _validate(self, p):
    """Return position's node, or raise appropriate error if invalid."""
    if not isinstance(p, self.Position):
      raise TypeError('p must be proper Position type')
    if p._container is not self:
      raise ValueError('p does not belong to this container')
    if p._node._next is None:                  # convention for deprecated nodes
      raise ValueError('p is no longer valid')
    return p._node

  def _make_position(self, node):
    """Return Position instance for given node (or None if sentinel)."""
    if node is self._header or node is self._trailer:
      return None                              # boundary violation
    else:
      return self.Position(self, node)         # legitimate position
    
  #------------------------------- accessors -------------------------------
  def first(self):
    """Return the first Position in the list (or None if list is empty)."""
    if self._reverse:
      return self._make_position(self._trailer._prev)
    else:
      return self._make_position(self._header._next)

  def last(self):
    """Return the last Position in the list (or None if list is empty)."""
    if self._reverse==False:
      return self._make_position(self._trailer._prev)
    else:
      return self._make_position(self._header._next)

  def before(self, p):
    """Return the Position just before Position p (or None if p is first)."""
    node = self._validate(p)
    if self._reverse==False:
      return self._make_position(node._prev)
    else:
      return self._make_position(node._next)

  def after(self, p):
    """Return the Position just after Position p (or None if p is last)."""
    node = self._validate(p)
    if self._reverse:
      return self._make_position(node._prev)
    else:
      return self._make_position(node._next)

  def __iter__(self):
    """Generate a forward iteration of the elements of the list."""
    # if self._reverse==True:
    cursor = self.first()
    while cursor is not None:
      yield cursor.element()
      cursor = self.after(cursor)
    # else:
    #   cursor = self.last()
    #   while cursor is not None:
    #     yield cursor.element()
    #     cursor = self.before(cursor)

  #------------------------------- mutators -------------------------------
 
  def add_first(self, e):
    """Insert element e at the front of the list and return new Position."""
    if self._reverse:
      return self._insert_between(e, self._trailer._prev, self._trailer)
    else:
      return self._insert_between(e, self._header, self._header._next)

  def add_last(self, e):
    """Insert element e at the back of the list and return new Position."""
    if self._reverse==False:
      return self._insert_between(e, self._trailer._prev, self._trailer)
    else:
      return self._insert_between(e, self._header, self._header._next)

  def add_before(self, p, e):
    """Insert element e into list before Position p and return new Position."""
    original = self._validate(p)
    if self._reverse:
      return self._insert_between(e, original, original._next)
    else:
      return self._insert_between(e, original._prev, original)

  def add_after(self, p, e):
    """Insert element e into list after Position p and return new Position."""
    original = self._validate(p)
    if self._reverse==False:
      return self._insert_between(e, original, original._next)
    else:
      return self._insert_between(e, original._prev, original)

  def delete(self, p):
    """Remove and return the element at Position p."""
    original = self._validate(p)
    return self._delete_node(original)  # inherited method returns element

  def replace(self, p, e):
    """Replace the element at Position p with e.

    Return the element formerly at Position p.
    """
    original = self._validate(p)
    old_value = original._element       # temporarily store old element
    original._element = e               # replace with new element
    return old_value                    # return the old element value

  def append(self,L):
    self._trailer._prev._next=L._header._next
    L._header._next._prev=self._trailer._prev
    self._trailer=L._trailer
    self._size+=L._size
    L._header=self._Node(None,None,None)
    L._trailer=self._Node(None,None,None)
    L._header._next = L._trailer                  # trailer is after header
    L._trailer._prev = L._header 
    
    
  def split(self,p):
    L1=PositionalList()
    if self._reverse==False:
      L1._header._next=self._header._next
      self._header._next=p._node._next
      p._node._next._prev=self._header
      L1._trailer._prev=p._node
      p._node._next=L1._trailer
    else:
      L1._header._next=p._node
      a=p._node._prev
      p._node._prev=L1._header
      L1._trailer._prev=self._trailer._prev
      p._node._prev._next=self._trailer
      self._trailer._prev=a
      self._trailer._prev._next=L1._trailer
      L1.reverse()
    self._size=0
    L1._size=0
    for i in self:
      self._size+=1
    for i in L1:
      L1._size+=1


    return L1

  def reverse(self):
    self._reverse=not self._reverse


