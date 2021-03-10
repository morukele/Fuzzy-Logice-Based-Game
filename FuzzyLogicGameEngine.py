# This program is for the implementation of the fuzzy logic engine
# The program ask the user for input of the health and ammo values
# and selection of the mode: Attacking, Defensive or Normal mode
# The outputs are the defuzzified value for the action and plots


import numpy as np
import matplotlib.pyplot as plt

# Generating the universe variables
#   *Ammo and Health on a range of [0, 100] => input
#   *Action has a range of [0, 100] => output 

# Generates points from 1 to 100 with intervals of .1

x_ammo = np.linspace(0, 100, 1000)
x_health = np.linspace(0, 100, 1000)
x_action = np.linspace(0, 100, 1000)


# Generating the fuzzy membership functions

# A method that created a triangle membership function
def triangleMembershipFunction(x, a, b, c):
    # This function takes in an array of x points and 
    # a vector containing a, b and c
    # where a=> left side, b = center, c = right side

    y = np.zeros(len(x))  # shape of the output array

    # Setting the areas outside of our interest to zero
    y[x <= a] = 0
    y[x >= c] = 0

    # Setting the center to 1
    y[x == b] = 1

    # Determine the index of the left side and right side
    left_side = np.logical_and(a < x, x <= b)
    right_side = np.logical_and(b < x, x < c)

    # Replacing those values with the appropriate values using interpolation
    y[left_side] = (x[left_side] - a) / (b - a)
    y[right_side] = (x[right_side] - c) / (b - c)

    return y


# Regular Fuzzy Logic Domain
# Creating triangle fuzzy membership functions for the ammo set
ammo_vlo = triangleMembershipFunction(x_ammo, 0, 0, 25)  # very low ammo
ammo_lo = triangleMembershipFunction(x_ammo, 0, 25, 50)  # low ammo
ammo_md = triangleMembershipFunction(x_ammo, 25, 50, 75)  # medium ammo
ammo_hi = triangleMembershipFunction(x_ammo, 50, 75, 100)  # high ammo
ammo_vhi = triangleMembershipFunction(x_ammo, 75, 100, 100)  # very high ammo

# Creating triangle fuzzy membership functions for the health set
health_vlo = triangleMembershipFunction(x_health, 0, 0, 25)  # very low health
health_lo = triangleMembershipFunction(x_health, 0, 25, 50)  # low health
health_md = triangleMembershipFunction(x_health, 25, 50, 75)  # medium health
health_hi = triangleMembershipFunction(x_health, 50, 75, 100)  # high health
health_vhi = triangleMembershipFunction(x_health, 75, 100, 100)  # very high health

# Creating triangle fuzzy membership functions for the action set
hide = triangleMembershipFunction(x_action, 0, 0, 25)
run = triangleMembershipFunction(x_action, 0, 25, 50)
stop = triangleMembershipFunction(x_action, 25, 50, 75)
walk = triangleMembershipFunction(x_action, 50, 75, 100)
attack = triangleMembershipFunction(x_action, 75, 100, 100)

# Visualizing the memberships

# Plotting ammo
fig = plt.figure()
plt.plot(x_ammo, ammo_vlo, 'b', label='very low')
plt.plot(x_ammo, ammo_lo, 'g', label='low')
plt.plot(x_ammo, ammo_md, 'r', label='medium')
plt.plot(x_ammo, ammo_hi, 'c', label='high')
plt.plot(x_ammo, ammo_vhi, 'm', label='high')
plt.title("Input: Ammo Fuzzy Universe")
plt.legend()
plt.grid(True)

# Plotting health
fig = plt.figure()
plt.plot(x_health, health_vlo, 'b', label='very low')
plt.plot(x_health, health_lo, 'g', label='low')
plt.plot(x_health, health_md, 'r', label='medium')
plt.plot(x_health, health_hi, 'c', label='high')
plt.plot(x_health, health_vhi, 'm', label='high')
plt.title("Input: Health Fuzzy Universe")
plt.legend()
plt.grid(True)

# Plotting Actions
fig = plt.figure()
plt.plot(x_action, hide, 'b', label='hide')
plt.plot(x_action, run, 'g', label='run away')
plt.plot(x_action, stop, 'r', label='stop')
plt.plot(x_action, walk, 'c', label='walk around')
plt.plot(x_action, attack, 'm', label='attack')
plt.title("Output: Action Fuzzy Universe")
plt.legend()
plt.grid(True)


plt.tight_layout()

# Degree of membership of each fuzzy set

# Input values used for the fuzzy engine:
health = input("Enter a value for health: ")
ammo = input("Enter a value for ammo: ")
mode = int(input("Select the mode => 1. Attack Mode, 2. Defence Mode, 3. Normal Mode: "))

print('Health :', health)
print('Ammo :', ammo)

# Selecting the Mode for the computation in other to assign the desired weight value
defenseWeight = []
attackWeight = []

# Setting the mode of the fuzzy engine
if mode == 1: 
    defenseWeight = 1
    attackWeight = 1.5
    print("Attack Mode Selected")
elif mode == 2: 
    defenseWeight = 1.5
    attackWeight = 1
    print("Defence Mode Selected")
elif mode == 3:
    defenseWeight = 1
    attackWeight = 1
    print("Normal Mode Selected")
else:
    # Fail safe for a situation when wrong option is selected
    print("Select a value from the specified options")
    exit()

print(" ")


# Finding the degree of membership for a particular input

# A function that interpolates thought a fuzzy data to give the degree of membership
def Interpolate(x, y, value):
    # This function takes in:
    # x => a 1d array of x-axis coordinates
    # y => a 1d array of y-axis coordinates
    # value => the exact value we desire the interpolation for 

    y = np.interp(value, x, y)

    return y


# Degree of memberships for ammo
ammo_level_vlo = Interpolate(x_ammo, ammo_vlo, ammo)
ammo_level_lo = Interpolate(x_ammo, ammo_lo, ammo)
ammo_level_md = Interpolate(x_ammo, ammo_md, ammo)
ammo_level_hi = Interpolate(x_ammo, ammo_hi, ammo)
ammo_level_vhi = Interpolate(x_ammo, ammo_vhi, ammo)
print('The degree of memberships of the Ammo input for Very Low, Low, Mid, High & Very High are: ')
print(ammo_level_vlo, ", ", ammo_level_lo, ", ", ammo_level_md, ", ", ammo_level_hi, ", ", ammo_level_vhi)
print(" ")

# Degree of memberships for health
health_level_vlo = Interpolate(x_health, health_vlo, health)
health_level_lo = Interpolate(x_health, health_lo, health)
health_level_md = Interpolate(x_health, health_md, health)
health_level_hi = Interpolate(x_health, health_hi, health)
health_level_vhi = Interpolate(x_health, health_vhi, health)
print('The degree of memberships of the Health input for Very Low, Low, Mid, High & Very High are: ')
print(health_level_vlo, ", ", health_level_lo, ", ", health_level_md, ", ", health_level_hi, ", ", health_level_vhi)
print(" ")

# Creating the fuzzy rules and applying them
# Recall that the rules in the article use AND, so we use the MIN operator
# There are 25 rules according to the article

rule1 = np.fmin(ammo_level_vlo, health_level_vlo) * defenseWeight  # ammo very low and health very low => hide
rule2 = np.fmin(ammo_level_vlo, health_level_lo) * defenseWeight  # ammo very low and health low => hide
rule3 = np.fmin(ammo_level_vlo, health_level_md) * defenseWeight  # ammo very low and health mid => run away
rule4 = np.fmin(ammo_level_vlo, health_level_hi) * defenseWeight  # ammo very low and health high => run away
rule5 = np.fmin(ammo_level_vlo, health_level_vhi)  # ammo very low and health very high => stop

rule6 = np.fmin(ammo_level_lo, health_level_vlo) * defenseWeight  # ammo low and health very low => hide
rule7 = np.fmin(ammo_level_lo, health_level_lo) * defenseWeight  # ammo low and health low => run away
rule8 = np.fmin(ammo_level_lo, health_level_md) * defenseWeight  # ammo low and health mid => run away
rule9 = np.fmin(ammo_level_lo, health_level_hi)  # ammo low and health high => stop
rule10 = np.fmin(ammo_level_lo, health_level_vhi) * attackWeight  # ammo low and health very high => walk around

rule11 = np.fmin(ammo_level_md, health_level_vlo) * defenseWeight  # ammo mid and health very low  => run away
rule12 = np.fmin(ammo_level_md, health_level_lo) * defenseWeight  # ammo mid and health low => run away
rule13 = np.fmin(ammo_level_md, health_level_md)  # ammo mid and health mid => stop
rule14 = np.fmin(ammo_level_md, health_level_hi) * attackWeight  # ammo mid and health high => walk around
rule15 = np.fmin(ammo_level_md, health_level_vhi) * attackWeight  # ammo mid and health very high => walk around

rule16 = np.fmin(ammo_level_hi, health_level_vlo) * defenseWeight  # ammo high and health very low  => run away
rule17 = np.fmin(ammo_level_hi, health_level_lo)  # ammo high and health low => stop
rule18 = np.fmin(ammo_level_hi, health_level_md) * attackWeight  # ammo high and health mid => walk around
rule19 = np.fmin(ammo_level_hi, health_level_hi) * attackWeight  # ammo high and health high => walk around
rule20 = np.fmin(ammo_level_hi, health_level_vhi) * attackWeight  # ammo high and health very high => attack

rule21 = np.fmin(ammo_level_vhi, health_level_vlo)  # ammo very high and health very low => stop
rule22 = np.fmin(ammo_level_vhi, health_level_lo) * attackWeight  # ammo very high and health low => walk around
rule23 = np.fmin(ammo_level_vhi, health_level_md) * attackWeight  # ammo very high and health mid => walk around
rule24 = np.fmin(ammo_level_vhi, health_level_hi) * attackWeight  # ammo very high and health high => attack
rule25 = np.fmin(ammo_level_vhi, health_level_vhi) * attackWeight  # ammo very high and health very high => attack

# finding the area under the action curves triggered by the rules (This is need for plotting the output)
# i.e. the area under the action curve is all value lower than the interested points on the curve
# in other words cutting the curve at the desired points
rule1_area = np.fmin(hide, rule1)  # hide zone
rule2_area = np.fmin(hide, rule2)  # hide zone
rule3_area = np.fmin(run, rule3)  # run away zone
rule4_area = np.fmin(run, rule4)  # run zone
rule5_area = np.fmin(stop, rule5)  # stop zone

rule6_area = np.fmin(hide, rule6)  # hide zone
rule7_area = np.fmin(run, rule7)  # run away zone
rule8_area = np.fmin(run, rule8)  # run away zone
rule9_area = np.fmin(stop, rule9)  # stop zone
rule10_area = np.fmin(walk, rule10)  # walk around zone

rule11_area = np.fmin(run, rule11)  # run away zone
rule12_area = np.fmin(run, rule12)  # run away zone
rule13_area = np.fmin(stop, rule13)  # stop zone
rule14_area = np.fmin(walk, rule14)  # walk around zone
rule15_area = np.fmin(walk, rule15)  # walk around zone

rule16_area = np.fmin(run, rule16)  # run away zone
rule17_area = np.fmin(stop, rule17)  # stop zone
rule18_area = np.fmin(walk, rule18)  # walk around zone
rule19_area = np.fmin(walk, rule19)  # walk around zone
rule20_area = np.fmin(attack, rule20)  # attack zone

rule21_area = np.fmin(stop, rule21)  # stop zone
rule22_area = np.fmin(walk, rule22)  # walk around zone
rule23_area = np.fmin(walk, rule23)  # walk around zone
rule24_area = np.fmin(attack, rule24)  # attack zone
rule25_area = np.fmin(attack, rule25)  # attack zone

# Visualizing the output of the rules

action0 = np.zeros_like(x_action)  # This is needed for plotting the shaded area

_, ax0 = plt.subplots(nrows=1, figsize=(9, 4))

# Here is for plotting the original output domains 
ax0.plot(x_action, hide, 'b', label='hide', linestyle='--', alpha=0.5)
ax0.plot(x_action, run, 'g', label='run away', linestyle='--', alpha=0.5)
ax0.plot(x_action, stop, 'r', label='stop', linestyle='--', alpha=0.5)
ax0.plot(x_action, walk, 'c', label='walk around', linestyle='--', alpha=0.5)
ax0.plot(x_action, attack, 'm', label='attack', linestyle='--', alpha=0.5)
ax0.legend()
ax0.set_title('Output membership')
ax0.grid(True)

# Here is for plotting the rule activated areas in the action function
ax0.fill_between(x_action, action0, rule1_area, facecolor='b', alpha=0.7)
ax0.fill_between(x_action, action0, rule2_area, facecolor='g', alpha=0.7)
ax0.fill_between(x_action, action0, rule3_area, facecolor='r', alpha=0.7)
ax0.fill_between(x_action, action0, rule4_area, facecolor='b', alpha=0.7)
ax0.fill_between(x_action, action0, rule5_area, facecolor='g', alpha=0.7)

ax0.fill_between(x_action, action0, rule6_area, facecolor='r', alpha=0.7)
ax0.fill_between(x_action, action0, rule7_area, facecolor='b', alpha=0.7)
ax0.fill_between(x_action, action0, rule8_area, facecolor='g', alpha=0.7)
ax0.fill_between(x_action, action0, rule9_area, facecolor='r', alpha=0.7)
ax0.fill_between(x_action, action0, rule10_area, facecolor='g', alpha=0.7)

ax0.fill_between(x_action, action0, rule11_area, facecolor='g', alpha=0.7)
ax0.fill_between(x_action, action0, rule12_area, facecolor='r', alpha=0.7)
ax0.fill_between(x_action, action0, rule13_area, facecolor='b', alpha=0.7)
ax0.fill_between(x_action, action0, rule14_area, facecolor='g', alpha=0.7)
ax0.fill_between(x_action, action0, rule15_area, facecolor='r', alpha=0.7)

ax0.fill_between(x_action, action0, rule16_area, facecolor='b', alpha=0.7)
ax0.fill_between(x_action, action0, rule17_area, facecolor='g', alpha=0.7)
ax0.fill_between(x_action, action0, rule18_area, facecolor='r', alpha=0.7)
ax0.fill_between(x_action, action0, rule19_area, facecolor='b', alpha=0.7)
ax0.fill_between(x_action, action0, rule20_area, facecolor='g', alpha=0.7)

ax0.fill_between(x_action, action0, rule21_area, facecolor='r', alpha=0.7)
ax0.fill_between(x_action, action0, rule22_area, facecolor='b', alpha=0.7)
ax0.fill_between(x_action, action0, rule23_area, facecolor='g', alpha=0.7)
ax0.fill_between(x_action, action0, rule24_area, facecolor='r', alpha=0.7)
ax0.fill_between(x_action, action0, rule25_area, facecolor='b', alpha=0.7)


# Defuzzification

# Center of Gravity Function 
def Centroid(x, aggregate):
    # This function takes in the x-axis of the curve and the aggregated area of the 
    # fuzzy set and returns the centroid position

    centroid = np.sum(x * aggregate) / np.sum(aggregate)

    return centroid


# Mean of Maximum Function
def MeanOfMax(x, a):
    # This function takes in a 1-D array a => aggregate of the fuzzy logic
    # another 1-D array x=> the x-axis
    # Returns the mean of the maximum value(s) of the aggregate array

    idx = np.argwhere(a == np.max(a))  # Finding the index of all max values on the y-axis

    res = np.mean(x[idx])  # computing the mean of the max values on the x-axis

    return res


# Max Aggregated output
#   Aggregate all the output of the 25 rules together i.e the area under the curve
max_aggregated_output = np.fmax(rule1_area, np.fmax(rule2_area, np.fmax(rule3_area, np.fmax(rule4_area, np.fmax(rule5_area,
                                np.fmax(rule6_area, np.fmax(rule7_area, np.fmax(rule8_area, np.fmax(rule9_area, np.fmax(rule10_area,
                                np.fmax(rule11_area, np.fmax(rule12_area, np.fmax(rule13_area, np.fmax(rule14_area, np.fmax(rule15_area,
                                np.fmax(rule16_area, np.fmax(rule17_area, np.fmax(rule18_area, np.fmax(rule19_area, np.fmax(rule20_area,
                                np.fmax(rule21_area, np.fmax(rule22_area, np.fmax(rule23_area, np.fmax(rule24_area, rule25_area))))))))))))))))))))))))

# Sum Aggregated output
sum_aggregated_output = (rule1_area + rule2_area + rule3_area + rule4_area + rule5_area +
                         rule6_area + rule7_area + rule8_area + rule9_area + rule10_area +
                         rule11_area + rule12_area + rule13_area + rule14_area + rule15_area +
                         rule16_area + rule17_area + rule18_area + rule19_area + rule20_area +
                         rule21_area + rule22_area + rule23_area + rule24_area + rule25_area)

# Max aggregated output and Centroid Defuzzification
max_centroid = Centroid(x_action, max_aggregated_output)
max_centroid_line = Interpolate(x_action, max_aggregated_output, max_centroid)  # for the plot
print("The crisp output value for Max aggregation and centroid defuzz is:", max_centroid)

# Sum Aggregated output and Centroid Defuzzification
sum_centroid = Centroid(x_action, sum_aggregated_output)
sum_centroid_line = Interpolate(x_action, sum_aggregated_output, sum_centroid)  # for the plot
print("The crisp output value for Sum aggregation and centroid defuzz is:", sum_centroid)

# Max Aggregated output and Mean of Maximum (MOM) Defuzzification
max_MOM = MeanOfMax(x_action, max_aggregated_output)
max_MOM_line = Interpolate(x_action, max_aggregated_output, max_MOM)  # for the plot
print("The crisp output value for Max aggregation and Mean of Max defuzz: ", max_MOM)

# Sum Aggregated output and Mean of Maximum (MOM) Defuzzification
sum_MOM = MeanOfMax(x_action, sum_aggregated_output)
sum_MOM_line = Interpolate(x_action, sum_aggregated_output, sum_MOM)  # for the plot
print("The crisp output value for Sum aggregation and Mean of Max defuzz: ", sum_MOM)

# Plotting the max aggregated area
_, ax0 = plt.subplots(figsize=(9, 4))
ax0.plot(x_action, hide, 'b', label='hide', linestyle='--', alpha=0.5)
ax0.plot(x_action, run, 'g', label='run away', linestyle='--', alpha=0.5)
ax0.plot(x_action, stop, 'r', label='stop', linestyle='--', alpha=0.5)
ax0.plot(x_action, walk, 'c', label='walk around', linestyle='--', alpha=0.5)
ax0.plot(x_action, attack, 'm', label='attack', linestyle='--', alpha=0.5)
ax0.fill_between(x_action, action0, max_aggregated_output, facecolor='b', alpha=0.5)  # plot for area under curve
ax0.plot([max_centroid, max_centroid], [0, max_centroid_line], 'k', linewidth=1.5, alpha=0.9, label='Max & Centroid')
ax0.plot([max_MOM, max_MOM], [0, max_MOM_line], 'r', linewidth=1.5, alpha=0.9, label='Max & Mean of Maximum')
ax0.legend()
ax0.set_title('Action Output: Max Aggregator')
ax0.grid(True)

# Plotting the sum aggregated area
_, ax0 = plt.subplots(figsize=(9, 4))
ax0.plot(x_action, hide, 'b', label='hide', linestyle='--', alpha=0.5)
ax0.plot(x_action, run, 'g', label='run away', linestyle='--', alpha=0.5)
ax0.plot(x_action, stop, 'r', label='stop', linestyle='--', alpha=0.5)
ax0.plot(x_action, walk, 'c', label='walk around', linestyle='--', alpha=0.5)
ax0.plot(x_action, attack, 'm', label='attack', linestyle='--', alpha=0.5)
ax0.fill_between(x_action, action0, sum_aggregated_output, facecolor='b', alpha=0.5)  # plot for area under curve
ax0.plot([sum_centroid, sum_centroid], [0, sum_centroid_line], 'k', linewidth=1.5, alpha=0.9, label='Sum & Centroid')
ax0.plot([sum_MOM, sum_MOM], [0, sum_MOM_line], 'r', linewidth=1.5, alpha=0.9, label='Sum & Mean Of Maximum')
ax0.legend()
ax0.set_title('Action Output: Sum Aggregator')
ax0.grid(True)

plt.show()
