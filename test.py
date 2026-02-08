value = 16
answer = 0

for i in range(value + 1):
  if i * i == value:
    answer = i
    break
  elif i * i > value:
    answer = i - 1
    break