from __future__ import print_function

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
from tqdm import tqdm
import math

import warnings
warnings.filterwarnings('ignore')

from rebound.data import utils
import rebound.config as CONFIG

def load_rebounds(game_events):
    """
    Load rebounds only from game events

    Parameters
    ----------
    game_events: pandas.DataFrame

    Returns
    -------
    rebounds: pandas.DataFrame
    """
    rebounds = game_events.loc[game_events.EVENTMSGTYPE == 4,:]
    rebounds.loc[:, 'EVENTTIME'] = utils.convert_time(rebounds.loc[:, 'PCTIMESTRING'].values)

    return rebounds


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

def plot(t, plots, rim_ind, shot_ind):
    n = len(plots)

    for i in range(0,n):
        label, data = plots[i]

        plt = py.subplot(n, 1, i+1)
        plt.tick_params(labelsize=8)
        py.grid()
        py.xlim([t[0], t[-1]])
        py.ylabel(label)

        py.plot(t, data, 'k-')
        py.scatter(t[rim_ind], data[rim_ind], marker='*', c='r')
        py.scatter(t[shot_ind], data[shot_ind], marker='*', c='g')

    py.xlabel("Time")

def create_figure(size, order, rim_time, shot_time):
    fig = py.figure(figsize=(8,6))
    nth = 'th'
    if order < 4:
        nth = ['st','nd','rd','th'][order-1]

    title = "Rim Time: %s, Shot Time: %s" % (rim_time, shot_time)

    fig.text(.5, .92, title, horizontalalignment='center')



def correct_rebounds(game_rebounds, movement, events):
    """
    Load rebounds only from game events

    Parameters
    ----------
    rebounds: pandas.DataFrame
        contains play-by-play data for rebounds
    movement: pandas.DataFrame
        SportVU movement data for a single game
    events: pandas.DataFrame
        contains play-by-play data

    Returns
    -------
    rebounds: pandas.DataFrame
        contains play-by-play with location data associated
    """
    fixed_rebounds = pd.DataFrame(columns=game_rebounds.columns)
    fixed_rebounds['QUARTER'] = 0

    for ind, rebound in game_rebounds.iterrows():

        try:
            event_id = rebound['EVENTNUM']
            shot_event = game_rebounds.loc[game_rebounds.EVENTNUM == event_id, :]

            movement_around_rebound = movement.loc[movement.event_id.isin([event_id, event_id - 1])]
            movement_around_rebound.drop_duplicates(subset=['game_clock'], inplace=True)

            shot_clock_time = movement_around_rebound.loc[movement_around_rebound.team_id == -1,'shot_clock'].values
            game_clock_time = movement_around_rebound.loc[movement_around_rebound.team_id == -1, 'game_clock'].values
            ball_height = movement_around_rebound.loc[movement_around_rebound.team_id == -1, 'radius'].values

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
            velocity_smoothed = smooth(*params, deriv=1)
            acceleration_smoothed = smooth(*params, deriv=2)
            max_ind = np.argmax(position_smoothed)

            shot_vel_window = velocity_smoothed[np.max([0, max_ind - 25]): max_ind]
            shot_min_vel_ind = np.argmin(shot_vel_window)
            shot_ind = max_ind - shot_min_vel_ind
            shot_time = game_clock_time[shot_ind]

            rim_acceleration_window = acceleration_smoothed[max_ind: max_ind + 20]
            rim_max_accel_ind = np.argmax(rim_acceleration_window)
            rim_ind = max_ind + rim_max_accel_ind
            rim_time = game_clock_time[rim_ind]

            # create_figure(size, order, rim_time, shot_time)
            # plot(game_clock_time, plots, rim_ind, shot_ind)

            actual_time = game_clock_time[np.argmax(shot_clock_time)]
            quarter = movement_around_rebound.loc[:, 'quarter'].values[0]
            movement_around_rebound = movement_around_rebound.loc[movement_around_rebound.game_clock == actual_time, :]

            rebound['QUARTER'] = quarter
            rebound['REBOUND_TEAM'] = rebound['PLAYER1_TEAM_ID']
            rebound['SHOT_TEAM'] = shot_event['PLAYER1_TEAM_ID']
            rebound['REBOUND_PLAYER'] = rebound['PLAYER1_ID']
            rebound['SHOT_PLAYER'] = shot_event['PLAYER1_ID']
            rebound['REBOUND_TIME'] = actual_time
            rebound['RIM_TIME'] = rim_time
            rebound['SHOT_TIME'] = shot_time
            rebound['LOC_X'] = movement_around_rebound.loc[movement_around_rebound.team_id == -1, 'x_loc'].values[0]
            rebound['LOC_Y'] = movement_around_rebound.loc[movement_around_rebound.team_id == -1, 'y_loc'].values[0]
            rebound['GAME_ID_STR'] = '00' + str(int(rebound['GAME_ID']))

        except Exception as err:
            continue

        fixed_rebounds = fixed_rebounds.append(rebound)

    return fixed_rebounds

if __name__ == '__main__':
    game_dir = CONFIG.data.movement.dir
    event_dir = CONFIG.data.events.dir

    games = utils.get_games()
    events = utils.get_events(event_dir, games)
    rebounds = load_rebounds(events)
    fixed_rebounds = pd.DataFrame(columns=rebounds.columns)

    for game in tqdm(games):
        game_id = int(game)
        game_movement = pd.read_csv('%s/%s_converted.csv' % (game_dir, game))
        game_rebounds = rebounds.loc[rebounds.GAME_ID == game_id, :]
        game_events = events.loc[events.GAME_ID == game_id, :]
        fixed_rebounds = fixed_rebounds.append(correct_rebounds(game_rebounds, game_movement, game_events))

    fixed_rebounds.to_csv('%s/%s.csv' % (CONFIG.data.rebounds.dir, 'rebounds'), index=False)
