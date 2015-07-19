def load_data(fname):
    f = open(fname,'r')
    scanned = []
    for line in f:
        elements = line.strip().split(',')
        (t, beacon_id, rssi, dist) = (int(elements[0]), int(elements[1]), float(elements[2]), float(elements[3]))
        scanned.append((t, beacon_id, rssi, dist))
    return scanned
def trilaterate(dist,beacon):  #x1 = 0 x2 =  1 x3 =  0 y1 = 0 y2 = 0 y3 = 1 
      A = beacon[0][0]**2 + beacon[0][1]**2 - dist[0]**2    
      B = beacon[1][0]**2 + beacon[1][1]**2 - dist[1]**2
      C = beacon[2][0]**2 + beacon[2][1]**2 - dist[2]**2
      X32 = beacon[2][0] - beacon[1][0]
      X13 = beacon[0][0] - beacon[2][0]
      X21 = beacon[1][0] - beacon[0][0]
      Y32 = beacon[2][1] - beacon[1][1]
      Y13 = beacon[0][1] - beacon[2][1]
      Y21 = beacon[1][1] - beacon[0][1]
      
      X = (A*Y32 + B*Y13 + C*Y21)/((beacon[0][0]*Y32 + beacon[1][0]*Y13 + beacon[2][0]*Y21)*2)
      Y = (A*X32 + B*X13 + C*X21)/((beacon[0][1]*X32 + beacon[1][1]*X13 + beacon[2][1]*X21)*2)
      return (X,Y)
      
def dist_rssi(rssi, ref):
    par = [0.42093, 6.9476, 0.54992]
    return par[0]*((rssi/ref)**par[1])+par[2]
    
def dist_beacon(rssi, beacon_id):
    ref_rssi = [-56, -58, -58]
    return dist_rssi(rssi, ref_rssi[beacon_id - 1])

def get_positions(fname):
    data = load_data(fname)
    last_distance = [0, 0, 0]
    beacon_pos = [(0, 0), (5, 0), (0, 4)]
    positions = []
    for d in data:
        (t, beacon_id, rssi, _) = d
        newdist = dist_beacon(rssi, beacon_id)
        if newdist < 5:
            last_distance[beacon_id - 1] =  newdist
        #print(last_distance)
        pos = trilaterate (last_distance, beacon_pos)
        positions.append(pos)
    return positions
    
#%matplotlib inline
from matplotlib import pyplot as plt
pos = get_positions('log3.txt')
x = [p[0] for p in pos]
y = [p[1] for p in pos]
plt.plot(x, y)
plt.show()

#sample comment

p = load_data('log3.txt')
for i in range(3):
    plt.plot([dist_beacon(d[2], d[1]) for d in p if i+1 == d[1]])
plt.show()
