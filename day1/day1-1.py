with open("inputs/day1-data.txt", "r") as fp:
    list_1, list_2 = [], []
    for line in fp:
        distance1, distance2 = line.split()
        list_1.append(int(distance1))
        list_2.append(int(distance2))

list_1.sort()
list_2.sort()

distance_difference = 0

for i in range(len(list_1)):
    distance_difference += abs(list_1[i] - list_2[i])

print(f"Distance difference - {distance_difference}")
