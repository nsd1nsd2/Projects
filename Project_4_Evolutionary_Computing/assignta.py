"""
Name: Roshan Peri/Freddy Elyas
File: assignta.py
Purpose: Helps the optimal placements 
for the TA's 
"""

import pandas as pd
import numpy as np
import time 
import random as rnd
from evo import Evo

#Load data 
sections_df = pd.read_csv(r"./assignta_data/sections.csv")
tas_df = pd.read_csv(r"./assignta_data/tas.csv")

tas_df['ta_id'] = tas_df['ta_id'].replace(48, 38)

# Organize data 
section_times = dict(zip(sections_df.section, sections_df.daytime))
section_min = dict(zip(sections_df.section, sections_df.min_ta))
section_max = dict(zip(sections_df.section, sections_df.max_ta))
ta_max = dict(zip(tas_df.ta_id, tas_df.max_assigned))
ta_prefs = tas_df.drop(columns=["max_assigned"])
ta_prefs.columns = ta_prefs.columns.astype(str)
ta_prefs = ta_prefs.set_index("ta_id").fillna("")
ta_prefs = ta_prefs.astype(str)

sections = list(sections_df.section)
tas = list(tas_df.ta_id)

def make_random_solution():
    """
    Purpose: Create a randomized table for all 
    the TA's based on their availablility 
    """
    sol = []
    for sec in sections:
        num_tas = rnd.randint(section_min[sec], section_max[sec])
        available_tas = [ta for ta in tas if ta_prefs.loc[ta][str(sec)] != 'U']
        chosen = rnd.sample(available_tas, min(num_tas, len(available_tas)))
        for ta in chosen:
            sol.append((ta, sec))
    return sol


def overallocation(sol):
    """
    Purpose: To minimize the overallocation of the TA's 
    by calculating the overallocation of all the TA's 
    """
    df = pd.DataFrame(sol, columns=['ta', 'sec'])
    ta_counts = df['ta'].value_counts()
    over = 0
    for ta, count in ta_counts.items():
        limit = ta_max.get(ta, 0)
        if count > limit:
            over += count - limit
    return over 


def conflicts(sol):
    """
    Purpose: Finds the number of TA's that have 
    conflicts with the sections that they are assigned
    """

    df = pd.DataFrame(sol, columns=['ta', 'sec'])
    df['time'] = df.sec.map(section_times)
    conflict_counts = df.duplicated(subset=['ta', 'time']).groupby(df.ta).any().sum() #ChatGPT code
    return conflict_counts

def undersupport(sol):
    """
    Purpose: Finds the total number of TA's per section 
    and returns the number of sections that don't have 
    enough TA's
    """
    df = pd.DataFrame(sol, columns=['ta', 'sec'])
    assigned = df.sec.value_counts()
    total = 0
    for sec in section_min:
        assigned_count = assigned.get(sec, 0)
        required = section_min[sec]
        if assigned_count < required:
            total += required - assigned_count
    return total


def unavailable(sol):
    """
    Purpose: Trys to find the number of 
    allocated TA's where they are in a 
    section but are unavailable and 
    returns the count of that 
    """
    count = 0
    for ta, sec in sol:
        try:
            if ta_prefs.loc[ta, str(sec)] == 'U':
                count += 1
        except KeyError: #ChatGPT code to deal with missing data values
            continue 
    return count


def unpreferred(sol):
    """
    Purpose: Trys to find the number of 
    allocated TA's where they are in a 
    section but are willing but not 
    preferred and returns a count for that
    """
    count = 0
    for ta, sec in sol:
        try:
            if ta_prefs.loc[ta, str(sec)] == 'W':
                count += 1
        except KeyError: #ChatGPT code to deal with missing data values 
            continue 
    return count


def mutate_add_random(sols):
    """
    Purpose: Adds new solutions to the model
    """
    sol = sols[0]
    new = sol[:]
    sec = rnd.choice(sections)
    ta = rnd.choice(tas)
    new.append((ta, sec))
    return new


def mutate_remove_random(sols):
    """
    Purpose: Removes a random solution from the model 
    """
    sol = sols[0] 
    if not sol: return sol[:]
    new = sol[:]
    new.pop(rnd.randint(0, len(new)-1))
    return new



def mutate_swap(sols):
    """
    Purpose: Swaps two solutions in the model 
    """
    sol = sols[0]  
    if len(sol) < 2: return sol[:]
    new = sol[:]
    i, j = rnd.sample(range(len(new)), 2)
    new[i], new[j] = new[j], new[i]
    return new

def mutate_tweak_ta(sols):
    """
    Purpose: Tweaks two TA solutions in the model 
    """
    sol = sols[0]  
    if not sol: return sol[:]
    new = sol[:]
    idx = rnd.randint(0, len(new)-1)
    ta = rnd.choice(tas)
    new[idx] = (ta, new[idx][1])
    return new
def load_solution(path):
    df = pd.read_csv(path, header=None)
    df.index.name = 'ta'
    df.columns = list(range(df.shape[1]))
    sol = [(ta, sec) for ta in df.index for sec in df.columns if df.loc[ta, sec] == 1]
    return sol


if __name__ == "__main__":
    evo = Evo()


    evo.add_objective("overallocation", overallocation)
    evo.add_objective("conflicts", conflicts)
    evo.add_objective("undersupport", undersupport)
    evo.add_objective("unavailable", unavailable)
    evo.add_objective("unpreferred", unpreferred)


    evo.add_agent("add", mutate_add_random)
    evo.add_agent("remove", mutate_remove_random)
    evo.add_agent("swap", mutate_swap)
    evo.add_agent("tweak", mutate_tweak_ta)

    print("Generating initial population...")
    for _ in range(100):
        evo.add_solution(make_random_solution())

 
    print("Starting 5-minute evolution...")
    start_time = time.time()

    evo.evolve(n=100000, dom=1000, time_limit=300)

    end_time = time.time()
    runtime = end_time - start_time

    summary = evo.summarize(groupname="ds3500team")
    summary.to_csv("ds3500team_summary.csv", index=False)

    print(f"Found {len(summary)} solutions")
    print(f"Total runtime: {runtime:.2f} seconds ({runtime / 60:.2f} minutes)")
