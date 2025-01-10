import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import csv
import brain
import importlib
importlib.reload(brain)

class Bear:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50
        
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def move_towards(self, other, step_size):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = self.distance_to(other)
        if distance > 0:  # Avoid division by zero
            self.x += step_size * dx / distance
            self.y += step_size * dy / distance

# Define a class for the dots
class Dot:
    def __init__(self, sepal_length, sepal_width, food_type, x, y):
        self.x = x
        self.y = y
        self.size = 50
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.food_type = food_type
        self.is_tested = False
        if self.food_type=='food':
            self.color = "green"
        else:
            self.color = "red"




# Initialize the main dot and random surrounding dots
import random
random.seed(42)
with open('forestdata.csv', 'r') as file:
    my_reader = csv.reader(file, delimiter=',')
    random_dots=[]
    for row in my_reader:
        random_dots.append(Dot(float(row[0]),float(row[1]),row[2],float(row[3]),float(row[4])))
        
        
bear = Bear(5, 5)  # Start in the center of the 10x10 grid

# Helper function to find the nearest dot
def find_nearest_dot(bear, dots):
    nearest_dot = None
    min_distance = float('inf')
    for dot in dots:
        distance = bear.distance_to(dot)
        if distance < min_distance and not dot.is_tested:
            min_distance = distance
            nearest_dot = dot
        
    prediction=brain.knn(nearest_dot)
    return nearest_dot,prediction
# Initialize the plot
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 250)
ax.set_ylim(0, 250)

# Plot the initial dots
bear_plot = ax.scatter(bear.x, bear.y, s=bear.size, c="grey", label="Bear")
random_dots_plot = ax.scatter([dot.x for dot in random_dots],[dot.y for dot in random_dots], s=[dot.size for dot in random_dots], c=[dot.color for dot in random_dots], label="Berrys")
ax.legend()

# Animation function
def update(frame):
    global bear, random_dots

    if not random_dots:
        return bear_plot, random_dots_plot
    # Find the nearest dot
    nearest_dot, prediction = find_nearest_dot(bear, random_dots)
    # Move the main dot towards the nearest dot
    bear.move_towards(nearest_dot, step_size=1)
    # If the main dot is close enough to the nearest dot, "consume" it
    if bear.distance_to(nearest_dot) < 2 :
        nearest_dot.is_tested=True
        if prediction=='food' :
            if nearest_dot.food_type=='food':
                bear.size += 20  # Increase the size of the main dot
                random_dots.remove(nearest_dot)
            else:
                bear.size = 5
                random_dots.remove(nearest_dot)
        elif prediction=='poison':
            nearest_dot.is_tested=True
            #random_dots.remove(nearest_dot)
        

    # Update the plots
    bear_plot.set_offsets([[bear.x, bear.y]])
    bear_plot.set_sizes([bear.size])
    random_dots_plot.set_offsets([[dot.x, dot.y] for dot in random_dots])
    random_dots_plot.set_sizes([dot.size for dot in random_dots])
    random_dots_plot.set_facecolor(['orange' if dot.is_tested and dot.food_type=='food' else dot.color for dot in random_dots])

    return bear_plot, random_dots_plot

# Create the animation
ani = FuncAnimation(fig, update, frames=10000, interval=10, blit=True)

# Show the animation
plt.show()
