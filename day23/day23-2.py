from collections import defaultdict, deque

with open("inputs/day23-data.txt", "r") as fp:
    connections = [line.strip() for line in fp]

adj_list = defaultdict(list)

for connection in connections:
    u, v = connection.split("-")
    adj_list[u].append(v)
    adj_list[v].append(u)


def bfs(node):
    visited = set([node])
    queue = deque([node])
    while len(queue) > 0:
        node = queue.popleft()
        for neighbor in adj_list[node]:
            if neighbor not in visited:
                fully_connected = True
                for visited_node in visited:
                    if neighbor not in adj_list[visited_node]:
                        fully_connected = False
                if fully_connected:
                    visited.add(neighbor)
                    queue.append(neighbor)
    return visited


visted = set()
max_computers = float("-inf")
computers_in_max = None
for node in adj_list:
    if node not in visted:
        current_set = bfs(node)
        visted.union(current_set)
        if len(current_set) > max_computers:
            max_computers = len(current_set)
            computers_in_max = current_set

print(",".join(sorted(computers_in_max)))
