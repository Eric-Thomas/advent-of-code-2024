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


def get_prerequisite_pages(row, page, pre_requisites=None):
    if pre_requisites is None:
        pre_requisites = []
    for pre_requisite in adj_list[page]:
        if pre_requisite in row and pre_requisite not in pre_requisites:
            pre_requisites += get_prerequisite_pages(row, pre_requisite, pre_requisites)
            pre_requisites.append(pre_requisite)

    return pre_requisites


def fix_row_order(row):
    fixed_row = []
    for page in row:
        for pre_requisite in get_prerequisite_pages(row, page):
            if pre_requisite not in fixed_row:
                fixed_row.append(pre_requisite)

        if page not in row:
            fixed_row.append(page)

    return fixed_row


fixed_invalid_middle_page_sum = 0
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
    if not valid:
        row = fix_row_order(row)
        fixed_invalid_middle_page_sum += int(row[len(row) // 2])

print(fixed_invalid_middle_page_sum)
