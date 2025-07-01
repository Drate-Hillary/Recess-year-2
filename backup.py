import os
import shutil
import time

source_folder = r"C:\Users\HP\Downloads\automations"
backup_folder = r"C:\Users\HP\Downloads\automations_backup" 

if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

now = time.time()
three_mins = 1 * 60

for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    if os.path.isfile(file_path):
        mins = os.path.getmtime(file_path)

        if now - mins <= three_mins:
            backup_path = os.path.join(backup_folder, filename)
            shutil.copy2(file_path, backup_path)

            print(f"Backed up: {filename}")