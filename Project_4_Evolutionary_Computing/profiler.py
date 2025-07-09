"""
Name: Roshan Peri/Fredy Elyas
File: profiler.py
Purpose: Runs a profiler of the TA allocation 
"""
import cProfile
import pstats


def profile_main():
    """
    Purpose: Profiling a shorter evolution run,
    measuring function execution time to help identify bottlenecks
    and prove that our algorithm can indeed
    scale to the 5-minute requirement"""
    print("Starting profiling...")
    cProfile.run("""
import sys
sys.path.append('.')
from assignta import *

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

for _ in range(50):
    evo.add_solution(make_random_solution())
evo.evolve(n=3000, dom=500, time_limit=60)  
""", 'evolution_profile.prof') #ChatGPT code 

    # loading profile results from generated .prof file
    stats = pstats.Stats('evolution_profile.prof')

    # sorting results by the cumulative time (can see what's taking the longest)
    stats.sort_stats('cumulative')

    # saving profile data to output file 'ds3500team_profile.txt'
    stats.dump_stats('ds3500team_profile.txt')

    print("Profile saved to ds3500team_profile.txt")
    print("Run complete!")


if __name__ == "__main__":
    profile_main()