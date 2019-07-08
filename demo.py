import pandas as pd
import numpy as np
import argparse

def get_paths(capital=100000,
              bet_fraction=0.01,
              num_rolls=5000,
              num_iter=500):
    """
    Return pandas dataframe with capital paths.

    Parameters:
    ----------
    capital = starting capital
    bet_fraction = fraction to be bet on every roll
    num_rolls = maximum number of rolls for every iteration (after capital reaches zero, subsequent capital_path vales set to NaN)
    num_iter = number of iterations in the monte carlo simulation
    """
    
    # do all the roullete rolls and put results into ndarray
    rolls = np.random.randint(1, 39, (num_rolls, num_iter))
    # initiate variable with required size
    capital_path = np.ones((num_rolls, num_iter))
    # assign starting capital value for every iteration
    capital_path[0] *= capital
    # add one more row to be able to use index num_rolls + 1
    capital_path = np.append(capital_path, [np.zeros(num_iter)],
                             axis=0)
    # do path calculations for every iteration
    for n, roll in enumerate(rolls):
        betsize = np.minimum(
            np.maximum(
                # bet a fraction of capital
                np.floor(capital_path[n] * bet_fraction),
                # but no less than 1
                np.ones(num_iter)),
            # unless you don't have 1
            capital_path[n])
        capital_path[n+1] = np.maximum(
            # this is a lose
            capital_path[n] - betsize
            # this is a win
            + (roll == 32) * betsize * 37,
            # make sure not to go negative
            np.zeros(num_iter))
    return pd.DataFrame(capital_path).replace(0, np.NaN)

def annualize(r, s):
    """
    Given per roll return and std return annualized values
    as a tuple (return, std)
    """
    rolls_per_annum = 6 * 8 * 250
    r = (1 + r) ** rolls_per_annum -1 
    s = s * np.sqrt(rolls_per_annum)
    return (r, s)


if __name__ == '__main__':
    # this is only for parsing command line arguments
    parser = argparse.ArgumentParser(
        'Monte Carlo simulator for roulette betting.', add_help=True)
    parser.add_argument('-c', '--capital',
                        help='starting capital',
                        default=1000000, type=float)
    parser.add_argument('-f', '--bet_fraction',
                        help='fraction of capital to be bet on every roulette roll',
                        default=0.01, type=float)
    parser.add_argument('-r', '--num_rolls',
                        help='maximum number of rolls',
                        default=10000, type=int)
    parser.add_argument('-i', '--num_iter',
                        help='number of iterations in this monte carlo simulation',
                        default=1000, type=int)
    args = vars(parser.parse_args())
    print(args)


    # this is actual programme
    path = get_paths(**args)
    returns = path.pct_change(limit=1)
    returns_median = returns.median(skipna=True).median()
    std = returns.std().median()
    print('--------------')
    print('median return per roll:')
    print('{:.2%}'.format(returns_median))
    print('median roll return std:')
    print(std)
    print('--------------')
    print('Annualized (6 bets per hour x 8 hours daily x 250 days per year)')
    a = annualize(returns_median, std)
    print('return:')
    print('{:.2%}'.format(a[0]))
    print('std:')
    print(a[1])
    


