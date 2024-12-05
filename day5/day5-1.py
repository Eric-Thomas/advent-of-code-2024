from collections import defaultdict

rules = []
page_numbers = []
parsing_rules = True
with open("inputs/day5-data.txt", "r") as fp:
    for line in fp:
        # Empty line marks switch from rules to page numbers
        if len(line.strip()) == 0:
            parsing_rules = False
        elif parsing_rules:
            rules.append(line.strip().split("|"))
        else:
            page_numbers.append(line.strip().split(","))


# Adjacency list that maps nodes to thier prerequisites
adj_list = defaultdict(list)
for u, v in rules:
    adj_list[v].append(u)

valid_middle_page_sum = 0
for row in page_numbers:
    valid = True
    printed_pages = set()
    for page_number in row:
        for pre_requisite in adj_list[page_number]:
            if pre_requisite not in printed_pages and pre_requisite in row:
                valid = False
                break
        if valid:
            printed_pages.add(page_number)
        else:
            break
    if valid:
        valid_middle_page_sum += int(row[len(row) // 2])

print(valid_middle_page_sum)
