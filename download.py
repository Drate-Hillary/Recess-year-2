import os
import shutil

download_folder = r"C:\Users\HP\Downloads\automations"

folders={
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'videos': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav', '.flac'],
    'archives': ['.zip', '.rar', '.tar'],
    'scripts': ['.py', '.sh', '.js'],
    'installers': ['.exe', '.msi'],
    'others': []
}

for folder in folders:
    folder_path = os.path.join(download_folder, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

for filename in os.listdir(download_folder):
    file_path = os.path.join(download_folder, filename)

    if os.path.isdir(file_path):
        continue

for folder, extension in folders.items():
    if any(filename.lower().endswith(ext) for ext in extension):
        targetFolder = os.path.join(download_folder, folder)
        shutil.move(file_path, targetFolder)

        print(f"{filename} in {targetFolder}")
