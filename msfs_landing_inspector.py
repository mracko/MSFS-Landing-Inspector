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
    v_speed_list = []
    g_force_list = []
    plane_alt_above_ground_list = []
    sim_on_ground_list = [1,1,1,1,1,1,1,1]
    run_app = 1
    simconnect_dict["G_FORCE"] = 0
    simconnect_dict["VERTICAL_SPEED"] = 0
    simconnect_dict["SIM_ON_GROUND"] = 0
    simconnect_dict["G_FORCE_LANDING"] = "N/A"
    simconnect_dict["VERTICAL_SPEED_LANDING"] = "N/A"
    simconnect_dict["G_FORCE_LANDING_LIST"] = "N/A"
    simconnect_dict["VERTICAL_SPEED_LANDING_LIST"] = "N/A"
    simconnect_dict["SIM_ON_GROUND_LIST"] = "N/A"
    simconnect_dict["AIRBORNE"] = 0
    simconnect_dict["G_FORCE_LIST"] = g_force_list
    simconnect_dict["V_SPEED_LIST"] = v_speed_list
    simconnect_dict["PLANE_ALT_ABOVE_GROUND_LIST"] = plane_alt_above_ground_list
    simconnect_dict["LANDING_RATING"] = "N/A"
    simconnect_dict["LANDING_COUNTER"] = 0
    
    # Create empty labels for charts
    labels_list = []
    for i in range(150):
        labels_list.append("")
    simconnect_dict["LABELS"] = labels_list
    
    # Run Simconnect Calculations
    while run_app == 1:
       
        if airborne == True and sum(sim_on_ground_list) == 30:
            simconnect_dict["G_FORCE_LANDING"] = max(g_force_list)
            max_gforce_index = g_force_list.index(max(g_force_list))
            simconnect_dict["VERTICAL_SPEED_LANDING"] = v_speed_list[max_gforce_index]
            simconnect_dict["G_FORCE_LANDING_LIST"] = g_force_list[::-1]*1
            v_speed_list_neg = [elem * (-1) for elem in v_speed_list]
            simconnect_dict["VERTICAL_SPEED_LANDING_LIST"] = v_speed_list_neg[::-1]*1
            simconnect_dict["PLANE_ALT_ABOVE_GROUND_LIST"] = plane_alt_above_ground_list[::-1]*1
            simconnect_dict["LANDING_COUNTER"] = simconnect_dict["LANDING_COUNTER"] + 1
            
            # Landing Rating Based on G-Forces
            if simconnect_dict["G_FORCE_LANDING"] < 1.25:
                simconnect_dict["LANDING_RATING"] = "Smooth landing"
            elif simconnect_dict["G_FORCE_LANDING"] < 1.5:
                simconnect_dict["LANDING_RATING"] = "Acceptable landing"
            elif simconnect_dict["G_FORCE_LANDING"] < 1.75:
                simconnect_dict["LANDING_RATING"] = "Poor landing"
            elif simconnect_dict["G_FORCE_LANDING"] < 2:
                simconnect_dict["LANDING_RATING"] = "Hard landing"
            elif simconnect_dict["G_FORCE_LANDING"] <= 2.5:
                simconnect_dict["LANDING_RATING"] = "Very hard landing"
            else:
                simconnect_dict["LANDING_RATING"] = "Structural damage to plane"
            airborne = False
        
        if sum(sim_on_ground_list) == 0 and airborne == False:
            airborne = True
            
        # Get Current Data       
        simconnect_dict["G_FORCE"] = round(aq.get("G_FORCE"), 2)
        simconnect_dict["VERTICAL_SPEED"] = round(aq.get("VERTICAL_SPEED"))
        simconnect_dict["SIM_ON_GROUND"] = aq.get("SIM_ON_GROUND")
        simconnect_dict["AIRBORNE"] = airborne
        simconnect_dict["G_FORCE_LIST"] = g_force_list
        
        # Make lists
        v_speed_list.insert(0, simconnect_dict["VERTICAL_SPEED"])
        if len(v_speed_list) > 151:
            v_speed_list.pop() 
        g_force_list.insert(0, simconnect_dict["G_FORCE"])
        if len(g_force_list) > 151:
           g_force_list.pop()
        sim_on_ground_list.insert(0, simconnect_dict["SIM_ON_GROUND"])
        if len(sim_on_ground_list) > 31:
           sim_on_ground_list.pop()
        plane_alt_above_ground_list.insert(0, (round(aq.get("PLANE_ALT_ABOVE_GROUND"), 1)))
        if len(plane_alt_above_ground_list) > 151:
           plane_alt_above_ground_list.pop()

        #print(f'SIMCONNECT: {simconnect_dict}')


if __name__ == "__main__":
    thread1 = Thread(target = simconnect_thread_func, args=('Thread-1', ))
    thread2 = Thread(target = flask_thread_func, args=('Thread-2', ))
    thread1.start()
    thread2.start()
        