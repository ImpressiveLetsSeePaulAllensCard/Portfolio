"""
Alyx Stockton
Assignment 3
Single Source Shortest Path Algorithm (Dijkstra)
All Pairs Shortest Path Algorithm (Floyd-Warshall)
Skeleton code Provided by Steven Geinitz
"""
from queue import PriorityQueue
# for timing checks
import time
# use a very large number as placeholder for infinity
import sys
INF = sys.maxsize


def createAdjMatrix(filename):
    """ Create an adj/weight matrix from a file with verts, neighbors, and weights. """
    f = open(filename, "r")
    n_verts = int(f.readline())
    print(f" n_verts = {n_verts}")
    adjmat = [[INF] * n_verts for i in range(n_verts)]
    for i in range(n_verts):
        adjmat[i][i] = 0
    for line in f:
        int_list = [int(i) for i in line.split()]
        vert = int_list.pop(0)
        assert len(int_list) % 2 == 0
        n_neighbors = len(int_list) // 2
        neighbors = [int_list[n] for n in range(0, len(int_list), 2)]
        distances = [int_list[d] for d in range(1, len(int_list), 2)]
        for i in range(n_neighbors):
            adjmat[vert][neighbors[i]] = distances[i]
    f.close()
    return adjmat


def printAdjMatrix(mat, width=3):
    """ Print an adj/weight matrix padded with spaces and with vertex names. """
    res_str = '     ' + ' '.join([str(v).rjust(width, ' ') for v in range(len(mat))]) + '\n'
    res_str += '    ' + '-' * ((width + 1) * len(mat)) + '\n'
    for i, row in enumerate(mat):
        row_str = [str(elem).rjust(width, ' ') if elem < INF else ' 999' for elem in row]
        res_str += ' ' + str(i).rjust(2, ' ') + ' |' + ' '.join(row_str) + "\n"
    print(res_str)


def dijkstraHeap(W, sv):
    """ Dijkstra's using a priority queue w/ adj matrix W and sv as starting vertex"""
    n = len(W)  # Number of vertices
    dist = [INF] * n  # Initialize distances to infinity for sol mat.
    visited = [False] * n  # Keep track of visited vertices, initalize all to false
    pq = PriorityQueue()  # Priority queue to store vertices based on distance
    dist[sv] = 0  # Distance to start vertex is 0
    pq.put((0, sv))  # Insert start vertex with distance 0 into priority queue

    while not pq.empty():
        # Extract vertex with minimum distance from priority queue
        d, u = pq.get()
        if visited[u]:
            continue
        visited[u] = True

        # Explore neighbors of the extracted vertex
        for v in range(n):
            if W[u][v] != INF and dist[v] > dist[u] + W[u][v]:
                dist[v] = dist[u] + W[u][v]
                pq.put((dist[v], v))

    return dist


def dijkstraArray(W, sv):
    """ Dijkstra's using an array w/ adj matrix W and sv as starting vert. """
    n = len(W)  # Number of vertices in the graph
    distances = [float('inf')] * n  # Initialize distances to infinity
    distances[sv] = 0  # Distance from start vertex to itself is 0
    visited = set()  # Set to keep track of visited vertices

    while len(visited) < n:
        # Find the vertex with the smallest distance that hasn't been visited yet
        min_dist = float('inf')
        min_vertex = None
        for v in range(n):
            if v not in visited and distances[v] < min_dist:
                min_dist = distances[v]
                min_vertex = v

        visited.add(min_vertex)  # Mark the vertex as visited

        # Update distances for neighbors of the current vertex
        for v in range(n):
            if W[min_vertex][v] != 0 and v not in visited:
                # Relaxation step: Update the distance if a shorter path is found
                distances[v] = min(distances[v], distances[min_vertex] + W[min_vertex][v])

    return distances


def floyd(W):
    """
    Carry out Floyd's algorithm using W as a weight/adj matrix.
    The input W is an adjacency matrix that indicate: W[i][j] weight from i to j
    Return a distance matrix where [i][j] entry is the length of the shortest path from
    i to j for all i and j. Should have the same dimensions as input W
    """
    n = len(W)

    # Generate a copy of the input matrix using splicing
    dist = [row[:] for row in W]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    """ Demonstrate the functions, starting with creating the graph. """
    g = createAdjMatrix("graph_20verts.txt")
    if len(g) <= 20:
        printAdjMatrix(g, width=4)

    # Run Floyd's algorithm
    start_time = time.time()
    res_floyd = floyd(g)
    elapsed_time_floyd = time.time() - start_time
    if len(g) <= 20 and res_floyd:
        printAdjMatrix(res_floyd, width=4)

    # Run Dijkstra's for a single starting vertex, v2
    start_vert = 2
    res_dijkstra_single1 = dijkstraHeap(g, start_vert)
    print(f" dijkstraHeap (for starting vert {start_vert})= : {res_dijkstra_single1}")
    res_dijkstra_single2 = dijkstraArray(g, start_vert)
    print(f" dijkstraArray (for starting vert {start_vert})= : {res_dijkstra_single2}")
    if len(g) <= 20 and res_floyd:
        print(f" floyd's algorithm    (for starting vert {start_vert}): {res_floyd[start_vert]}")
        print(f" dijkstraHeap (for starting vert {start_vert}): {res_dijkstra_single1}")
        print(f" dijkstraArray     (for starting vert {start_vert}): {res_dijkstra_single2}")
    elif res_floyd:
        print(f" adjacency matrix for starting vert {start_vert}      : {g[start_vert][:20]}")
        print(f" floyd's algorithm    (for starting vert {start_vert}): {res_floyd[start_vert][:20]}")
        print(f" dijkstraHeap (for starting vert {start_vert}): {res_dijkstra_single1[:20]}")
        print(f" dijkstraArray     (for starting vert {start_vert}): {res_dijkstra_single2[:20]}")

    # Check that the two produce same results by comparing result from
    # Dijkstra's with the corresponding row from Floyd's output matrix
    assert res_floyd[start_vert] == res_dijkstra_single1
    assert res_floyd[start_vert] == res_dijkstra_single2

    # Run Dijkstra's overall starting points (note this is not the intended way
    # to utilize this algorithm, however we are using it as point of comparion).
    res_dijkstra1 = [[None] * len(g) for i in range(len(g))]
    start_time = time.time()
    for sv in range(len(g)):
        res_dijkstra1[sv] = dijkstraHeap(g, sv)
    elapsed_time_dijkstra1 = time.time() - start_time

    res_dijkstra2 = [[None] * len(g) for i in range(len(g))]
    start_time = time.time()
    for sv in range(len(g)):
        res_dijkstra2[sv] = dijkstraArray(g, sv)
    elapsed_time_dijkstra2 = time.time() - start_time

    # Compare times, Dijkstra's should be slower (for non-trivial sized graphs)
    print(f"  Dijkstra's w/ pri queue elapsed time (for all starts): {elapsed_time_dijkstra1:.2f}")
    print(f"  Dijkstra's w/ array elapsed time (for all starts): {elapsed_time_dijkstra2:.2f}")
    print(f"  Floyd's elapsed time: {elapsed_time_floyd:.2f}")

    # Double check again that the results are all the same
    assert res_floyd == res_dijkstra1
    assert res_floyd == res_dijkstra2
