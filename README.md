# PICMathSubway FEC Data Collection Scheduler
This is the repository of PICMathSubway group in Spring 2020 at NYU. The project includes an automatic scheduler of Fare Evasion Control Data Collection for MTA.

## Required Packages
`numpy`, `pandas`, `tqdm`, `pickle`, `scipy`.

## Required Data
1. File of the base sample tasks `base_file`.
2. File of all stations `station_file`.
3. File of locations of all FECs `location_file`.
4. File of available checkers `checker_file`.
5. File of special sample tasks `special_file`.

## Graph Generation
Before running the following command, OTP server must be running on port 8080 (if not available you need to edit the code in `gate.py` function `extract_travel_time`).

You need to also edit file `constants.py` variable `DATE` to the corresponding date to be scheduled.

Then run the following command to generate the three graphs:
`python3 read_tasks.py -f base_file -i station_file -s location_file -c checker_file -p special_file`

The function `read` in `read_tasks.py` will return the three graphs for weekdays, Saturday, and Sunday. Meanwhile, the three graphs will be pickled and saved as `wkd_save.pkd`, `sat_save.pkl`, and `sun_save.pkl`

## Schedule Generation

### Weekly Schedule

### Monthly Schedule

### Failed Tasks


## Acknowledgement
