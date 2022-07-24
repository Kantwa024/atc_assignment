import atcSimulator.main_class as main_class

code = main_class.ATC("PUNE", 5, 10)
    
def test_check_name():
    assert code.airport_name == "PUNE"

def test_check_runways_cnt():
    assert code.runways_cnt == 5

def test_add_runways():
    code.runways_cnt = 10
    code.add_runways()
    assert len(code.runways.keys()) == 10

def test_add_runway():
    code.runways_cnt = 10
    code.add_runways()
    code.add_runway(code.available_runways()[0])
    assert len(code.available_runways()) == 9

def test_remove_runway():
    code.runways_cnt = 10
    code.add_runways()
    code.add_runway(code.available_runways()[0])
    code.add_runway(code.available_runways()[0])
    code.remove_runway(code.on_runway_aircrafts()[0])
    assert len(code.available_runways()) == 9

def test_add_random_aircrafts():
    code.add_random_aircraft(1000)
    assert len(code.aircrafts.keys()) == 1000

def test_remove_land_time():
    code.landing_time = {}
    code.landing_time[1] = 123
    code.landing_time[2] = 567
    code.landing_time[3] = 561
    del code.landing_time[3]
    assert code.landing_time[2] == 567
    assert len(code.landing_time.keys()) == 2
    assert code.landing_time.get(3) == None

def test_remove_aircraft():
    code.aircrafts = {}
    code.add_random_aircraft(1000)
    del code.aircrafts[list(code.aircrafts.keys())[0]]
    assert len(code.aircrafts.keys()) == 999

def test_run_priority_indexing():
    code.aircrafts = {}
    code.add_aircraft(1234, 100, 200, 1, 10, -1)
    code.add_aircraft(1921, 70, 200, 1, 10, -1)
    code.add_aircraft(1234, 150, 200, 2, 10, -1)
    assert code.run_priority_indexing()[0][0] == 1921

def test_update_runway_time():
    code.aircrafts = {}
    code.add_aircraft(1234, 100, 200, 1, 10, -1)
    code.add_aircraft(1921, 70, 200, 1, 10, 1)
    code.add_aircraft(1234, 150, 200, 2, 10, -1)
    code.update_runway_time(1)
    assert code.aircrafts[1921][-2] == 9

def test_aircraft_exist():
    code.aircrafts = {}
    code.add_aircraft(1234, 100, 200, 1, 10, -1)
    code.add_aircraft(1921, 70, 200, 1, 10, 1)
    code.add_aircraft(1234, 150, 200, 2, 10, -1)
    assert code.aircraft_exist(1234) == True
    assert code.aircraft_exist(9999) == False

def test_check_add_input_format():
    assert code.check_add_input_format(1234, 120.22, 120, 1.2, 10, 1) == True

def test_on_runway_aircrafts():
    code.runways_cnt = 10
    code.add_runways()
    code.aircrafts = {}
    code.add_aircraft(1234, 100, 200, 1, 10, -1)
    code.add_aircraft(1921, 70, 200, 1, 10, -1)
    code.add_aircraft(1234, 150, 200, 2, 10, -1)
    code.do_landing(1234)
    assert len(code.available_runways()) == 9
    assert len(code.on_runway_aircrafts()) == 1
    assert code.is_runway_available(code.on_runway_aircrafts()[0]) == False











