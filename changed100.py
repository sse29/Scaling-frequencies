import math
logfile = open('1-plx-MN15-THF[6819].log', 'r')
data = logfile.readlines()
logfile.close()

temperature = 298.15
K = 1.3806488*(10**(-23))
R = 1.9872
h = 6.62606957*(10**(-34))

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

for i in vibrational1:
    vibrationalValues += i
# for i in vibrational2:
#     vibrationalValues += i

vibrationalValues = (vibrationalValues.split())

vibrationals = []
for i in vibrationalValues:
    try:
        freq = float(i)
        vibrationals.append(freq)
    except:
        pass


frequencies = []
index = 0
for i in data:
    if "Frequencies" in i:
        line = (i.split())
        for j in range(len(line)):
            try:
                freq = float(line[j])
                if freq < 100:
                    freq = 100
                    vibrationals[index] = h * (freq * 29979245800) / K
                frequencies.append(freq)
                index += 1
            except:
                pass

SV = 0
for i in vibrationals[:len(vibrationals)//2]:
    value = i / temperature
    exp = math.exp(value)-1
    part1 = value/exp
    part2 = math.log(1-math.exp(-value))
    SV += part1 - part2

SV = SV * R


EV = 0
for i in vibrationals[:len(vibrationals)//2]:
    EV += i * (0.5 + 1/(math.exp(i/temperature) - 1))
EV = EV*R


GV = EV-temperature*SV


print("SV: ", SV)
print("EV: ", EV*0.001)
print("GV: ", GV)