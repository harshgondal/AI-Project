import tkinter as tk
from tkinter import messagebox
import random

def get_fitness(state, coefficients, target):
    present_value = sum(state[i] * coefficients[i] for i in range(len(state)))
    diff = abs(target - present_value)
    fitness = 1 / (1 + diff)
    return fitness

def get_selection_probability(curr_gen, coefficients, target):
    fitness = {i: get_fitness(curr_gen[i], coefficients, target) for i in range(len(curr_gen))}
    total = sum(fitness.values())
    probabilities = {i: fitness[i] / total for i in range(len(curr_gen))}
    return probabilities

def search(utility, key):
    if key == 0:
        return 0
    for i in range(1, len(utility)):  
        if utility[i] > key and utility[i-1] <= key:
            return i-1

def get_selected(curr_gen, coefficients, target):
    selected = []
    probabilities = get_selection_probability(curr_gen, coefficients, target)
    utility = [0]
    utility.extend(utility[-1] + probabilities[i] for i in range(len(curr_gen)))
    for _ in range(len(curr_gen)):
        temp = random.random()
        index = search(utility, temp)
        selected.append(curr_gen[index])
    return selected

def get_children(curr_gen, coefficients, target):
    children = []
    selected = get_selected(curr_gen, coefficients, target)
    while len(children) < len(curr_gen):
        temp1 = random.randint(0, len(selected) - 1)
        while True:
            temp2 = random.randint(0, len(selected) - 1)
            if temp1 != temp2:
                break
        parent1 = selected[temp1]
        parent2 = selected[temp2]
        crossover = random.randint(0, len(parent1))
        child = parent1[:crossover] + parent2[crossover:]
        if random.random() < 0.01:  
            index = random.randint(0, len(child) - 1)
            new_gene = random.randint(0, 9)
            child[index] = new_gene
        children.append(child)  
    return children

def configure_random(nor_first_gen, coefficients):
    return [[random.randint(0, 9) for _ in range(len(coefficients))] for _ in range(nor_first_gen)]

def run_genetic_algorithm():
    coefficients = [int(coefficients_entries[i].get()) for i in range(6)]
    target = int(target_entry.get())
    nor_first_gen = int(nor_first_gen_entry.get())

    perfect_specimens = []

    best = 0
    answer = 0
    curr_gen = configure_random(nor_first_gen, coefficients)

    for _ in range(30):
        next_gen = get_children(curr_gen, coefficients, target)
        for state in next_gen:
            temp = get_fitness(state, coefficients, target)
            if temp == 1 and state not in perfect_specimens:
                perfect_specimens.append(state)
                messagebox.showinfo("Perfect Specimen Found", f"Perfect Specimen: {state}")
                answer = state
                return
            elif(temp>best):
                best = temp
                answer = state.copy()
        curr_gen = next_gen

    messagebox.showinfo("Best Answer", f"No perfect specimen found.\nBest Answer: {answer}")

# GUI Setup
root = tk.Tk()
root.title("Genetic Algorithm Optimizer")

# Statement about coefficients
statement_label = tk.Label(root, text="There are 6 variables which multiplied with some coefficients give some target. This project deals with solving such optimization problems using genetic algorithm.")
statement_label.grid(row=0, columnspan=2, padx=5, pady=5)

# Coefficients Input
coefficients_labels = ['a', 'b', 'c', 'd', 'e', 'f']
coefficients_entries = []
for i, label in enumerate(coefficients_labels):
    tk.Label(root, text=f"Coefficient for {label}:").grid(row=i+1, column=0, padx=5, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=i+1, column=1, padx=5, pady=5)
    coefficients_entries.append(entry)

# Target Input
target_label = tk.Label(root, text="Target:")
target_label.grid(row=8, column=0, padx=5, pady=5)
target_entry = tk.Entry(root)
target_entry.grid(row=8, column=1, padx=5, pady=5)

# Number of Individuals Input
nor_first_gen_label = tk.Label(root, text="Number of Individuals in First Generation:")
nor_first_gen_label.grid(row=9, column=0, padx=5, pady=5)
nor_first_gen_entry = tk.Entry(root)
nor_first_gen_entry.grid(row=9, column=1, padx=5, pady=5)

# Run Button
run_button = tk.Button(root, text="Run Genetic Algorithm", command=run_genetic_algorithm)
run_button.grid(row=10, columnspan=2, padx=5, pady=10)

root.mainloop()
