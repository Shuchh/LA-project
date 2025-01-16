#this script is for try and simulate a log analyzer for J35 printers.
import os
#first part of the code is for opening all the unified logs file by date order (from old to new) and merge them into one file.
directory = r"\\objet-data\R&D DATA\Shachar Gabay\CPE Projects\Reliabilty\L.A project\Logs"

#open all the unified logs (.log files) in an array from path.
def find_unified_logs_from_path():
    files = [
      os.path.join(directory,f)
      for f in os.listdir(directory)
      if os.path.isfile(os.path.join(directory,f)) and f.endswith(".log")
       and "slice2travels" not in f.lower()
    ]
    return files

#sort all the files in the array by date (from old to new).
def sort_unified_logs_by_date(files):
    files.sort(key=os.path.getmtime)
    return files

#the 2nd part of the code is for scanning each of the sorted files in the array and search for job names and print windows (meaning date, start time, and end time) each job will be saved in an array of dictionaries.
def find_print_windows(files):
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if "Sending PrintPrepare" in line:
                    print(line)
