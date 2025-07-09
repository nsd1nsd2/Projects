"""
Name: Roshan Peri/Freddy Elyas 
File: evo.py
Description: An evolutionary computing framework for solving
multi-objective optimization problems.

Finds pareto-optimal solutions revealing tradeoffs between different
objectives

Note: Most of code is from class 
"""

import random as rnd
import copy
import pandas as pd
import numpy as np
from functools import reduce

class Evo:

    def __init__(self):
        self.pop = {}  # scores (tuple) --> solution
        self.objectives = {}   # name --> obj function (goals)
        self.agents = {}  # agents: name -> (operator, num_solutions_input)

    def add_objective(self, name, f):
        self.objectives[name] = f

    def add_agent(self, name, op, k=1):
        self.agents[name] = (op, k)

    def get_random_solutions(self, k=1):
        if len(self.pop) == 0:
            return []
        all_solutions = list(self.pop.values())
        return [copy.deepcopy(rnd.choice(all_solutions)) for _ in range(k)]

    def add_solution(self, sol):
        scores = tuple([(name, f(sol)) for name, f in self.objectives.items()])
        self.pop[scores] = sol

    def run_agent(self, name):
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    @staticmethod
    def dominates(p, q):
        pscores = np.array([score for name, score in p])
        qscores = np.array([score for name, score in q])
        score_diffs = qscores - pscores
        return min(score_diffs) >= 0 and max(score_diffs) > 0

    @staticmethod
    def reduce_nds(S, p):
        return S - {q for q in S if Evo.dominates(p, q)}

    def remove_dominated(self):
        nds = reduce(Evo.reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def evolve(self, n=1, dom=100, time_limit=None):
        import time
        start_time = time.time()
        agent_names = list(self.agents.keys())

        for i in range(n):
            if time_limit and (time.time() - start_time) > time_limit:
                break
            pick = rnd.choice(agent_names)
            self.run_agent(pick)
            if i % dom == 0:
                self.remove_dominated()
                print(self)

        self.remove_dominated()

    def summarize(self, groupname="team"):
        """
        Purpose: Summarizes the evolutionary computation in a pandas dataframe 
        """
        rows = []
        for scores, sol in self.pop.items():
            row = {k: v for k, v in scores}
            row["groupname"] = groupname
            rows.append(row)
        df = pd.DataFrame(rows)
        df = df[["groupname"] + list(self.objectives.keys())]
        return df

    def __str__(self):
        rslt = ""
        for scores, sol in self.pop.items():
            rslt += str(dict(scores))+":\t"+str(sol)+"\n"
        return rslt
