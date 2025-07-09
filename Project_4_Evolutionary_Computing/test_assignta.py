"""
Name: Roshan Peri/Freddy Elyas
File: test_assignta.py
Purpose: Tests to see if the code is running correctly using a pytest 
"""

import pandas as pd
import pytest
from assignta import overallocation, conflicts, undersupport, unavailable, unpreferred

def load_solution(path):
    df = pd.read_csv(path, header=None)
    df.index.name = 'ta'
    df.columns = list(range(df.shape[1]))
    sol = [(ta, sec) for ta in df.index for sec in df.columns if df.loc[ta, sec] == 1]
    return sol

test_cases = {
    "test1": (r"./assignta_data/test1.csv", [34, 7, 1, 59, 10]),
    "test2": (r"./assignta_data/test2.csv", [37, 5, 0, 57, 16]),
    "test3": (r"./assignta_data/test3.csv", [19, 2, 11, 34, 17]),
}

@pytest.mark.parametrize("name,expected", test_cases.items()) #ChatGPT code 
def test_objectives(name, expected):
    path, scores = expected
    sol = load_solution(path)
    assert overallocation(sol) == scores[0], f"{name} overallocation"
    assert conflicts(sol) == scores[1], f"{name} conflicts"
    assert undersupport(sol) == scores[2], f"{name} undersupport"
    assert unavailable(sol) == scores[3], f"{name} unavailable"
    assert unpreferred(sol) == scores[4], f"{name} unpreferred"
