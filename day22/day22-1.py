secret_numbers = []
with open("inputs/day22-data.txt", "r") as fp:
    for line in fp:
        secret_numbers.append(int(line.strip()))

for i in range(len(secret_numbers)):
    secret_number = secret_numbers[i]
    for _ in range(2000):
        secret_number = ((secret_number * 64) ^ secret_number) % 16777216
        secret_number = ((secret_number // 32) ^ secret_number) % 16777216
        secret_number = ((secret_number * 2048) ^ secret_number) % 16777216
    secret_numbers[i] = secret_number

print(sum(secret_numbers))
