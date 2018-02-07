import pandas as pd
from os import listdir
from os.path import isfile, join, exists
import re

import movement.config as CONFIG


def convert_time(minutes, seconds):
    new_times = []
    for ind in range(len(minutes)):
        m, s = minutes[ind], seconds[ind]
        time = int(m) * 60 + int(s)
        new_times.append(time)

    return new_times


def get_events(event_dir, games):
    """
    Loads game events CSV files and returns a single event file

    Parameters
    ----------
    dirs: str list

    Returns
    -------
    names: str list
        game ids
    """
    events = pd.DataFrame

    # go through each game and get events
    for game in games:
        if events.empty:
            events = pd.read_csv('%s/%s.csv' % (event_dir, game))
        else:
            game_events = pd.read_csv('%s/%s.csv' % (event_dir, game))
            events.append(game_events)

    events['GAME_ID'] = '00' + events['GAME_ID'].astype(int).astype(str)

    return events


def get_games():
    """
    Loads game movements CSV files and returns list of games to get event descriptions from
    """
    # Try converted directory..maybe user removed csv directory to free up memory
    potential_game_dirs = [CONFIG.data.movement.dir]
    names = []
    for path in potential_game_dirs:
        if exists(path):
            for f in listdir(path):
                if isfile(join(path, f)):
                    m = re.match(r'\d+', f)
                    names.append(m.string[m.start() : m.end()])
    if len(names) > 0:
        return names

    print('No games found.')
    return names


def get_converted_games():
    """
    Loads converted game movements CSV files and returns list of games to get event descriptions from
    """
    # Try converted directory..maybe user removed csv directory to free up memory
    potential_game_dirs = [CONFIG.data.movement.converted.dir]
    names = []
    for path in potential_game_dirs:
        if exists(path):
            for f in listdir(path):
                if isfile(join(path, f)):
                    m = re.match(r'\d+', f)
                    names.append(m.string[m.start() : m.end()])
    if len(names) > 0:
        return names

    print('No games found.')
    return names
