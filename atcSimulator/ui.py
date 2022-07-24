from operator import imod
from matplotlib.pyplot import show
from numpy import size
from requests import delete
# import atcSimulator.main_class as main_class
import main_class
from tkinter import *
import threading
import time
import tksheet

class Ui:
    def __init__(self):
        self.code = main_class.ATC("Name", 0, 0)
        self.root = Tk(className=" ATC Simulator")
        self.root.geometry("1000x600")
        self.root.resizable(0, 0)

        self.sheet = tksheet.Sheet(self.root, width=1000, height=250)
        self.sheet.headers(["Id", "Fuel", "Burning Rate", "Passengers", "Runway Time", "Runway Number",  "Emergency", "Crashed"])
        self.sheet.pack(side=BOTTOM)
        self.parent1 = Frame()
        self.parent1.pack(side=TOP, anchor=NW)

        self.add_Id, self.add_Fuel, self.add_Rate, self.add_Passengers, self.add_Time, self.add_Number = None, None, None, None, None, None
        self.airport_name, self.airport_runways, self.airport_emergency = None, None, None
        self.draw_add_form(self.parent1)

        self.parent2 = Frame()
        self.parent2.pack(side=TOP, anchor=NW)
        self.draw_airport_form(self.parent2)

        self.cnt, self.remove_id, self.land_id = None, None, None
        self.parent3 = Frame()
        self.parent3.pack(side=TOP, anchor=NW)
        self.draw_extra_functions(self.parent3)

        self.show_info_window = None

        t1 = threading.Thread(target=self.code.run_tick, args=(1, self.extra_total_aircrafts, self.extra_total_on_runway, self.extra_total_available_runways, self.extra_crashed, self.extra_successfully_landed, self.extra_current_emergency, self.sheet))

        t1.start()

        self.root.mainloop()


        self.code.run = False

        t1.join()

        
    def show_extra_info_on_gui(self, window):
        self.extra_total_aircrafts = Label(window ,text = "Total aircrafts: 12").grid(row = 0,column = 0)
        self.extra_total_on_runway = Label(window ,text = "Total aircrafts on runway: 3").grid(row = 1,column = 0)
        self.extra_total_available_runways = Label(window ,text = "Total runway availables: 2").grid(row = 2,column = 0)
        self.extra_crashed = Label(window ,text = "Crashed: 2").grid(row = 3,column = 0)
        self.extra_successfully_landed = Label(window ,text = "Successfully landed: 21").grid(row = 4,column = 0)
        self.extra_current_emergency = Label(window ,text = "Current emergency aircrafts: 3").grid(row = 4,column = 0)



    def get_random_cnt(self):
        try:
            Cnt = int(self.cnt.get())
            self.code.add_random_aircraft(Cnt)
            self.cnt.delete(0, 'end')
        except:
            raise Exception("Please check inputs format.")

    def get_remove_id(self):
        try:
            Id = int(self.remove_id.get())
            self.code.remove_aircraft(Id)
            self.remove_id.delete(0, 'end')
        except:
            raise Exception("Please check inputs format.")

    def get_land_aircraft(self):
        try:
            Id = int(self.land_id.get())
            self.code.do_landing(Id)
            self.land_id.delete(0, 'end')
        except:
            raise Exception("Please check inputs format.")

    def show_search_table(self, sheet, id_entry):
        try:
            Id = int(id_entry.get())
            lst = self.code.aircrafts_data_list
            sheet.set_sheet_data([])
            for i in lst:
                if i[0] == Id:
                    sheet.set_sheet_data([i])
                    break
        except:
            raise Exception("Please check aircraft id")

    def show_search_aircraft_info_window(self):
        if self.show_info_window != None:
            self.show_info_window.destroy()

        self.show_info_window = Toplevel(self.root)
        self.show_info_window.geometry("1000x150")
        self.show_info_window.title("Search Aircraft Information")
        self.show_info_window.resizable(0, 0)

        sheet = tksheet.Sheet(self.show_info_window, width=1000, height=100)
        sheet.headers(["Id", "Fuel", "Burning Rate", "Passengers", "Runway Time", "Runway Number",  "Emergency", "Crashed"])
        sheet.pack(side=BOTTOM)

        frame = Frame(self.show_info_window)
        frame.pack(side=TOP, anchor=NW)
        
        Label(frame ,text = "Aircraft Id    ").grid(row = 0,column = 0)
        id = Entry(frame)
        id.grid(row=0, column=1)
        Label(frame ,text = "       ").grid(row = 0,column = 2)
        Button(frame ,text="Search Aircraft", command= lambda : self.show_search_table(sheet, id)).grid(row=0, column=3)

    def show_new_aircraft_info_window(self):
        if self.show_info_window != None:
            self.show_info_window.destroy()

        self.show_info_window = Toplevel(self.root)
        self.show_info_window.geometry("1000x250")
        self.show_info_window.title("Aircrafts Information")
        self.show_info_window.resizable(0, 0)

        sheet = tksheet.Sheet(self.show_info_window, width=1000, height=250)
        sheet.headers(["Id", "Fuel", "Burning Rate", "Passengers", "Runway Time", "Runway Number",  "Emergency", "Crashed"])
        sheet.grid()
        lst = self.code.aircrafts_data_list
        sheet.set_sheet_data(lst)
        
    def show_database_aircraft_info_window(self):
        if self.show_info_window != None:
            self.show_info_window.destroy()

        self.show_info_window = Toplevel(self.root)
        self.show_info_window.geometry("510x250")
        self.show_info_window.title("Aircrafts Information From Database")
        self.show_info_window.resizable(0, 0)

        sheet = tksheet.Sheet(self.show_info_window, width=1000, height=250)
        sheet.headers(["Id", "Passengers", "Runway Number",  "Landing Date/Time"])
        sheet.grid()
        lst = self.code.database.get_data(self.code.airport_name)
        sheet.set_sheet_data(lst)
        

    def draw_extra_functions(self, window):
        a = Label(window ,text = "           Count").grid(row = 0,column = 0)
        b = Label(window ,text = "            Aircraft Id").grid(row = 0,column = 2)
        c = Label(window ,text = "                    Aircraft Id").grid(row = 0,column = 4)
        self.cnt = Entry(window)
        self.cnt.grid(row = 0,column = 1)
        self.remove_id = Entry(window)
        self.remove_id.grid(row = 0,column = 3)
        self.land_id = Entry(window)
        self.land_id.grid(row = 0,column = 5)
        Label(window ,text = "").grid(row = 2,column = 2)
        Button(window ,text="Add Random Aircrafts", command= self.get_random_cnt).grid(row=3, column=1)
        Button(window ,text="Remove Aircraft", command= self.get_remove_id).grid(row=3, column=3)
        Button(window ,text="Land Aircraft", command= self.get_land_aircraft).grid(row=3, column=5)
        Label(window ,text = "                          ").grid(row = 0,column = 6)
        Button(window ,text="Show aircrafts information", command= self.show_new_aircraft_info_window).grid(row=0, column=7)
        Label(window ,text = "").grid(row = 3,column = 6)
        Button(window ,text="Show successfully landed aircrafts information", command= self.show_database_aircraft_info_window).grid(row=3, column=7)
    
    def get_add_form_data(self):
        try:
            Id, Fuel, Burning_Rate, Passengers, Time, Number = 0, 0, 0, 0, 0, -1
            Id = int(self.add_Id.get())
            Fuel = float(self.add_Fuel.get())
            Burning_Rate = float(self.add_Rate.get())
            Passengers = int(self.add_Passengers.get())
            Time = int(self.add_Time.get())
            self.code.add_aircraft(Id, Fuel, Passengers, Burning_Rate, Time, Number)
            self.add_Id.delete(0, 'end')
            self.add_Fuel.delete(0, 'end')
            self.add_Rate.delete(0, 'end')
            self.add_Passengers.delete(0, 'end')
            self.add_Time.delete(0, 'end')
        except:
            raise Exception("Please check inputs format.")


    def add_form_placeholders(self):
        self.add_Id.insert(0, "Id")
        self.add_Fuel.insert(0, "Fuel")
        self.add_Passengers.insert(0, "Passengers")
        self.add_Rate.insert(0, "Burning Rate")
        self.add_Time.insert(0, "Runway Time")

    def draw_add_form(self, window):
        a = Label(window ,text = "Id").grid(row = 0,column = 0)
        b = Label(window ,text = "      Fuel").grid(row = 0,column = 2)
        c = Label(window ,text = "                Burning Rate").grid(row = 0,column = 4)
        d = Label(window ,text = "      Passengers").grid(row = 1,column = 0)
        e = Label(window ,text = "    Runway Time").grid(row = 1,column = 2)
        g = Label(window ,text = "").grid(row = 2,column = 2)
        self.add_Id = Entry(window)
        self.add_Id.grid(row = 0,column = 1)
        self.add_Fuel = Entry(window)
        self.add_Fuel.grid(row = 0,column = 3)
        self.add_Rate = Entry(window)
        self.add_Rate.grid(row = 0,column = 5)
        self.add_Passengers = Entry(window)
        self.add_Passengers.grid(row = 1,column = 1)
        self.add_Time = Entry(window)
        self.add_Time.grid(row = 1,column = 3)
        
        Button(window ,text="Add Aircraft", command= self.get_add_form_data).grid(row=3, columnspan=2, sticky='ew', column=2)
        Label(window ,text = "").grid(row = 4,column = 2)
        Label(window ,text = "").grid(row = 5,column = 2)

        self.extra_total_aircrafts = Label(window ,text = "                                       Aircrafts: 0", font=("Arial", 12))
        self.extra_total_aircrafts.grid(row = 0,column = 10)
        self.extra_total_on_runway = Label(window ,text = "                    Aircrafts on runway: 0", font=("Arial", 12))
        self.extra_total_on_runway.grid(row = 1,column = 10)
        self.extra_total_available_runways = Label(window ,text = "                      Available runways: 0", font=("Arial", 12))
        self.extra_total_available_runways.grid(row = 2,column = 10)
        self.extra_crashed = Label(window ,text = "                                     Crashed: 0", font=("Arial", 12))
        self.extra_crashed.grid(row = 3,column = 10)
        self.extra_successfully_landed = Label(window ,text = "                     Successfully landed: 0", font=("Arial", 12))
        self.extra_successfully_landed.grid(row = 4,column = 10)
        self.extra_current_emergency = Label(window ,text = "                   Emergency aircrafts: 0", font=("Arial", 12))
        self.extra_current_emergency.grid(row = 5,column = 10)

    def get_airport_form_data(self):
        try:
            Name, Runways, Emergency = "Name", 0, 0.0
            Name = str(self.airport_name.get())
            Runways = int(self.airport_runways.get())
            Emergency = float(self.airport_emergency.get())
            self.code.airport_name = Name
            self.code.runways_cnt = Runways
            self.code.emergency_fuel_limit = Emergency
            self.code.add_runways()
            self.airport_name.delete(0, 'end')
            self.airport_emergency.delete(0, 'end')
            self.airport_runways.delete(0, 'end')
        except:
            raise Exception("Please check inputs format.")

    def draw_airport_form(self, window):
        a = Label(window ,text = "Airport Name").grid(row = 0,column = 0)
        b = Label(window ,text = "    Total Runways").grid(row = 0,column = 2)
        c = Label(window ,text = "Emergency Fuel Limit").grid(row = 0,column = 4)
        self.airport_name = Entry(window)
        self.airport_name.grid(row = 0,column = 1)
        self.airport_runways = Entry(window)
        self.airport_runways.grid(row = 0,column = 3)
        self.airport_emergency = Entry(window)
        self.airport_emergency.grid(row = 0,column = 5)
        Label(window ,text = "").grid(row = 2,column = 2)
        Button(window ,text="Add Details", command= self.get_airport_form_data).grid(row=3, columnspan=2, sticky='ew', column=2)
        Label(window ,text = "                                                      ").grid(row = 4,column = 6)
        Button(window ,text="Search Aircraft", command= self.show_search_aircraft_info_window).grid(row=4, column=7)
        Label(window ,text = "").grid(row = 4,column = 2)
        Label(window ,text = "").grid(row = 5,column = 2)



ui = Ui()