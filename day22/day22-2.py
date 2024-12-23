from collections import defaultdict, deque

secret_numbers = []
with open("inputs/day22-data.txt", "r") as fp:
    for line in fp:
        secret_numbers.append(int(line.strip()))

secret_number_prices = []
for i in range(len(secret_numbers)):
    secret_number = secret_numbers[i]
    current_prices = []
    for _ in range(2000):
        secret_number = ((secret_number * 64) ^ secret_number) % 16777216
        secret_number = ((secret_number // 32) ^ secret_number) % 16777216
        secret_number = ((secret_number * 2048) ^ secret_number) % 16777216
        current_prices.append(secret_number % 10)
    secret_number_prices.append(current_prices)

changes_to_banans = defaultdict(int)
for prices in secret_number_prices:
    prev_price = prices[0]
    changes = deque([])
    changes_in_current_prices = set()
    for i in range(1, len(prices)):
        changes.append(prices[i] - prev_price)
        if len(changes) > 4:
            changes.popleft()

        if len(changes) == 4 and tuple(changes) not in changes_in_current_prices:
            changes_to_banans[tuple(changes)] += prices[i]
            changes_in_current_prices.add(tuple(changes))

        prev_price = prices[i]

print(max(changes_to_banans.values()))
