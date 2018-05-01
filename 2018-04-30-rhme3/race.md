# Race of a lifetime, Misc, 100pts

> You are participating in a race around the world. The prize would be a personalized flag, together with a brand new car. Who wouldn't want that? You are given some locations during this race, and you need to get there as quick as possible. The race organisation is monitoring your movements using the GPS embedded in the car. However, your car is so old and could never win against those used by the opposition. Time to figure out another way to win this race.

A pretty simple challenge, we just have to pretend to be GPS output
and spoof it to make it look as though we are very fast (but not too
fast, to avoid triggering some "asserts"). Final code:

```python
import serial, sys

s = serial.Serial("/dev/ttyUSB0", 115200, timeout = 2)

print s.read_until("\t")
s.write("ak\n")

t = s.read_until(">")
print t
t = t.splitlines()[2].split()

lat = float(t[1])
lng = float(t[3])

airports = [
    (49.0096906, 2.5479245), # Paris
    (31.1443439, 121.808273), # Shanghai
    (37.6213129, -122.3789554), # San Francisco
]

plan = [
    (51.9979819, 4.3855044, "R", "tgt") # Riscure
]
i = 0

speed = {
    "R": 0.3,
    "A": 7,
    "A2": 7.5,
    "R2": 0.9,
}

dt = 1

def length(a, b):
    return (a**2 + b**2) ** 0.5

def demax(dlat, dlng):
    l = length(dlat, dlng)
    if l > dt:
        dlat /= l
        dlng /= l
        dlat *= dt
        dlng *= dt
    return dlat, dlng

tm = 0

while True:
    tm += 1
    print "time", tm
    print "plan: ", plan
    print "GOTO", plan[i]
    dlat, dlng = plan[i][0] - lat, plan[i][1] - lng

    if dt > 6:
        dt = 7 + (2) / (51.99 - 31.14) * (lat - 31.14)
        print "spd", dt

    if abs(dlat) < 0.01 and abs(dlng) < 0.01:
        i += 1
        dt = speed[plan[i][2]]
        dlat, dlng = plan[i][0] - lat, plan[i][1] - lng

    print "delta1", dlat, dlng
    if dlng < -180:
        dlng += 360
    print "delta2", dlat, dlng
    dlat, dlng = demax(dlat, dlng)
    lat += dlat
    lng += dlng
    if lng > 180:
        lng -= 360

    s.write("%.7f %.7f\n" % (lat, lng))
    rd = s.read_until(">")
    print rd
    lines = rd.splitlines()
    for line in lines:
        if "Location:" in line or "Delft" in line:
            if "Kearny" in line:
                tgtlat, tgtlng = 37.7933885, -122.4067155
            elif "Delft" in line:
                tgtlat, tgtlng = (51.9979819, 4.3855044) # Riscure
            else:
                line = line.split()
                tgtlat = float(line[1])
                tgtlng = float(line[2])

            dbest = length(lat - tgtlat, lng - tgtlng) / speed["R"]
            plan = [(tgtlat, tgtlng, "R", "tgt")]

            for a1 in airports:
                for a2 in airports:
                    d1 = length(lat - a1[0], lng - a1[1]) / speed["R"]
                    d2 = length(tgtlat - a2[0], tgtlng - a2[1]) / speed["R"]
                    d3 = length(a1[0] - a2[0], a1[1] - a2[1]) / speed["A"]
                    d = d1 + d2 + d3
                    if d < dbest:
                        dbest = d
                        ch = "A"
                        ch2 = "R"
                        if "Delft" in line:
                            ch = "A2"
                            ch2 = "R2"
                        plan = [(a1[0], a1[1], "R", "air1"),
                                (a2[0], a2[1], ch, "air2"), 
                                (tgtlat, tgtlng, ch2, "tgt")]
            i = 0
            tm = 0
            dt = speed[plan[i][2]]

```