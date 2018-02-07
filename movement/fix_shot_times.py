from __future__ import print_function

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
from tqdm import tqdm
import math

import warnings
warnings.filterwarnings('ignore')

from movement import utils
import movement.config as CONFIG


def load_shots():
    """
    Load shots only from game events

    Parameters
    ----------
    game_events: pandas.DataFrame

    Returns
    -------
    shots: pandas.DataFrame
    """
    shots = pd.read_csv('%s/%s' % (CONFIG.data.shots.dir, 'shots.csv'))
    shots.loc[:, 'EVENTTIME'] = utils.convert_time(minutes=shots.loc[:, 'MINUTES_REMAINING'].values, seconds = shots.loc[:, 'SECONDS_REMAINING'].values)
    shots['GAME_ID'] = '00' + shots['GAME_ID'].astype(int).astype(str)

    return shots


def sg_filter(x, m, k=0):
    """
    x = Vector of sample times
    m = Order of the smoothing polynomial
    k = Which derivative
    """
    mid = len(x) / 2
    a = x - x[mid]
    expa = lambda x: map(lambda i: i**x, a)
    A = np.r_[map(expa, range(0,m+1))].transpose()
    Ai = np.linalg.pinv(A)

    return Ai[k]


def smooth(x, y, size=5, order=2, deriv=0):

    if deriv > order:
        raise Exception, "deriv must be <= order"

    n = len(x)
    m = size

    result = np.zeros(n)

    for i in xrange(m, n-m):
        start, end = i - m, i + m + 1
        f = sg_filter(x[start:end], order, deriv)
        result[i] = np.dot(f, y[start:end])

    if deriv > 1:
        result *= math.factorial(deriv)

    return result

def plot(t, plots, shot_ind):
    n = len(plots)

    for i in range(0,n):
        label, data = plots[i]

        plt = py.subplot(n, 1, i+1)
        plt.tick_params(labelsize=8)
        py.grid()
        py.xlim([t[0], t[-1]])
        py.ylabel(label)

        py.plot(t, data, 'k-')
        py.scatter(t[shot_ind], data[shot_ind], marker='*', c='g')

    py.xlabel("Time")
    py.show()
    py.close()

def create_figure(order, shot_time):
    fig = py.figure(figsize=(8,6))
    nth = 'th'
    if order < 4:
        nth = ['st','nd','rd','th'][order-1]

    title = "Shot Time: %s" % (shot_time)

    fig.text(.5, .92, title, horizontalalignment='center')



def correct_shots(game_shots, movement, events):
    """
    Load shots only from game events

    Parameters
    ----------
    game_shots: pandas.DataFrame
        contains play-by-play data for single game shots
    movement: pandas.DataFrame
        SportVU movement data for a single game
    events: pandas.DataFrame
        contains play-by-play data

    Returns
    -------
    shots: pandas.DataFrame
        contains play-by-play with location data associated
    """
    fixed_shots = pd.DataFrame(columns=game_shots.columns)
    fixed_shots['QUARTER'] = 0

    for ind, shot in game_shots.iterrows():

        try:
            event_id = shot['GAME_EVENT_ID']

            movement_around_shot = movement.loc[movement.event_id.isin([event_id, event_id - 1])]
            movement_around_shot.drop_duplicates(subset=['game_clock'], inplace=True)

            game_clock_time = movement_around_shot.loc[movement_around_shot.team_id == -1, 'game_clock'].values
            ball_height = movement_around_shot.loc[movement_around_shot.team_id == -1, 'radius'].values

            size = 10
            order = 3

            params = (game_clock_time, ball_height, size, order)

            # plots = [
            #     ["Position", ball_height],
            #     ["Position Smoothed", smooth(*params, deriv=0)],
            #     ["Velocity", smooth(*params, deriv=1)],
            #     ["Acceleration", smooth(*params, deriv=2)]
            # ]

            position_smoothed = smooth(*params, deriv=0)
            # velocity_smoothed = smooth(*params, deriv=1)
            acceleration_smoothed = smooth(*params, deriv=2)
            max_ind = np.argmax(position_smoothed)

            shot_window = acceleration_smoothed[np.max([0, max_ind - 25]): max_ind]
            shot_min_ind = np.argmin(shot_window)
            shot_ind = max_ind - shot_min_ind
            shot_time = game_clock_time[shot_ind]

            # create_figure(order, shot_time)
            # plot(game_clock_time, plots, shot_ind)

            quarter = movement_around_shot.loc[:, 'quarter'].values[0]
            movement_around_shot = movement_around_shot.loc[movement_around_shot.game_clock == shot_time, :]

            shot['QUARTER'] = quarter
            shot['SHOT_TIME'] = shot_time
            shot['LOC_X'] = movement_around_shot.loc[movement_around_shot.team_id == -1, 'x_loc'].values[0]
            shot['LOC_Y'] = movement_around_shot.loc[movement_around_shot.team_id == -1, 'y_loc'].values[0]

        except Exception as err:
            continue

        fixed_shots = fixed_shots.append(shot)

    return fixed_shots

if __name__ == '__main__':
    game_dir = CONFIG.data.movement.converted.dir
    event_dir = CONFIG.data.events.dir

    games = utils.get_games()
    events = utils.get_events(event_dir, games)
    shots = load_shots()
    fixed_shots = pd.DataFrame(columns=shots.columns)

    for game in tqdm(games):
        try:
            game_movement = pd.read_csv('%s/%s_converted.csv' % (game_dir, game))
            game_shots = shots.loc[shots.GAME_ID == game, :]
            game_events = events.loc[events.GAME_ID == game, :]
        except IOError as err:
            print(err)
            continue

        fixed_shots = fixed_shots.append(correct_shots(game_shots, game_movement, game_events))

    fixed_shots.to_csv('%s/%s_fixed.csv' % (CONFIG.data.shots.dir, 'shots'), index=False)
