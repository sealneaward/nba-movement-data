import pandas as pd
import os
from tqdm import tqdm

import movement.config as CONFIG

def half_full_to_half(data):
    """
    Convert single half court movement to shot log dimensional movement

    Parameters
    ----------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that is converted to
        a single half court (x_loc < 47)

    Returns
    -------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that is converted
        to the single shooting court that follows shot log dimensions
        (-250-250, -47.5-422.5)
    """
    # convert to half court scale
    # note the x_loc and the y_loc are switched in shot charts from movement data (charts are perpendicular)
    data['x_loc_copy'] = data['x_loc']
    data['y_loc_copy'] = data['y_loc']

    # Range conversion formula
    # http://math.stackexchange.com/questions/43698/range-scaling-problem

    data['x_loc'] = data['y_loc_copy'].apply(lambda y: 250 * (1 - (y - 0)/(50 - 0)) + -250 * ((y - 0)/(50 - 0)))
    data['y_loc'] = data['x_loc_copy'].apply(lambda x: -47.5 * (1 - (x - 0)/(47 - 0)) + 422.5 * ((x - 0)/(47 - 0)))
    data = data.drop(['x_loc_copy', 'y_loc_copy'], axis=1, inplace=False)

    return data


def full_to_half_full(data):
    """
    Convert full court movement to a single half court

    Parameters
    ----------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that covers the entire court

    Returns
    -------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that
        is converted to a single half court (x_loc < 47)
    """

    # first force all points above 47 to their half court counterparts
    # keep all original points for furhter limitations to single court
    data['x_loc_original'] = data['x_loc']
    data['y_loc_original'] = data['y_loc']
    data.loc[data.x_loc > 47,'y_loc'] = data.loc[data.x_loc > 47, 'y_loc'].apply(lambda y: 50 - y)
    data.loc[data.x_loc > 47,'x_loc'] = data.loc[data.x_loc > 47, 'x_loc'].apply(lambda x: 94 - x)

    return data

if __name__ == "__main__":
    csv_dir = CONFIG.data.movement.dir
    converted_dir = CONFIG.data.movement.converted.dir
    if not os.path.exists(converted_dir):
        os.makedirs(converted_dir)

    games = os.listdir(csv_dir)
    converted_games = os.listdir(csv_dir)

    for game in tqdm(games):
        # convert full court movement data to half court range seen in shot log data
        game = game.split('.')[0]
        converted_game = '%s_converted.csv'

        if converted_game in converted_games:
            continue
        else:
            data = pd.read_csv('%s/%s.csv' % (csv_dir, str(game)))
            data = full_to_half_full(data)
            data = half_full_to_half(data)
            data.to_csv('%s/%s_converted.csv' % (converted_dir, str(game)), index=False)
