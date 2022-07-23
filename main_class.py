from cmath import inf
from hashlib import new
from sys import flags
import time
import random
from beautifultable import BeautifulTable
import threading
from datetime import datetime
import database

class ATC:
    def __init__(self, airport_name, runways_cnt, emergency_fuel_limit):
        if isinstance(runways_cnt, int):
            self.airport_name = airport_name
            self.runways_cnt = runways_cnt
            self.aircrafts = {}
            self.runways = {}
            self.landing_time = {}
            self.landing_time_str = {}
            self.emergency_fuel_limit = emergency_fuel_limit
            self.aircrafts_data_list = []
            self.successfully_land = 0
            self.database = database.Database()

            self.add_runways()
            print("Welocome to "+ str(airport_name)+ " airport")
            print()
            print("All functions name")
            table = BeautifulTable()
            fun_lst = [["add_runways", "None", "Add all the runways in hash table"],
            ["add_runway", "Runway Number", "True if there is any aircraft"],
            ["remove_runway", "Runway Number", "Change True in False"],
            ["do_landing", "Aircraft Id", "Change the runway number from 0 to somethin else"],
            ["add_random_aircraft", "Count", "Add random aircraft details"],
            ["add_aircraft", "Id, Fuel, Passengers, Burning Rate, Runway Time, Runway Number", "Add aircraft details"],
            ["remove_aircraft", "Aircraft Id", "Remove aircraft details"],
            ["run_priority_indexing", "None", "Arrange aircraft according to risk"],
            ["show_information", "None", "Show aircrafts details in a table"],
            ["run_tick", "Delay", "Run simulation automatically for infinite time"],
            ["aircraft_exist", "Aircraft Id", "True if aircraft in database"],
            ["check_add_input_format","Id, Fuel, Passengers, Burning Rate, Runway Time, Runway Number", "True if format is right"],
            ["on_runway_aircrafts", "None", "List of busy runways"],
            ["available_runways", "None", "List of available runways"],
            ["is_runway_available", "Runway Number", "True if runway available"],
            ["check_emergency", "List", "Input is a list of aircraft details, emergency landing"],
            ["del_emergency_landing", "None", "Delete aircraft using runway time"],
            ["update_runway_time", "Tick", "Decrease runway time by tick value"],
            ["run_tick_thread", "Tick", "Run task in background"]]
            
            fun_lst.sort(key=lambda x: x[0])
            for i in fun_lst:
                table.rows.append(i)
            table.rows.header = [str(i) for i in range(1, len(fun_lst)+1)]
            table.columns.header = ["Function Name", "Inputs", "Information"]
            print(table)
        else:
            raise Exception("Please check the runway number format")

    def add_runways(self):
        for i in range(1, self.runways_cnt+1):
            self.runways[i] = False

    def do_landing(self, id):
        if isinstance(id, int):
            lst = self.available_runways()
            if len(lst) != 0 and id not in self.landing_time:
                self.aircrafts[id][4] = lst[0]
                self.add_runway(lst[0])
                self.landing_time[id] = time.time()
                self.landing_time_str[id] = datetime.now()
            else:
                print("No runway available")
        else:
            raise Exception("Please check the id format")

    def add_runway(self, number):
        if isinstance(number, int):
            self.runways[number] = True
            return list(self.runways.keys())
        else:
            raise Exception("Please check the runway number format")

    def remove_runway(self, number):
        if isinstance(number, int):
            if number in self.runways:
                self.runways[number] = False
                return True
            else:
                return False
        else:
            raise Exception("Please check the runway number format")

    def add_random_aircraft(self, cnt):
        if isinstance(cnt, int):
            while cnt > 0:
                id = random.randint(1000,9999)
                fuel = round(random.uniform(200.0, 500.0),2)
                passengers = random.randint(10, 300)
                burning_rate = round(random.uniform(1.0, 3.0),2)
                runway_time = random.randint(5,10)

                while id in self.aircrafts:
                    id = random.randint(1000,9999)

                self.aircrafts[id] = [fuel, burning_rate, passengers, runway_time, -1]
                cnt -= 1
        else:
            raise Exception("Please check the count format")

    # aricraft[id] = [fuel, burning_rate, passengers, runway_time, runway_number]
    def add_aircraft(self, id, fuel, passengers, burning_rate, runway_time, runway_number = -1):
        if self.check_add_input_format(id, fuel, passengers, burning_rate, runway_time, runway_number):
            self.aircrafts[id] = [fuel, burning_rate, passengers, runway_time, runway_number]
            return self.aircrafts
        else:
            raise Exception("Please check the input format")

    def remove_land_time(self, id):
        if isinstance(id, int):
            if id in self.landing_time:
                del self.landing_time[id]
                del self.landing_time_str[id]
                return True
            else:
                return False
        else:
            raise Exception("Please check the aircraft id format")

    def remove_aircraft(self, id):
        if isinstance(id, int):
            if id in self.aircrafts:
                self.remove_land_time(id)
                if self.aircrafts[id][-1] > -1:
                    self.runways[self.aircrafts[id][-1]] = False
                del self.aircrafts[id]
                return True
            else:
                return False
        else:
            raise Exception("Please check the aircraft id format")
    
    def run_priority_indexing(self):
        data_lst = []
        for id, info in self.aircrafts.items():
            new_info = [id] + info
            new_info[1] -= new_info[2]
            new_info[1] = round(new_info[1],2)
            data_lst.append(new_info)
        
        data_lst.sort(key=lambda x : (x[1]/x[2], x[1], -x[2], -x[3], x[4]))

        self.aircrafts = {}
        for i in data_lst:
            self.aircrafts[i[0]] = i[1:]

        return data_lst
        
    def count_crashed(self):
        cnt = 0
        for id, info in self.aircrafts.items():
            if info[0] <= 0:
                cnt += 1
        return cnt

    def count_emergency(self):
        cnt = 0
        for id, info in self.aircrafts.items():
            if info[0] <= self.emergency_fuel_limit:
                cnt += 1
        return cnt

    def check_emergency(self, lst):
        for i in lst:
            if i[-2] == "True" and i[0] not in self.landing_time:
                if len(self.available_runways()) != 0:
                    self.do_landing(i[0])
                

    def show_information(self):
        table = BeautifulTable()

        lnth = 0
        new_lst = []
        for info in self.run_priority_indexing():
            data = info+["True" if info[1] <= self.emergency_fuel_limit else "False"]+ ["True" if info[1] < 0 else "False"]
            new_lst.append(data)
            table.rows.append(data)
            lnth += 1
        
        self.aircrafts_data_list = new_lst
        # self.check_emergency(new_lst)

        table.rows.header = [str(i) for i in range(1, lnth+1)]
        table.columns.header = ["Id", "Fuel", "Burning Rate", "Passengers", "Runway Time", "Runway Number",  "Emergency", "Crashed"]
        print(table)
        print()
        print()
        print("-"*150)
        print()
        print()

    def del_emergency_landing(self):
        data_dict = self.aircrafts.copy()
        print(self.aircrafts)
        for id, info in data_dict.items():
            if info[-1] > -1 and info[-2] <= 0 and info[0] > 0:
                self.successfully_land += 1
                self.runways[info[-1]] = False
                del self.landing_time[id]
                del self.aircrafts[id]
                time_str = str(self.landing_time_str[id])
                del self.landing_time_str[id]
                self.database.insert_doc(self.airport_name, id, info[2], info[-1], time_str)



    def update_runway_time(self, tick):
        if isinstance(tick, int):
            data_dict = self.aircrafts
            for id, info in data_dict.items():
                if info[-1] > -1:
                    self.aircrafts[id][-2] -= tick
        else:
            raise Exception("Please enter a vaild format of Tick")

    def run_tick_thread(self, tick):
        threading.Thread(target=self.run_tick, args=(tick,)).start()

    def run_tick(self, tick):
        if isinstance(tick, int):
            while True:
                self.del_emergency_landing()
                self.show_information()
                self.update_runway_time(tick)
                time.sleep(tick)
        else:
            raise Exception("Please enter a vaild format of Tick")

    def aircraft_exist(self, id):
        if isinstance(id, int):
            return id in self.aircrafts
        else:
            raise Exception("Please check the aircraft id format")
    
    def check_add_input_format(self, id, fuel, passengers, burning_rate, runway_time, runway_number):
        return isinstance(id, int) and (isinstance(fuel, float) or isinstance(fuel, int)) and isinstance(passengers, int) and (isinstance(burning_rate, float) or isinstance(burning_rate, int)) and isinstance(runway_time, int) and isinstance(runway_number, int)
    
    def on_runway_aircrafts(self):
        lst_runways = []
        for number, flag in self.runways.items():
            if flag == True:
                lst_runways.append(number)

        return lst_runways

    def available_runways(self):
        lst_runways = []
        for number, flag in self.runways.items():
            if flag == False:
                lst_runways.append(number)

        return lst_runways

    def is_runway_available(self, number):
        if number in self.runways:
            if isinstance(number, int):
                return self.runways[number]
            else:
                raise Exception("Please check the runway number format")
        else:
            return False





