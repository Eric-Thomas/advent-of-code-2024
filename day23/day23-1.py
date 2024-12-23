from collections import defaultdict
from copy import copy

with open("inputs/day23-data.txt", "r") as fp:
    connections = [line.strip() for line in fp]

adj_list = defaultdict(list)

for connection in connections:
    u, v = connection.split("-")
    adj_list[u].append(v)
    adj_list[v].append(u)


fully_connected_components_of_lenght_3 = set()
for node in adj_list:
    graph = set([node])
    for neighbor in adj_list[node]:
        if neighbor not in graph:
            graph.add(neighbor)
            for next_neighbor in adj_list[neighbor]:
                if next_neighbor not in graph and next_neighbor in adj_list[node]:
                    graph.add(next_neighbor)
                if len(graph) == 3:
                    fully_connected_components_of_lenght_3.add(copy(tuple(sorted(graph))))
                    graph.remove(next_neighbor)
            graph.remove(neighbor)

components_of_3_with_1_that_starts_with_t = 0
for fully_connected_component in fully_connected_components_of_lenght_3:
    for computer in fully_connected_component:
        if computer.startswith("t"):
            components_of_3_with_1_that_starts_with_t += 1
            break

print(components_of_3_with_1_that_starts_with_t)
