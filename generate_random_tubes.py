import sys,math,random,Config

x = y = 0
def gen_forest():
  distance_between = 16
  number_of_tubes = 10000
  per_row = int(math.sqrt(number_of_tubes))
  global x, y
  forest = []
#  x = y = 0
  for i in range(0,number_of_tubes):
    tube_size = random.randint(0,1000)
    x += 1
    if(x % per_row == 0):
      x = 0
      y += 1 

    zlist = []
    for i in range(0,tube_size/10):
      zlist.append(random.randint(0,tube_size))   
    zlist = sorted(zlist)
  
    tube = []
    for z in zlist:
      tube.append((x*distance_between,y*distance_between,z))

    forest.append(tube)
  
  return forest

forest = gen_forest()
Config.write(forest, 'straight_forest.json')

print "Generated a forest with " + str(len(forest)) + " tubes"
print "They are distributed on the xy plane with approximately " + str(y) + " rows square"

