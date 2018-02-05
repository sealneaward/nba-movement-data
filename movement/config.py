from _config_section import ConfigSection

import os
from movement.constant import data_dir

REAL_PATH = data_dir

data = ConfigSection("data")
data.dir = "%s/%s" % (REAL_PATH, "data")

data.movement = ConfigSection("movement data")
data.movement.dir = "%s/%s" % (data.dir, "csv")

data.movement.converted = ConfigSection("movement data")
data.movement.converted.dir = "%s/%s" % (data.dir, "converted")

data.events = ConfigSection("event information data")
data.events.dir = "%s/%s" % (data.dir, "events")

data.shots = ConfigSection("shot information data")
data.shots.dir = "%s/%s" % (data.dir, "shots")

