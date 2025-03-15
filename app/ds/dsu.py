from app.ds.set import Set

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))  # Each node is its own parent
        self.rank = [1] * n  # Rank helps in Union by Rank
        self.sets = Set()  # Track sets of elements
        for i in range(n):
            self.sets.add(Set([i]))  # Each element starts in its own set

    def find(self, x):
        if self.parent[x] != x:  # Path compression
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:  # Only merge if different sets
            # Find the corresponding sets
            setX = next(s for s in self.sets if rootX in s)
            setY = next(s for s in self.sets if rootY in s)
            
            # Merge sets based on rank
            if self.rank[rootX] > self.rank[rootY]:  # Attach smaller under larger
                self.parent[rootY] = rootX
                new_set = setX.union(setY)
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
                new_set = setX.union(setY)
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1  # Increase rank when merging equal rank trees
                new_set = setX.union(setY)
            
            # Update sets
            self.sets.discard(setX)
            self.sets.discard(setY)
            self.sets.add(new_set)

    def get_sets(self):
        return self.sets.copy()

    def split(self, x):
        """
        Splits element x into its own set
        """
        root = self.find(x)
        # Find the set containing x
        old_set = next(s for s in self.sets if root in s)
        
        # Create new sets
        remaining_set = Set([i for i in old_set if i != x])
        new_set = Set([x])
        
        # Update sets collection
        self.sets.discard(old_set)
        if len(remaining_set) > 0:
            self.sets.add(remaining_set)
        self.sets.add(new_set)
        
        # Update DSU structure
        self.parent[x] = x
        self.rank[x] = 1