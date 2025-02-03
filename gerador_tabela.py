import csv, os

reader = csv.reader(open('estoque.csv', 'r', encoding="utf-8")) 
data = []

for row in reader: 
  data.append(row) 
  
header = data.pop(0) 

def fixed_length (text, length): 
  if len (text) > length: 
    text = text[:length] 
  elif len (text) < length: 
    text = (text + " " * length)[:length] 
  return text 

def draw_table (data):
  os.system('cls') 
  print("-"*106) 
  print("#", end=" ")
  counter = 0
  for column in header:
    if counter == 0:
      print(fixed_length(column, 7), end =" #   ")
    elif counter == 1:
      print(fixed_length(column, 40), end =" #   ")
    else:
      print(fixed_length(column, 20), end =" #   ")
    counter = counter + 1 
  print("")
  print("-"*106)
  
  for row in data:
    print("# ", end="")
    counter = 0
    for column in row:
      if counter == 0:
        print(fixed_length(column, 7), end =" #   ")
      elif counter == 1:
        print(fixed_length(column, 40), end =" #   ")
      else:
        print(fixed_length(column, 20), end =" #   ")
      counter = counter + 1
    print()
  print("-"*106)

draw_table(data)
