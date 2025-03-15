class Set:
    def __init__(self, iterable=None):
        self._set = set(iterable) if iterable else set()
        self._list = list(self._set)  # Maintain ordered list of elements
    
    def add(self, element):
        if element not in self._set:
            self._set.add(element)
            self._list.append(element)
    
    def remove(self, element):
        self._set.remove(element)
        self._list.remove(element)
    
    def discard(self, element):
        if element in self._set:
            self._set.discard(element)
            self._list.remove(element)
    
    def pop(self):
        element = self._list.pop()
        self._set.remove(element)
        return element
    
    def clear(self):
        self._set.clear()
        self._list.clear()
    
    def union(self, other):
        new_set = Set()
        for element in self._list:
            new_set.add(element)
        for element in other._list:
            new_set.add(element)
        return new_set
    
    def intersection(self, other):
        new_set = Set()
        for element in self._list:
            if element in other._set:
                new_set.add(element)
        return new_set
    
    def difference(self, other):
        new_set = Set()
        for element in self._list:
            if element not in other._set:
                new_set.add(element)
        return new_set
    
    def symmetric_difference(self, other):
        new_set = Set()
        for element in self._list:
            if element not in other._set:
                new_set.add(element)
        for element in other._list:
            if element not in self._set:
                new_set.add(element)
        return new_set
    
    def update(self, other):
        for element in other._list:
            self.add(element)
    
    def intersection_update(self, other):
        to_remove = []
        for element in self._list:
            if element not in other._set:
                to_remove.append(element)
        for element in to_remove:
            self.remove(element)
    
    def difference_update(self, other):
        for element in other._list:
            self.discard(element)
    
    def symmetric_difference_update(self, other):
        to_remove = []
        to_add = []
        for element in self._list:
            if element in other._set:
                to_remove.append(element)
        for element in other._list:
            if element not in self._set:
                to_add.append(element)
        for element in to_remove:
            self.remove(element)
        for element in to_add:
            self.add(element)
    
    def issubset(self, other):
        return self._set <= other._set
    
    def issuperset(self, other):
        return self._set >= other._set
    
    def isdisjoint(self, other):
        return self._set.isdisjoint(other._set)
    
    def copy(self):
        new_set = Set()
        for element in self._list:
            new_set.add(element)
        return new_set
    
    def size(self):
        return len(self._list)
    
    def contains(self, element):
        return element in self._set
    
    def to_frozenset(self):
        return frozenset(self._set)
    
    def enumerate(self):
        return list(enumerate(self._list))
    
    def filter(self, func):
        new_set = Set()
        for element in self._list:
            if func(element):
                new_set.add(element)
        return new_set
    
    def map(self, func):
        new_set = Set()
        for element in self._list:
            new_set.add(func(element))
        return new_set
    
    def reduce(self, func, initializer=None):
        from functools import reduce
        return reduce(func, self._list, initializer) if initializer else reduce(func, self._list)
    
    def __iter__(self):
        return iter(self._list)  # Use ordered list for iteration
    
    def __len__(self):
        return len(self._list)
    
    def __contains__(self, item):
        return item in self._set
    
    def __add__(self, other):
        return self.union(other)
    
    def __sub__(self, other):
        return self.difference(other)
    
    def __matmul__(self, other):
        return self.intersection(other)
    
    def __repr__(self):
        return f"Set({self._list})"
