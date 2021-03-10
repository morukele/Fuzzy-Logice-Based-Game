# This code is optimized for just the 3D plot of the evolution of
# The defuzzified output based on the input parameters

import numpy as np
import matplotlib.pyplot as plt


# A function that creates a triangle membership function
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


# A function that interpolates the fuzzy data to give the degree of membership
def Interpolate(x, y, value):
    # This function takes in:
    # x => a 1d array of x-axis coordinates
    # y => a 1d array of y-axis coordinates
    # value => the exact value we desire the interpolation for

    y = np.interp(value, x, y)

    return y


# A function that computes the center of Gravity of 2 Arrays
def Centroid(x, aggregate):
    # This function takes in the x-axis of the curve and the aggregated area of the
    # fuzzy set and returns the centroid position

    centroid = np.sum(x * aggregate) / np.sum(aggregate)

    return centroid


# A function that computes the mean of maximum of 2 arrays
def MeanOfMax(x, a):
    # This function takes in a 1-D array a => aggregate of the fuzzy logic
    # another 1-D array x=> the x-axis
    # Returns the mean of the maximum value(s) of the aggregate array

    idx = np.argwhere(a == np.max(a))  # Finding the index of all max values on the y-axis

    res = np.mean(x[idx])  # computing the mean of the max values on the x-axis

    return res


# Generating the universe variables
#   *Ammo and Health input ranges [0, 100]
#   *Action output ranges [0, 100]

# Generating the points from 1 to 100
n = 1000  # number of points
x_ammo = np.linspace(0, 100, n)
x_health = np.linspace(0, 100, n)
x_action = np.linspace(0, 100, n)


# Fuzzy Logic Game Engine
#   This function takes in the health and ammo value and returns the
#   fuzzy action output after applying fuzzy logic
#   it returns 4 outputs: *the crisp value from Sum aggregate and centroid defuzz
#                         *the crisp value from Sum aggregate and Mean of Maximum defuzz
#                         *the crisp value from Max aggregate and Mean of Maximum defuzz
#                         *the crisp value from Max aggregate and Mean of Maximum defuzz
def fuzzyEngine(x_ammo, x_health, x_action, health, ammo):
    # This function takes in the ammo x-axis, health x-axis, ammo x-axis
    # the health and ammo input
    # Then returns the crisp value of the action to be take.

    # Creating triangle fuzzy membership functions for the ammo
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

    # Calculating the degree of membership for the input variables
    # Degree of memberships for ammo
    ammo_level_vlo = Interpolate(x_ammo, ammo_vlo, ammo)
    ammo_level_lo = Interpolate(x_ammo, ammo_lo, ammo)
    ammo_level_md = Interpolate(x_ammo, ammo_md, ammo)
    ammo_level_hi = Interpolate(x_ammo, ammo_hi, ammo)
    ammo_level_vhi = Interpolate(x_ammo, ammo_vhi, ammo)

    # Degree of memberships for health
    health_level_vlo = Interpolate(x_health, health_vlo, health)
    health_level_lo = Interpolate(x_health, health_lo, health)
    health_level_md = Interpolate(x_health, health_md, health)
    health_level_hi = Interpolate(x_health, health_hi, health)
    health_level_vhi = Interpolate(x_health, health_vhi, health)

    # Applying the rules specified by the article.
    # The condition is the AND condition, thus we use the MIN operator
    # There are 25 rules in total from the article

    rule1 = np.fmin(ammo_level_vlo, health_level_vlo)  # ammo very low and health very low => hide
    rule2 = np.fmin(ammo_level_vlo, health_level_lo)  # ammo very low and health low => hide
    rule3 = np.fmin(ammo_level_vlo, health_level_md)  # ammo very low and health mid => run away
    rule4 = np.fmin(ammo_level_vlo, health_level_hi)  # ammo very low and health high => run away
    rule5 = np.fmin(ammo_level_vlo, health_level_vhi)  # ammo very low and health very high => stop

    rule6 = np.fmin(ammo_level_lo, health_level_vlo)  # ammo low and health very low => hide
    rule7 = np.fmin(ammo_level_lo, health_level_lo)  # ammo low and health low => run away
    rule8 = np.fmin(ammo_level_lo, health_level_md)  # ammo low and health mid => run away
    rule9 = np.fmin(ammo_level_lo, health_level_hi)  # ammo low and health high => stop
    rule10 = np.fmin(ammo_level_lo, health_level_vhi)  # ammo low and health very high => walk around

    rule11 = np.fmin(ammo_level_md, health_level_vlo)  # ammo mid and health very low  => run away
    rule12 = np.fmin(ammo_level_md, health_level_lo)  # ammo mid and health low => run away
    rule13 = np.fmin(ammo_level_md, health_level_md)  # ammo mid and health mid => stop
    rule14 = np.fmin(ammo_level_md, health_level_hi)  # ammo mid and health high => walk around
    rule15 = np.fmin(ammo_level_md, health_level_vhi)  # ammo mid and health very high => walk around

    rule16 = np.fmin(ammo_level_hi, health_level_vlo)  # ammo high and health very low  => run away
    rule17 = np.fmin(ammo_level_hi, health_level_lo)  # ammo high and health low => stop
    rule18 = np.fmin(ammo_level_hi, health_level_md)  # ammo high and health mid => walk around
    rule19 = np.fmin(ammo_level_hi, health_level_hi)  # ammo high and health high => walk around
    rule20 = np.fmin(ammo_level_hi, health_level_vhi)  # ammo high and health very high => attack

    rule21 = np.fmin(ammo_level_vhi, health_level_vlo)  # ammo very high and health very low => stop
    rule22 = np.fmin(ammo_level_vhi, health_level_lo)  # ammo very high and health low => walk around
    rule23 = np.fmin(ammo_level_vhi, health_level_md)  # ammo very high and health mid => walk around
    rule24 = np.fmin(ammo_level_vhi, health_level_hi)  # ammo very high and health high => attack
    rule25 = np.fmin(ammo_level_vhi, health_level_vhi)  # ammo very high and health very high => attack

    # Finding the points in the universe activated by the rules
    # This is useful for plotting the region on the graph
    # The logic is to cut the output domain but the y-value of the rules
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

    # Aggregation of Output
    # Max Aggregation
    max_aggregated_output = np.fmax(rule1_area, np.fmax(rule2_area, np.fmax(rule3_area, np.fmax(rule4_area, np.fmax(rule5_area,
                            np.fmax(rule6_area, np.fmax(rule7_area, np.fmax(rule8_area, np.fmax(rule9_area, np.fmax(rule10_area,
                            np.fmax(rule11_area, np.fmax(rule12_area, np.fmax(rule13_area, np.fmax(rule14_area, np.fmax(rule15_area,
                            np.fmax(rule16_area, np.fmax(rule17_area, np.fmax(rule18_area, np.fmax(rule19_area, np.fmax(rule20_area,
                            np.fmax(rule21_area, np.fmax(rule22_area, np.fmax(rule23_area, np.fmax(rule24_area, rule25_area))))))))))))))))))))))))

    # Defuzzification
    # Max aggregated output and Centroid Defuzzification
    max_centroid = Centroid(x_action, max_aggregated_output)

    return max_centroid


# Testing the engine with single value
healthValue = 82
ammoValue = 22

action = fuzzyEngine(x_ammo, x_health, x_action, healthValue, ammoValue)

print('The crisp value for the action is: ', action)


# for plotting the 3D surface with 100 discrete points due computational constraints
p = 25  # THe number of discrete points
x = np.linspace(0, 100, p)  # ammo axis
y = np.linspace(0, 100, p)  # health axis
z = np.linspace(0, 100, p)  # action axis
Z = np.zeros((p, p))  # an matrix of zero with the desired shape of output

# iterating to solve every possible combination of values in the given domain
for i in range(p):
    for j in range(p):
        ammoValue = x[i]
        healthValue = y[j]
        a = fuzzyEngine(x, y, x_action, healthValue, ammoValue)
        Z[i][j] = a

    
# Developing the 3D surface plot
X, Y = np.meshgrid(x, y)

# Pseudo Color Plot
fig = plt.figure()
plt.pcolor(X, Y, Z, cmap='viridis', edgecolor='k', linewidths=1)
plt.title("Mesh Plot of Input and Output Parameters")

# 3D surface plot
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', linewidths=1)

ax.set_xlabel('Ammo')
ax.set_ylabel('Health')
ax.set_zlabel("Action")
ax.set_title('Evolution of Input and Output Parameters')

plt.show()