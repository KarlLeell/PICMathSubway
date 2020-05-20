## BFS.py

### class Params:


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    checker_shift_start : TODO

    full_time : TODO

    weights : TODO

    sp : TODO

    lapse_rate : TODO

    pruning_threshold : TODO

    mu : TODO

    sigma : TODO

### class Node(Gate):


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    gate : TODO

#### def calc_dist_priority

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    child_idx : TODO

##### OUTPUTS
    self.dist_priority_list[child_idx] : TODO

#### def remove_child

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    n : TODO

#### def heuristic_value

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    parent_node : TODO

    idx : TODO

##### OUTPUTS
    self.value : TODO

### def Lapse

TODO: fill in the function explanation here

##### INPUTS

    probability : TODO

##### OUTPUTS
    '''truewithacertainprobability''' : TODO

##### OUTPUTS
    random.random()<probability : TODO

### def Stop

TODO: fill in the function explanation here

##### INPUTS

    probability : TODO

##### OUTPUTS
    '''truewithacertainprobability''' : TODO

##### OUTPUTS
    random.random()<probability : TODO

### def InitializeChildren

TODO: fill in the function explanation here

##### INPUTS

    node : TODO

    cumm_delay : TODO

    params : TODO

##### OUTPUTS
    node.children : TODO

##### OUTPUTS
    print('\t\t\tviabletotoLIC') : TODO

##### OUTPUTS
    node.children : TODO

### def CheckLicDist

TODO: fill in the function explanation here

##### INPUTS

    gate : TODO

    cumm_delay : TODO

    params : TODO

    extra_time=0 : TODO

##### OUTPUTS
    result>=0 : TODO

### def SelectNode

TODO: fill in the function explanation here

##### INPUTS

    root : TODO

##### OUTPUTS
    '''theleafnodealongthemostpromisingbranch''' : TODO

##### OUTPUTS
    n : TODO

    cumm_delay : TODO

### def ExpandNode

TODO: fill in the function explanation here

##### INPUTS

    node : TODO

    cumm_delay : TODO

    params : TODO

##### OUTPUTS
     : TODO

### def Backpropagate

TODO: fill in the function explanation here

##### INPUTS

    node : TODO

    root : TODO

    value : TODO

##### OUTPUTS
    PathAverage(node.parent : TODO

    root : TODO

    pathsum : TODO

    counter) : TODO

##### OUTPUTS
    pathsum/counter : TODO

### def ArgmaxChild

TODO: fill in the function explanation here

##### INPUTS

    node : TODO

##### OUTPUTS
    '''thechildwithmaxvalue''' : TODO

##### OUTPUTS
    random.choice([iforiinnode.childrenifi.value==maxvalue]) : TODO

### def MakeMove

TODO: fill in the function explanation here

##### INPUTS

    root : TODO

    params : TODO

##### OUTPUTS
    ArgmaxChild(root) : TODO

### def print_decision_path

TODO: fill in the function explanation here

##### INPUTS

    node : TODO

    root : TODO

    verbose=False : TODO

##### OUTPUTS
    print('toLIC') : TODO

##### OUTPUTS
    nodes : TODO

    delay_array : TODO

    travel_time_array : TODO

### def make_gate_array

TODO: fill in the function explanation here

##### INPUTS

    root : TODO

##### OUTPUTS
    gate_array : TODO

### def get_value

TODO: fill in the function explanation here

##### INPUTS

    node : TODO

##### OUTPUTS
    value : TODO

### def delete_nodes

TODO: fill in the function explanation here

##### INPUTS

    nodes : TODO

    graph : TODO

    verbose=False : TODO

##### OUTPUTS
    graph : TODO

##### OUTPUTS
    print('\n\n----------------') : TODO

##### OUTPUTS
    [wkd_graph : TODO

    sat_graph : TODO

    sun_graph] : TODO

    WeekSchedule(checker : TODO

    start_time : TODO

    start_time+duration : TODO

    ds_array : TODO

    ) : TODO

##### OUTPUTS
    wks_forall : TODO

    graphs : TODO

    failed_tasks : TODO

### def failed_tasks_to_excel_1

TODO: fill in the function explanation here

##### INPUTS

    failed_tasks : TODO

##### OUTPUTS
    "failed_tasks_1.xlsx" : TODO

### def failed_tasks_to_excel_2

TODO: fill in the function explanation here

##### INPUTS

    failed_tasks : TODO

##### OUTPUTS
    "failed_tasks_2.xlsx" : TODO

##### OUTPUTS
    month_forall : TODO

    failed_tasks_month : TODO

### def print_schedule

TODO: fill in the function explanation here

##### INPUTS

    month_forall : TODO

    filename : TODO

## checker.py

### class Checker:


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    name : TODO

    shift_start : TODO

    shift_end : TODO

    ft_work_status : TODO

    rdo : TODO

    working_days : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

## constants.py

## DaySchedule.py

### class DaySchedule:


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    checker : TODO

    day : TODO

    shift_start : TODO

    shift_end : TODO

    gate_array : TODO

    delay_array : TODO

    travel_time_array : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

## gate.py

### class Gate(Station):


#### def __repr__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

##### OUTPUTS
    self.name : TODO

#### def __str__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

##### OUTPUTS
    self.name : TODO

#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    name : TODO

    sample_id : TODO

    loc : TODO

    boro : TODO

    routes : TODO

    
booth_id : TODO

    begin_time : TODO

    day : TODO

    neighbors : TODO

    
edge_dist_tt : TODO

    dist_prio : TODO

    comments : TODO

    dummy_value : TODO

    
availability_priority_holder : TODO

    availability_priority : TODO

    
task_type : TODO

#### def find_neighbors

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

##### OUTPUTS
    self.neighbors : TODO

#### def calc_travel_time

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    dst_gate : TODO

##### OUTPUTS
    0 : TODO

##### OUTPUTS
    dist : TODO

#### def extract_travel_time

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    dst_gate : TODO

    date : TODO

### def 1="""'http://localhost:8080/otp/routers/default/plan?fromPlace="""
str2="""&toPlace="""
str3="""&time="""
#x:xam/pm
am_pm='am'if

TODO: fill in the function explanation here

##### INPUTS

    self.begin_time+1 : TODO

##### OUTPUTS
    distance : TODO

#### def calc_abs_dist

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    dst_gate : TODO

##### OUTPUTS
    d : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def print_station

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

## performance_measure.py

### def efficiency

This function measures how efficient a monthly schedule is. It reads the monthly schedule and then calculates and prints out the following figures:
-total working hours
-total checking hours
-working efficiency (total checking hours / total working hours)

##### INPUTS

     

### def completion

This function reads a monthly schedule, calculates how many tasks of each type are completed and prints out the following:
-base tasks completed
-proportion of base sample completed
-rescheduled tasks completed
-proportion of rescheduled tasks completed
-special tasks completed
-proportion of special tasks completed

##### INPUTS

    total_tasks : number of tasks in base sample

    total_special_tasks : number of tasks in special sample

## read_checkers.py

### def read_checkers

TODO: fill in the function explanation here

##### INPUTS

    path : TODO

##### OUTPUTS
    '''salistofcheckers''' : TODO

##### OUTPUTS
    checkers : TODO

### def ser.add_argument

TODO: fill in the function explanation here

##### INPUTS

    '-f' : TODO

    '--file_loc' : TODO

    default='NYCTFERequiredData/FECheckerlist.xlsx' : TODO

    type=str : TODO

## read_tasks.py

### def read

TODO: fill in the function explanation here

##### INPUTS

    path : TODO

##### OUTPUTS
    wkd_graph : TODO

    sat_graph : TODO

    sun_graph : TODO

### def read_failed_tasks

TODO: fill in the function explanation here

##### INPUTS

    graph : TODO

    file_name : TODO

### def ser.add_argument

TODO: fill in the function explanation here

##### INPUTS

    '-f' : TODO

    '--file_loc' : TODO

    default='NYCTFERequiredData/SFESAMPLE210.xlsx' : TODO

    type=str : TODO

### def ser.add_argument

TODO: fill in the function explanation here

##### INPUTS

    '-s' : TODO

    '--station_loc' : TODO

    default='NYCTFERequiredData/station_location.csv' : TODO

    type=str : TODO

### def ser.add_argument

TODO: fill in the function explanation here

##### INPUTS

    '-i' : TODO

    '--station_id' : TODO

    default='NYCTFERequiredData/ListofStationsandFCAs_v2.xlsx' : TODO

    type=str : TODO

### def ser.add_argument

TODO: fill in the function explanation here

##### INPUTS

    '-c' : TODO

    '--checker_schedule' : TODO

    default='NYCTFERequiredData/FECheckerListASSIGNED.xlsx' : TODO

    type=str : TODO

### def ser.add_argument

TODO: fill in the function explanation here

##### INPUTS

    '-p' : TODO

    '--special' : TODO

    default='NYCTFERequiredData/SFESpecialAM-PM.xlsx' : TODO

    type=str : TODO

## station.py

### class Station:


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    name : TODO

    booth_id : TODO

    loc : TODO

    boro : TODO

    routes : TODO

#### def abs_loc

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

##### OUTPUTS
    [float(i)foriinself.loc] : TODO

##### OUTPUTS
    [0 : TODO

    0] : TODO

#### def set_station

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    name : TODO

    booth_id : TODO

    loc : TODO

    0] : TODO

    boro : TODO

    routes : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

## subway_graph.py

### class Graph():


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    day : TODO

    graph_type : TODO

#### def naive_init

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def fine_init

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def add_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

#### def naive_add

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

#### def fine_add

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

#### def fine_add_aux

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

#### def find_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    booth_id : TODO

    begin_time : TODO

##### OUTPUTS
    vertex : TODO

##### OUTPUTS
    None : TODO

#### def delete_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

    booth_id : TODO

    begin_time : TODO

##### OUTPUTS
    False : TODO

##### OUTPUTS
    False : TODO

##### OUTPUTS
    self.naive_del_vertex(vertex) : TODO

##### OUTPUTS
    self.fine_del_vertex(vertex) : TODO

#### def naive_del_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

##### OUTPUTS
    True : TODO

#### def fine_del_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

##### OUTPUTS
    True : TODO

#### def normalize_distance_priority

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def normalize_availability_priority

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def sparsity_check

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

##### OUTPUTS
    sparse_indices : TODO

#### def add_special_task

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    layer : TODO

##### OUTPUTS
    None : TODO

##### OUTPUTS
    None : TODO

#### def add_special_sample

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

## testStation.py

### def main

TODO: fill in the function explanation here

##### INPUTS

    args : TODO

### def ser.add_argument

TODO: fill in the function explanation here

##### INPUTS

    'file_loc' : TODO

    type=str : TODO

    default='NYCTFERequiredData/ListofStationsandFCAs.xlsx' : TODO

## travel_time_book_generator.py

### def generate

TODO: fill in the function explanation here

##### INPUTS

     : TODO

## WeekSchedule.py

### class WeekSchedule:


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    checker : TODO

    shift_start : TODO

    shift_end : TODO

    DaySchedule_array : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

