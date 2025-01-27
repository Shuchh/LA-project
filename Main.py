#this script is for try and simulate a log analyzer for J35 printers.
import os
import re
#first part of the code is for opening all the unified logs file by date order (from old to new) and merge them into one file.
directory = r"\\objet-data\R&D DATA\Shachar Gabay\CPE Projects\Reliabilty\L.A project\Logs"

#open all the unified logs (.log files) in an array from path.
def find_unified_logs_from_path(directory):
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

# the 2nd part of the code is for scanning each of the sorted files in the array and search for job names and print windows (meaning date, start time, and end time) each job will be saved in an array of dictionaries.
def find_print_windows(files):
    results=[]
    pattern = r"\s*job name:\s*(.*?)\s*ID:" # for finding full job name with spaces and all
    id_pattern = r"\s*ID:\s*(.*?)\s*Total slices:"
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if "Sending PrintPrepare" in line:
                    parts=line.split()
                    next_line=next(f,None) # job name is in the next line
                    match = re.search(pattern, next_line, re.IGNORECASE) # finding the job name
                    id_match = re.search(id_pattern, next_line, re.IGNORECASE) # finding the job ID
                    if match:
                       job_name = match.group(1)  # keeps the job name
                    else:
                       job_name = "no job name found"
                       print("job name:",job_name)
                    if "C:\Program Files\Stratasys" in next_line or "C:/Program Files/Stratasys" in next_line: # from wizards, keeps only DNT's and MRW's
                        if "DynamicNozzleTests\WithRoller" in next_line:
                            job_name = "DynamicNozzleTests WithRoller"
                        elif "DynamicNozzleTests\WithoutRoller" in next_line:
                            job_name = "DynamicNozzleTests WithoutRoller"
                        elif "MRW" in next_line:   
                            job_name = "MRW"  
                        else:
                            break 
                    if id_match:
                        job_id = id_match.group(1)  # keeps the job ID
                    print("Job data:", job_name, job_id)       
                    results.append({"file":file, "date":parts[1], "start time":parts[2], "job name":job_name, "job_id":job_id})       
    return results                
                


#running the progrem
log_files = find_unified_logs_from_path(directory)
sorted_files=sort_unified_logs_by_date(log_files)
find_print_windows(sorted_files)


