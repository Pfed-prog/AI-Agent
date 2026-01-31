import os

directory_path = 'c:/Users/fedor/Downloads/'

most_recent_file = None
most_recent_time = 0


# iterate over the files in the directory using os.scandir
for entry in os.scandir(directory_path):
    if entry.is_file():
        # get the modification time of the file using entry.stat().st_mtime_ns
        mod_time = entry.stat().st_mtime_ns
        if mod_time > most_recent_time:
            # update the most recent file and its modification time
            most_recent_file = entry.name
            most_recent_time = mod_time

print(most_recent_file)