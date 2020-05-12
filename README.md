# PICMathSubway FEC Data Collection Scheduler
This is the repository of PICMathSubway group in Spring 2020 at NYU. The project includes an automatic scheduler of Fare Evasion Control Data Collection for MTA.

## Required Packages
`numpy`, `pandas`, `tqdm`, `pickle`, `scipy`, `xlwt`, `random`.

## Required Data
1. Excel file of the base sample tasks `base_file`.
2. Excel file of all stations `station_file`.
3. CSV file of locations of all FECs `location_file`.
4. Excel file of available checkers `checker_file`.
5. Excel file of special sample tasks `special_file`.

## Graph Generation
Before running the following command, OTP server must be running on port 8080 (if not available you need to edit the code in `gate.py` function `extract_travel_time`).

You need to also edit file `constants.py` variable `DATE` to the corresponding date to be scheduled.

Then run the following command to generate the three graphs:
`python3 read_tasks.py -f base_file -i station_file -s location_file -c checker_file -p special_file`

Or you can call the function `read` in `read_tasks.py` which will return the three graphs for weekdays, Saturday, and Sunday. Meanwhile, the three graphs will be pickled and saved as `wkd_save.pkd`, `sat_save.pkl`, and `sun_save.pkl`

## Schedule Generation

### Weekly Schedule
To generate a weekly schedule for all the checkers run the function `week_bfs_forall` in `BFS.py`. This function returns an array of `WeekSchedules`, one `WeekSchedule` for each checker, an array of the three modifies graphs, and an array of the simulated failed tasks.

### Monthly Schedule
To generate a monthly schedule for all the checkers run `BFS.py`. This will produce four excel files, one for each week of the month, with weekly schedules for each checker sperated by sheets.

### Failed Tasks
To simulate failed tasks for testing purposes, inside the function `month_bfs_forall` in `BFS.py` there is a call to the function `failed_tasks_to_excel1` and `failed_tasks_to_excel2` which generates the excel files for incomplete tasks from the first and second week respectively.

Then the function `read_failed_tasks` in `month_bfs_forall` reads the excel files with the failed tasks and reinserts these tasks into the current graph.

### Special Samples
The function `week_bfs_forall` in `BFS.py` inserts special samples into sparse layers of the graph three times a week, depending on the number of checkers, while generating weekly schedules, 

## Acknowledgement
PIC Math is a program of the Mathematical Association of America (MAA). Support for this MAA program is provided by the National Science Foundation (NSF grant DMS-1722275) and the National Security Agency (NSA).

We would like to thank our industry partner, the MTA for working with us this semester. We would also like to thank Eric Jensen, Acting Manager, and Timon Stasko, Manager of Operations Research, for attending our biweekly presentations and giving us thoughtful feedback.

Special thanks to our professor Vindya Bhat and our TA Xinment Li for being the scrum masters for this project and guiding us this semester.
