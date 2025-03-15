class Graph:

    sparseness_threshold = 0.3

    def __init__(self, size, representation="flexible"):
        self.size = size
        self.representation = representation
        self.adjacency_matrix = [[[] for _ in range(size)] for _ in range(size)] if representation in ["matrix", "flexible"] else None
        self.adjacency_list = {i: [] for i in range(size)} if representation in ["list", "flexible"] else None

    def add_edge(self, src, dest, weight):
        """
        Adds a directed edge with a string weight from src to dest.
        Multiple edges with different weights are allowed between same vertices.
        """
        if self.representation in ["matrix", "flexible"]:
            self.adjacency_matrix[src][dest].append(weight)
        if self.representation in ["list", "flexible"]:
            self.adjacency_list[src].append((dest, weight))
        self.switch_representation()

    def delete_edge(self, src, dest, weight=None):
        """
        Deletes the directed edge(s) from src to dest.
        If weight is specified, only deletes edges with that weight.
        """
        if self.representation in ["matrix", "flexible"]:
            if weight is None:
                self.adjacency_matrix[src][dest] = []
            else:
                self.adjacency_matrix[src][dest] = [w for w in self.adjacency_matrix[src][dest] if w != weight]
        
        if self.representation in ["list", "flexible"]:
            if weight is None:
                self.adjacency_list[src] = [(d, w) for d, w in self.adjacency_list[src] if d != dest]
            else:
                self.adjacency_list[src] = [(d, w) for d, w in self.adjacency_list[src] if not (d == dest and w == weight)]
        
        self.switch_representation()

    def add_vertex(self):
        """
        Adds a new vertex to the graph.
        """
        self.size += 1
        if self.representation in ["matrix", "flexible"]:
            for row in self.adjacency_matrix:
                row.append([])
            self.adjacency_matrix.append([[] for _ in range(self.size)])
        if self.representation in ["list", "flexible"]:
            self.adjacency_list[self.size - 1] = []
        self.switch_representation()  # Automatically switch representation

    def delete_vertex(self, vertex):
        """
        Deletes a vertex and all its associated edges.
        """
        if self.representation in ["matrix", "flexible"]:
            self.adjacency_matrix.pop(vertex)
            for row in self.adjacency_matrix:
                row.pop(vertex)
        if self.representation in ["list", "flexible"]:
            self.adjacency_list.pop(vertex)
            for src in self.adjacency_list:
                self.adjacency_list[src] = [(d, w) for d, w in self.adjacency_list[src] if d != vertex]
        self.size -= 1
        self.switch_representation()  # Automatically switch representation

    def set_edge_weight(self, src, dest, weight):
        """
        Updates the weight of an existing edge.
        """
        if self.representation in ["matrix", "flexible"]:
            self.adjacency_matrix[src][dest].append(weight)
        if self.representation in ["list", "flexible"]:
            for i, (d, w) in enumerate(self.adjacency_list[src]):
                if d == dest:
                    self.adjacency_list[src][i] = (dest, weight)
                    break

    def get_edges(self, src, dest=None):
        """
        Returns all edges (weights) from src to dest.
        If dest is None, returns all edges from src.
        """
        if self.representation == "matrix":
            if dest is None:
                return [(d, w) for d in range(self.size) for w in self.adjacency_matrix[src][d]]
            return self.adjacency_matrix[src][dest]
        else:  # list
            if dest is None:
                return self.adjacency_list[src]
            return [w for d, w in self.adjacency_list[src] if d == dest]

    def switch_representation(self):
        """
        Modified to handle lists of weights instead of single weights and edge cases
        """
        # If size is 0 or 1, no need to switch representations
        if self.size <= 1:
            return

        edge_count = sum(
            sum(1 for weights in row for _ in weights)
            for row in self.adjacency_matrix
        ) if self.representation in ["matrix", "flexible"] else sum(
            len(edges) for edges in self.adjacency_list.values()
        )
        sparseness = edge_count / (self.size * (self.size - 1))

        if sparseness > self.sparseness_threshold and self.representation != "matrix":
            # Switch to matrix
            self.adjacency_matrix = [[[] for _ in range(self.size)] for _ in range(self.size)]
            for src, edges in self.adjacency_list.items():
                for dest, weight in edges:
                    self.adjacency_matrix[src][dest].append(weight)
            self.adjacency_list = None
            self.representation = "matrix"
        elif sparseness <= self.sparseness_threshold and self.representation != "list":
            # Switch to list
            self.adjacency_list = {i: [] for i in range(self.size)}
            for src in range(self.size):
                for dest in range(self.size):
                    for weight in self.adjacency_matrix[src][dest]:
                        self.adjacency_list[src].append((dest, weight))
            self.adjacency_matrix = None
            self.representation = "list"

    def remove_duplicate_edges(self):
        """
        Removes duplicate edges (same source, destination, and weight).
        """
        if self.representation == "matrix":
            # For matrix representation
            for i in range(self.size):
                for j in range(self.size):
                    # Convert list to set and back to remove duplicates
                    self.adjacency_matrix[i][j] = list(set(self.adjacency_matrix[i][j]))
        else:
            # For list representation
            for src in self.adjacency_list:
                # Convert to set of (dest, weight) tuples and back to list
                self.adjacency_list[src] = list(set((dest, weight) for dest, weight in self.adjacency_list[src]))

        # Switch representation if needed after removing duplicates
        self.switch_representation()
    
    def get_edges_count(self):
        """
        Returns the number of edges in the graph.
        """
        if self.representation == "matrix":
            return sum(sum(len(weights) for weights in row) for row in self.adjacency_matrix)
        else:
            return sum(len(edges) for edges in self.adjacency_list.values())
