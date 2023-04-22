import math
logfile = open('1-plx-MN15-THF[6819].log', 'r')
data = logfile.readlines()
logfile.close()

frequencies = []
for i in data:
    if "Frequencies" in i:
        line = (i.split())
        for j in range(len(line)):
            try:
                freq = float(line[j])
                if freq < 50:
                    freq = 50
                frequencies.append(freq)
            except:
                pass

# print(len(frequencies))
temperature = 298.15
K = 1.3806488*(10**(-23))
R = 1.9872


# print(math.log(math.e))
# print(17*5)

starts = []
ends = []
for i in range(len(data)):
    if data[i].startswith(" Vibrational temperatures:"):
        starts.append(i)
    elif data[i].startswith(" Zero-point correction="):
        ends.append(i)
vibrational1 = (data[starts[0]:ends[0]])
vibrational2 = (data[starts[1]:ends[1]])

vibrationalValues = ""

# for i in vibrational1:
#     vibrationalValues += i
for i in vibrational2:
    vibrationalValues += i


vibrationalValues = (vibrationalValues.split())


vibrationals = []
for i in vibrationalValues:
    try:
        freq = float(i)
        vibrationals.append(freq)
    except:
        pass
# print(len(vibrationals))

SV = 0
for i in vibrationals:
    value = i / temperature
    exp = math.exp(value)-1
    part1 = value/exp
    part2 = math.log(1-math.exp(-value))
    SV += part1 - part2

SV = SV * R


EV = 0
for i in vibrationals:
    EV += i * (0.5 + 1/(math.exp(i/temperature) - 1))
EV = EV*R * 0.001


GV = EV-temperature*SV


print("SV: ", SV)
print("EV: ", EV)
print("GV: ", GV)