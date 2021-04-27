from flask import Flask, render_template, jsonify, request
from SimConnectCust import *
from threading import Thread
import time

simconnect_dict = {}

# Flask WebApp
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
    
    

# SimConnect  App
def simconnect_thread_func(threadname):
    
    global simconnect_dict
    
    # Init SimConnect
    sm = SimConnect()
    aq = AircraftRequests(sm, _time = 0, _attemps = 3)
    
    # Init variables
    run_app = 1
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
    sim_on_ground_list_all = []
    airspeed = 0
    airspeed_prev = 0
    airspeed_list = []
    airspeed_list_ground = []
    pitch = 0
    pitch_prev = 0
    pitch_list = []
    pitch_list_ground = []
    bank = 0
    bank_prev = 0
    bank_list = []
    bank_list_ground = []
    heading = 0
    heading_prev = 0
    heading_list = []
    heading_list_ground = []
    wind_speed = 0
    wind_speed_prev = 0
    wind_speed_list = []
    wind_speed_list_ground = []
    wind_direction = 0
    wind_direction_prev = 0
    wind_direction_list = []
    wind_direction_list_ground = []
    airspeed_list_all = []
    pitch_list_all = []
    bank_list_all = []
    heading_list_all = []
    wind_speed_list_all = []
    wind_direction_list_all = []
    
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
    simconnect_dict["AIRSPEED"] = "N/A"
    simconnect_dict["AIRSPEED_LIST"] = airspeed_list
    simconnect_dict["AIRSPEED_LIST_GROUND"] = airspeed_list_ground
    simconnect_dict["PITCH"] = "N/A"
    simconnect_dict["PITCH_LIST"] = pitch_list
    simconnect_dict["PITCH_LIST_GROUND"] = pitch_list_ground
    simconnect_dict["BANK"] = "N/A"
    simconnect_dict["BANK_LIST"] = bank_list
    simconnect_dict["BANK_LIST_GROUND"] = bank_list_ground
    simconnect_dict["HEADING"] = "N/A"
    simconnect_dict["HEADING_LIST"] = heading_list
    simconnect_dict["HEADING_LIST_GROUND"] = heading_list_ground
    simconnect_dict["WIND_SPEED"] = "N/A"
    simconnect_dict["WIND_SPEED_LIST"] = wind_speed_list
    simconnect_dict["WIND_SPEED_LIST_GROUND"] = wind_speed_list_ground
    simconnect_dict["WIND_DIRECTION"] = "N/A"
    simconnect_dict["WIND_DIRECTION_LIST"] = wind_direction_list
    simconnect_dict["WIND_DIRECTION_LIST_GROUND"] = wind_direction_list_ground
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
               
        airspeed = round(aq.get("AIRSPEED_TRUE"))
        if airspeed < -99999:
            airspeed = airspeed_prev
        else:
            airspeed_prev = airspeed
            
        pitch = round(aq.get("PLANE_PITCH_DEGREES") * 180 / 3.1416, 1) * (-1)
        if abs(pitch) > 999:
            pitch = pitch_prev
        else:
            pitch_prev = pitch 

        bank = round((aq.get("PLANE_BANK_DEGREES") * 180 / 3.1416), 1)
        if abs(bank) > 999:
            bank = bank_prev
        else:
            bank_prev = bank

        heading = round(aq.get("PLANE_HEADING_DEGREES_TRUE") * 180 / 3.1416)
        if abs(heading) > 999:
            heading = heading_prev
        else:
            heading_prev = heading
            
        wind_speed = round(aq.get("AMBIENT_WIND_VELOCITY"), 1)
        if wind_speed < -99999:
            wind_speed = wind_speed_prev
        else:
            wind_speed_prev = wind_speed

        wind_direction = round(aq.get("AMBIENT_WIND_DIRECTION"))
        if wind_direction < -99999:
            wind_direction = wind_direction_prev
        else:
            wind_direction_prev = wind_direction
        
        # Make lists
        sim_on_ground_list.insert(0, sim_on_ground)
        if len(sim_on_ground_list) > 21:
           sim_on_ground_list.pop()
           
        sim_on_ground_list_all.insert(0, sim_on_ground)
        if len(sim_on_ground_list_all) > 151:
           sim_on_ground_list_all.pop()

        v_speed_list_all.insert(0, v_speed)
        if len(v_speed_list_all) > 151:
            v_speed_list_all.pop()
        g_force_list_all.insert(0, g_force)
        if len(g_force_list_all) > 151:
            g_force_list_all.pop()
        airspeed_list_all.insert(0, airspeed)
        if len(airspeed_list_all) > 151:
            airspeed_list_all.pop() 
        pitch_list_all.insert(0, pitch)
        if len(pitch_list_all) > 151:
            pitch_list_all.pop() 
        bank_list_all.insert(0, bank)
        if len(bank_list_all) > 151:
            bank_list_all.pop() 
        heading_list_all.insert(0, heading)
        if len(heading_list_all) > 151:
            heading_list_all.pop() 
        wind_speed_list_all.insert(0, wind_speed)
        if len(wind_speed_list_all) > 151:
            wind_speed_list_all.pop()
        wind_direction_list_all.insert(0, wind_direction)
        if len(wind_direction_list_all) > 151:
            wind_direction_list_all.pop()
        
        
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
            airspeed_list.insert(0, "null")
            if len(airspeed_list) > 151:
               airspeed_list.pop()
            airspeed_list_ground.insert(0, airspeed)
            if len(airspeed_list_ground) > 151:
               airspeed_list_ground.pop()
            pitch_list.insert(0, "null")
            if len(pitch_list) > 151:
               pitch_list.pop()
            pitch_list_ground.insert(0, pitch)
            if len(pitch_list_ground) > 151:
               pitch_list_ground.pop()
            bank_list.insert(0, "null")
            if len(bank_list) > 151:
               bank_list.pop()
            bank_list_ground.insert(0, bank)
            if len(bank_list_ground) > 151:
               bank_list_ground.pop()
            heading_list.insert(0, "null")
            if len(heading_list) > 151:
               heading_list.pop()
            heading_list_ground.insert(0, heading)
            if len(heading_list_ground) > 151:
               heading_list_ground.pop()
            wind_speed_list.insert(0, "null")
            if len(wind_speed_list) > 151:
               wind_speed_list.pop()
            wind_speed_list_ground.insert(0, wind_speed)
            if len(wind_speed_list_ground) > 151:
               wind_speed_list_ground.pop()
            wind_direction_list.insert(0, "null")
            if len(wind_direction_list) > 151:
               wind_direction_list.pop()
            wind_direction_list_ground.insert(0, wind_direction)
            if len(wind_direction_list_ground) > 151:
               wind_direction_list_ground.pop()
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
            airspeed_list.insert(0, airspeed)
            if len(airspeed_list) > 151:
               airspeed_list.pop()
            airspeed_list_ground.insert(0, "null")
            if len(airspeed_list_ground) > 151:
               airspeed_list_ground.pop()
            pitch_list.insert(0, pitch)
            if len(pitch_list) > 151:
               pitch_list.pop()
            pitch_list_ground.insert(0, "null")
            if len(pitch_list_ground) > 151:
               pitch_list_ground.pop()
            bank_list.insert(0, bank)
            if len(bank_list) > 151:
               bank_list.pop()
            bank_list_ground.insert(0, "null")
            if len(bank_list_ground) > 151:
               bank_list_ground.pop()
            heading_list.insert(0, heading)
            if len(heading_list) > 151:
               heading_list.pop()
            heading_list_ground.insert(0, "null")
            if len(heading_list_ground) > 151:
               heading_list_ground.pop()
            wind_speed_list.insert(0, wind_speed)
            if len(wind_speed_list) > 151:
               wind_speed_list.pop()
            wind_speed_list_ground.insert(0, "null")
            if len(wind_speed_list_ground) > 151:
               wind_speed_list_ground.pop()
            wind_direction_list.insert(0, wind_direction)
            if len(wind_direction_list) > 151:
               wind_direction_list.pop()
            wind_direction_list_ground.insert(0, "null")
            if len(wind_direction_list_ground) > 151:
               wind_direction_list_ground.pop()

        
        # Populate vars to JSON dictionary
        simconnect_dict["G_FORCE"] = g_force
        simconnect_dict["VERTICAL_SPEED"] = v_speed
        simconnect_dict["SIM_ON_GROUND"] = sim_on_ground
        simconnect_dict["AIRBORNE"] = airborne

        
        # Make landing/airborne decision
        if airborne == True and sum(sim_on_ground_list) == 20:
            # Fix - need to get the last value before on ground readings
            v_speed_list_touchdown = v_speed_list_ground
            g_force_list_touchdown = g_force_list_ground
            change_last = False
            for idx, element in enumerate(v_speed_list_touchdown):
                if idx >= 1:
                    if element == "null" and sim_on_ground_list_all[idx-1] == 1:
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
            
            # Get Values for Touchdown 
            simconnect_dict["VERTICAL_SPEED_LANDING"] = min(v_speed_list_touchdown)
            
            # Calculate Custom G-Force based on vertical speed
            # Model uses Harvsine acceleration model for peak acceleration https://www.nhtsa.gov/sites/nhtsa.dot.gov/files/18esv-000501.pdf
            # For time a custom function is used that ranges from 0.25 for GA to 0.35 for airliners. This simulates the rigidness of suspention.
            custom_g_force_v_speed_m_per_s = (min(v_speed_list_touchdown) * (-0.3048) / 60)
            plane_weight = max(round(aq.get("TOTAL_WEIGHT") * 0.45), 50)
            custom_g_force_impact_duration = 0.355 + (-0.103/(1 + (plane_weight/15463)**1.28))
            custom_g_force = 1 + (((2 * custom_g_force_v_speed_m_per_s) / custom_g_force_impact_duration) / 9.80665)
            custom_g_force = round(custom_g_force, 2)

            # Get Index of Touchdown from min Vertical Speed
            index_vspeed_touchdown = v_speed_list_touchdown.index(min(v_speed_list_touchdown))
            
            # Check if SimConnect G force is within +/- 10% of custom G force. If not use custom G force
            if g_force_list_touchdown[index_vspeed_touchdown] < custom_g_force*0.9 or g_force_list_touchdown[index_vspeed_touchdown] > custom_g_force*1.1:
                g_force_list_touchdown[index_vspeed_touchdown] = custom_g_force
                g_force_list[index_vspeed_touchdown] = custom_g_force
                g_force_list_ground[index_vspeed_touchdown] = custom_g_force
            
            # Get the rest of touchdown data based on vertical speed index
            simconnect_dict["G_FORCE_LANDING"] = max(g_force_list_touchdown)
            simconnect_dict["AIRSPEED"] = airspeed_list_all[index_vspeed_touchdown]
            simconnect_dict["PITCH"] = pitch_list_all[index_vspeed_touchdown]
            simconnect_dict["BANK"] = bank_list_all[index_vspeed_touchdown]
            simconnect_dict["HEADING"] = heading_list_all[index_vspeed_touchdown]
            simconnect_dict["WIND_SPEED"] = wind_speed_list_all[index_vspeed_touchdown]
            simconnect_dict["WIND_DIRECTION"] = wind_direction_list_all[index_vspeed_touchdown]
            
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
            simconnect_dict["AIRSPEED_LIST"] = airspeed_list[::-1]*1
            simconnect_dict["AIRSPEED_LIST_GROUND"] = airspeed_list_ground[::-1]*1
            simconnect_dict["PITCH_LIST"] = pitch_list[::-1]*1
            simconnect_dict["PITCH_LIST_GROUND"] = pitch_list_ground[::-1]*1
            simconnect_dict["BANK_LIST"] = bank_list[::-1]*1
            simconnect_dict["BANK_LIST_GROUND"] = bank_list_ground[::-1]*1
            simconnect_dict["HEADING_LIST"] = heading_list[::-1]*1
            simconnect_dict["HEADING_LIST_GROUND"] = heading_list_ground[::-1]*1
            simconnect_dict["WIND_SPEED_LIST"] = wind_speed_list[::-1]*1
            simconnect_dict["WIND_SPEED_LIST_GROUND"] = wind_speed_list_ground[::-1]*1
            simconnect_dict["WIND_DIRECTION_LIST"] = wind_direction_list[::-1]*1
            simconnect_dict["WIND_DIRECTION_LIST_GROUND"] = wind_direction_list_ground[::-1]*1
            simconnect_dict["SIM_ON_GROUND_LIST"] = sim_on_ground_list_all[::-1]*1
            
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
            
            
        # Decision for Airborne
        if sum(sim_on_ground_list) == 0 and airborne == False:
            airborne = True

        
if __name__ == "__main__":
    thread1 = Thread(target = simconnect_thread_func, args=('Thread-1', ), daemon=True)
    thread2 = Thread(target = flask_thread_func, args=('Thread-2', ), daemon=True)
    thread1.start()
    thread2.start()

    print("\n*********************")
    print("MSFS Landing Inspector initialized")
    print("Load 'localhost:5000' in your browser to start MSFS Landing Inspector")
    print("Tip: You can access MSFS Landing Inspector from your mobile device. Check install_instructions.txt for instructions.")
    print("\n*********************\n\n")
    while True:
        time.sleep(.5)
