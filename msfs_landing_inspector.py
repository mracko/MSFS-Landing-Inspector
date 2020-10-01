from flask import Flask, render_template, jsonify, request
from SimConnect import *
from threading import Thread

simconnect_dict = {}

def flask_thread_func(threadname):
    
    global simconnect_dict
    
    app = Flask(__name__)
    
    @app.route('/_stuff', methods = ['GET'])
    def stuff():
        global simconnect_dict
        
        return jsonify(simconnect_dict)

    @app.route('/')
    def index():
        return render_template('body.html')

    app.run(host='0.0.0.0', debug=False, use_reloader=False)

def simconnect_thread_func(threadname):
    
    global simconnect_dict
    
    # Init SimConnect
    sm = SimConnect()
    aq = AircraftRequests(sm, _time = 0)
    
    # Init variables
    airborne = False
    g_force = 0
    v_speed = 0
    plane_alt_above_ground = 0
    sim_on_ground = 0
    g_force_prev = 0
    v_speed_prev = 0
    plane_alt_above_ground_prev = 0
    sim_on_ground_prev = 0
    v_speed_list_all = []
    g_force_list_all = []
    v_speed_list = []
    g_force_list = []
    plane_alt_above_ground_list = []
    v_speed_list_ground = []
    g_force_list_ground = []
    plane_alt_above_ground_list_ground = []
    sim_on_ground_list = [1,1,1,1,1,1,1,1]
    run_app = 1
    simconnect_dict["G_FORCE"] = 0
    simconnect_dict["VERTICAL_SPEED"] = 0
    simconnect_dict["SIM_ON_GROUND"] = 0
    simconnect_dict["G_FORCE_LANDING"] = "N/A"
    simconnect_dict["VERTICAL_SPEED_LANDING"] = "N/A"
    simconnect_dict["SIM_ON_GROUND_LIST"] = "N/A"
    simconnect_dict["AIRBORNE"] = 0
    simconnect_dict["G_FORCE_LIST"] = g_force_list
    simconnect_dict["V_SPEED_LIST"] = v_speed_list
    simconnect_dict["G_FORCE_LANDING_LIST"] = "N/A"
    simconnect_dict["G_FORCE_LANDING_LIST_GROUND"] = "N/A"
    simconnect_dict["VERTICAL_SPEED_LANDING_LIST"] = "N/A"    
    simconnect_dict["VERTICAL_SPEED_LANDING_LIST_GROUND"] = "N/A"
    simconnect_dict["PLANE_ALT_ABOVE_GROUND_LIST"] = plane_alt_above_ground_list
    simconnect_dict["PLANE_ALT_ABOVE_GROUND_LIST_GROUND"] = plane_alt_above_ground_list_ground
    simconnect_dict["LANDING_RATING"] = "N/A"
    simconnect_dict["LANDING_COUNTER"] = 0
    
    # Create empty labels for charts
    labels_list = []
    for i in range(150):
        labels_list.append("")
    simconnect_dict["LABELS"] = labels_list
    
    # Run Simconnect Calculations
    while run_app == 1:
            
        # Get Current Data 
        # Fix for -999999 values
        
        v_speed = round(aq.get("VELOCITY_WORLD_Y")*60)
        if v_speed < -99999:
            v_speed = v_speed_prev
        else:
            #g_force_custom =  ((v_speed * 0.3048) - (v_speed_prev * 0.3048)) + 9.8 
            g_force_custom =  (round(aq.get("ACCELERATION_WORLD_Y")) / 32.2) + 1
            v_speed_prev = v_speed

        g_force = round(aq.get("G_FORCE"), 2)
        if g_force < -99999:
            g_force = g_force_prev
        else:
            g_force_prev = g_force
            
        plane_alt_above_ground = round(aq.get("PLANE_ALT_ABOVE_GROUND"), 1)
        if plane_alt_above_ground < -99999:
            plane_alt_above_ground = plane_alt_above_ground_prev
        else:
            plane_alt_above_ground_prev = plane_alt_above_ground
        
        sim_on_ground = aq.get("SIM_ON_GROUND")
        if sim_on_ground < -99999:
            sim_on_ground = sim_on_ground_prev
        else:
            sim_on_ground_prev = sim_on_ground        
               
        
        # Make lists
        sim_on_ground_list.insert(0, sim_on_ground)
        if len(sim_on_ground_list) > 31:
           sim_on_ground_list.pop()
        v_speed_list_all.insert(0, v_speed)
        if len(v_speed_list_all) > 151:
            v_speed_list_all.pop()
        g_force_list_all.insert(0, g_force)
        if len(g_force_list_all) > 151:
            g_force_list_all.pop() 
        
        # Make lists for graph - separation between airborne and landing
        if sim_on_ground == 1:
            v_speed_list.insert(0, "null")
            if len(v_speed_list) > 151:
                v_speed_list.pop() 
            g_force_list.insert(0, "null")
            if len(g_force_list) > 151:
               g_force_list.pop()
            plane_alt_above_ground_list.insert(0, "null")
            if len(plane_alt_above_ground_list) > 151:
               plane_alt_above_ground_list.pop()
            v_speed_list_ground.insert(0, v_speed)
            if len(v_speed_list_ground) > 151:
                v_speed_list_ground.pop() 
            g_force_list_ground.insert(0, g_force)
            if len(g_force_list_ground) > 151:
               g_force_list_ground.pop()
            plane_alt_above_ground_list_ground.insert(0, plane_alt_above_ground)
            if len(plane_alt_above_ground_list_ground) > 151:
               plane_alt_above_ground_list_ground.pop()
        else:
            v_speed_list.insert(0, v_speed)
            if len(v_speed_list) > 151:
                v_speed_list.pop() 
            g_force_list.insert(0, g_force)
            if len(g_force_list) > 151:
               g_force_list.pop()
            plane_alt_above_ground_list.insert(0, plane_alt_above_ground)
            if len(plane_alt_above_ground_list) > 151:
               plane_alt_above_ground_list.pop()
            v_speed_list_ground.insert(0, "null")
            if len(v_speed_list_ground) > 151:
                v_speed_list_ground.pop() 
            g_force_list_ground.insert(0, "null")
            if len(g_force_list_ground) > 151:
               g_force_list_ground.pop()
            plane_alt_above_ground_list_ground.insert(0, "null")
            if len(plane_alt_above_ground_list_ground) > 151:
               plane_alt_above_ground_list_ground.pop()
        

        # Populate vars to JSON dictionary
        simconnect_dict["G_FORCE"] = g_force
        simconnect_dict["VERTICAL_SPEED"] = v_speed
        simconnect_dict["SIM_ON_GROUND"] = sim_on_ground
        simconnect_dict["AIRBORNE"] = airborne
        
        # Make landing/airborne decision
        if airborne == True and sum(sim_on_ground_list) == 30:
            # Fix - need to get the last value before on ground readings
            v_speed_list_touchdown = v_speed_list_ground
            g_force_list_touchdown = g_force_list_ground
            change_last = False
            for idx, element in enumerate(v_speed_list_touchdown):
                if idx >= 1:
                    if element == 0 and v_speed_list_touchdown[idx-1] == 1:
                        if change_last == False:
                            v_speed_list_touchdown[idx] = v_speed_list[idx]
                            g_force_list_touchdown[idx] = g_force_list[idx]
                            change_last = True
                        else:
                            change_last = False
                    else:
                        change_last = False
            
            v_speed_list_touchdown = [0 if x=="null" else x for x in v_speed_list_touchdown]
            g_force_list_touchdown = [0 if x=="null" else x for x in g_force_list_touchdown]
            
            simconnect_dict["G_FORCE_LANDING"] = max(g_force_list_touchdown)
            simconnect_dict["VERTICAL_SPEED_LANDING"] = min(v_speed_list_touchdown)
            # Create Lists for Graphs
            simconnect_dict["G_FORCE_LANDING_LIST"] = g_force_list[::-1]*1
            simconnect_dict["G_FORCE_LANDING_LIST_GROUND"] = g_force_list_ground[::-1]*1
            v_speed_list_neg = [elem * (-1) if elem != "null" else "null" for elem in v_speed_list]
            v_speed_list_ground_neg = [elem * (-1) if elem != "null" else "null" for elem in v_speed_list_ground]
            simconnect_dict["VERTICAL_SPEED_LANDING_LIST"] = v_speed_list_neg[::-1]*1
            simconnect_dict["VERTICAL_SPEED_LANDING_LIST_GROUND"] = v_speed_list_ground_neg[::-1]*1
            simconnect_dict["PLANE_ALT_ABOVE_GROUND_LIST"] = plane_alt_above_ground_list[::-1]*1
            simconnect_dict["PLANE_ALT_ABOVE_GROUND_LIST_GROUND"] = plane_alt_above_ground_list_ground[::-1]*1
            simconnect_dict["LANDING_COUNTER"] = simconnect_dict["LANDING_COUNTER"] + 1
            
            # Landing Rating Based on G-Forces
            if simconnect_dict["VERTICAL_SPEED_LANDING"] > -60:
                simconnect_dict["LANDING_RATING"] = "Very soft landing"
            elif simconnect_dict["VERTICAL_SPEED_LANDING"] > -120:
                simconnect_dict["LANDING_RATING"] = "Soft landing"
            elif simconnect_dict["VERTICAL_SPEED_LANDING"] > -200:
                simconnect_dict["LANDING_RATING"] = "Average landing"
            elif simconnect_dict["VERTICAL_SPEED_LANDING"] > -300:
                simconnect_dict["LANDING_RATING"] = "Firm landing"
            elif simconnect_dict["VERTICAL_SPEED_LANDING"] > -400:
                simconnect_dict["LANDING_RATING"] = "Hard landing"
            elif simconnect_dict["VERTICAL_SPEED_LANDING"] > -600:
                simconnect_dict["LANDING_RATING"] = "Very hard landing"
            else:
                simconnect_dict["LANDING_RATING"] = "Structural damage to plane"
            airborne = False
        
        if sum(sim_on_ground_list) == 0 and airborne == False:
            airborne = True

if __name__ == "__main__":
    thread1 = Thread(target = simconnect_thread_func, args=('Thread-1', ))
    thread2 = Thread(target = flask_thread_func, args=('Thread-2', ))
    thread1.start()
    thread2.start()
        