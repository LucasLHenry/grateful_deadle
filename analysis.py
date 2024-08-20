from game_algorithm import generate_game
from lib.database.utils import run_with_timeout, calc_game_difficulty
from lib.database.utils import generate_play_amounts
from math import sqrt
import matplotlib.pyplot as plt

def main():
    # game_difficulty_analysis()
    play_amount_analysis()

avg = lambda x: sum(x)/len(x)
std = lambda x, avg: sqrt(sum([(val - avg)**2 for val in x]) / (len(x) - 1))

def play_amount_analysis():
    play_amts = [amt for _, amt in generate_play_amounts().items()]
    plt.hist(play_amts, density=False, bins=50)
    plt.show()

def game_difficulty_analysis():
    meds = []
    for _ in range(1000):
        med = calc_game_difficulty(run_with_timeout(generate_game, 0.25, restart=True), True)
        meds.append(med)
    print(f"\naverage score is {avg(meds):.2f}, standard deviation is {std(meds, avg(meds)):.2f}")
    plt.hist(meds, density=False, bins=30)
    
    num_bins = 5
    meds = sorted(meds)
    n = len(meds)
    bin_size = int(n / num_bins)  # number of bins
    bin_cutoffs = [int(max(meds[i*bin_size:(i+1)*bin_size])) for i in range(num_bins)]
    print(bin_cutoffs)
    plt.show()
    
    
if __name__ == "__main__":
    main()