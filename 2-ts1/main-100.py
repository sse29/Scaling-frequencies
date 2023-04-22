import math
logfile = open('../Corrections/2-ts1-brdg-mk-MN15-THF.log', 'r')
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

vibrationalValues = ""

for i in vibrational1:
    vibrationalValues += i


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
EV = EV*R*0.001


GV = EV-temperature*SV


print("SV: ", SV)
print("EV: ", EV)
print("GV: ", GV)

deltaGold = 12.6 * 1000

logfile = open('common/values100.txt', 'r')
dataChanged100 = logfile.readlines()
logfile.close()

SVibReactant100=float(dataChanged100[0][:-1])
EVibReactant100=float(dataChanged100[1][:-1])

deltaSv100 = SV - SVibReactant100
deltaEv100 = EV*1000 - EVibReactant100*1000

deltaGv100 = deltaEv100 - temperature * deltaSv100

logfile = open('common/values.txt', 'r')
data = logfile.readlines()
logfile.close()

SVibReactant=float(data[0][:-1])
EVibReactant=float(data[1][:-1])

deltaSv = SV - SVibReactant
deltaEv = EV*1000 - EVibReactant*1000

deltaGv = deltaEv - temperature * deltaSv

deltaE = 5.7 * 1000

newDeltaG50 = deltaGold + deltaGv100 - deltaGv + deltaE - 1.98

print("New Delta G reaction:",newDeltaG50/1000, "Kcal / mol")
