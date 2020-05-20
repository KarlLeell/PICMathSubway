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

### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    checker_shift_start : TODO

    full_time=True : TODO

    weights=[] : TODO

    sp=0.01 : TODO

    lapse_rate=0 : TODO

    pruning_threshold=float('inf') : TODO

    mu=0.0 : TODO

    sigma=1.0 : TODO

### class Node(Gate):


#### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    gate : TODO

### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    gate : TODO

#### def calc_dist_priority

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    child_idx : TODO

### def calc_dist_priority

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

### def remove_child

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

### def heuristic_value

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
    result>0 : TODO

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

### def __init__

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

### def print

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

### def __init__

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

### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

## gate.py

### class Gate(Station):


#### def __repr__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def __repr__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

##### OUTPUTS
    self.name : TODO

#### def __str__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def __str__

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

    task_matrix : TODO

    1) : TODO

### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    name='' : TODO

    sample_id='' : TODO

    loc=None : TODO

    boro='' : TODO

    routes=None : TODO

    
booth_id='' : TODO

    begin_time=0 : TODO

    task_matrix=np.zeros((24*12 : TODO

    1) : TODO

#### def find_neighbors

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def find_neighbors

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

### def calc_travel_time

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

### def extract_travel_time

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    dst_gate : TODO

    date : TODO

### def 1="""'http://localhost:8080/otp/routers/default/plan?fromPlace="""
str2="""&toPlace="""
str3="""&time=1:02pm&date="""
str4="""&mode=TRANSIT,WALK&maxWalkDistance=500&arriveBy=false'"""
loc1=str

TODO: fill in the function explanation here

##### INPUTS

    self.loc)[1:-1].replace('' : TODO

    '' : TODO

##### OUTPUTS
    distance : TODO

#### def calc_abs_dist

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    dst_gate : TODO

### def calc_abs_dist

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

### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def print_station

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def print_station

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

## performance_measure.py

### def efficiency

TODO: fill in the function explanation here

##### INPUTS

     : TODO

### def completion

TODO: fill in the function explanation here

##### INPUTS

    total_tasks : TODO

    total_special_tasks : TODO

## read_checkers.py

### def read_checkers

TODO: fill in the function explanation here

##### INPUTS

    path : TODO

##### OUTPUTS
    '''salistofcheckers''' : TODO

##### OUTPUTS
    checkers : TODO

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

### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    name='' : TODO

    booth_id='' : TODO

    loc=None : TODO

    boro='' : TODO

    routes=None : TODO

#### def abs_loc

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def abs_loc

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

##### OUTPUTS
    self.loc : TODO

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

### def set_station

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    name='' : TODO

    booth_id='' : TODO

    loc=[0 : TODO

    0] : TODO

    boro='' : TODO

    routes=[] : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def print

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

### def __init__

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    day=constants.DAY[0] : TODO

    graph_type=constants.GRAPH_TYPE[0] : TODO

#### def naive_init

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def naive_init

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def fine_init

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def fine_init

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def add_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

### def add_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

#### def naive_add

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

### def naive_add

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

#### def fine_add

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

### def fine_add

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

#### def fine_add_aux

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex : TODO

### def fine_add_aux

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

### def find_vertex

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

### def delete_vertex

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

    vertex=None : TODO

    booth_id='' : TODO

    begin_time=0 : TODO

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

### def naive_del_vertex

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

### def fine_del_vertex

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

### def normalize_distance_priority

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def normalize_availability_priority

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def normalize_availability_priority

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def sparsity_check

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def sparsity_check

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

### def add_special_task

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

### def add_special_sample

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

#### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

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

### def __init__

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

### def print

TODO: fill in the function explanation here

##### INPUTS

    self : TODO

