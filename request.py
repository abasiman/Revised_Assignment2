import random


num_requests = 1000
max_cylinder = 4999


requests = [random.randint(0, max_cylinder) for _ in range(num_requests)]


with open("requests.txt", "w") as file:
    for request in requests:
        file.write(f"{request}\n")

print("requests.txt file created with 1,000 random requests.")
