import os
# change this data_dir for personal path
if os.environ['HOME'] == '/home/neil':
    data_dir = '/home/neil/projects/nba-movement-data'
else:
    raise Exception("Unspecified data_dir, unknown environment")