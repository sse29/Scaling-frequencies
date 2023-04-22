import math

# Read the log file and return the lines as a list
def read_logfile(filename):
    with open(filename, 'r') as logfile:
        data = logfile.readlines()
    return data

# Extract frequencies from the log file data
def extract_frequencies(data):
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
    return frequencies

# Extract vibrational values from the log file data
def extract_vibrational_values(data):
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
    return vibrationals

# Calculate the entropy of vibrational modes (SV)
def calculate_sv(vibrationals, temperature):
    R = 1.9872
    SV = 0
    for i in vibrationals:
        value = i / temperature
        exp = math.exp(value)-1
        part1 = value/exp
        part2 = math.log(1-math.exp(-value))
        SV += part1 - part2
    return SV * R

# Calculate the vibrational energy (EV)
def calculate_ev(vibrationals, temperature):
    R = 1.9872
    EV = 0
    for i in vibrationals:
        EV += i * (0.5 + 1/(math.exp(i/temperature) - 1))
    return EV * R * 0.001

# Calculate the Gibbs free energy of vibrational modes (GV)
def calculate_gv(EV, SV, temperature):
    return EV - temperature * SV

def main():
    filename = '1-plx-MN15-THF[6819].log'
    temperature = 298.15
    K = 1.3806488*(10**(-23))

    # Read the log file
    data = read_logfile(filename)
    
    # Extract frequencies and vibrational values
    frequencies = extract_frequencies(data)
    vibrationals = extract_vibrational_values(data)

    # Calculate SV, EV, and GV
    SV = calculate_sv(vibrationals, temperature)
    EV = calculate_ev(vibrationals, temperature)
    GV = calculate_gv(EV, SV, temperature)

    # Calculate other thermodynamic properties
    ET = ER = 0.889
    Etot = EV + ET + ER
    Hcorr = Etot + K * temperature

    ST = 44.344
    SR = 34.494
    Stot = SV + ST + SR
    Gcorr = Hcorr - temperature * Stot

    # Print the results
    print(f"SV: {SV}")
    print(f"EV: {EV}")
    print(f"GV: {GV}")
    print(Etot)
    print(Hcorr / 627.5095)
    print((Gcorr / 1000) * 4.184 * 4.35974434 * 10** (-18))

main()