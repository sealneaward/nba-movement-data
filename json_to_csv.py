import pandas
import os
import sys
import json

data_path = sys.path[0] + '/data/'
csv_path = data_path + 'csv'
files = os.listdir(data_path)

if not os.path.exists(csv_path):
    os.makedirs(csv_path)

count = 0
movement_headers = ["team_id", "player_id", "x_loc", "y_loc", "radius", "game_clock", "shot_clock", "game_id",
                    "event_id"]
for file in files:
    if '.json' not in file:
        continue
    try:
        count = count + 1
        file_data = open(data_path + file)
        game_id = file.replace('.json', '')
        data = json.load(file_data)
        events = data['events']
        moments = []

        for event in events:
            event_id = event['eventId']
            movement_data = event['moments']
            for moment in movement_data:
                for player in moment[5]:
                    player.extend((moment[2], moment[3], game_id, event_id))
                    moments.append(player)

        # movement frame is complete for game
        movement = pandas.DataFrame(moments, columns=movement_headers)
        movement.to_csv('./data/csv/' + game_id + '.csv', index=False)
        # movement.to_json('./data/json/' + game_id + '.json', orient='records')

        print '\n'
        print '\n'
        print 'Finished collecting dataframe for Game ID: ' + game_id
        print 'Completed : ' + str(count) + ' games.'
    except Exception as e:
        print 'Error in loading: ' + str(file) + ' file, Error: ' + str(e)

print '\n'
print '\n'
print 'Finished collecting dataframes for all games.'
print str(count) + ' games counted'
