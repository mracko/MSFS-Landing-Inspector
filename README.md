# MSFS Landing Inspector
MSFS Landing Inspector is tool for analyzing landings in Microsoft Flight Simulator 2020. It reads the airplane’s telemetry data via SimConnect and displays relevant information about your landing in a web browser. This MSFS Landing Inspector is free to use. If you like this tool and would like to support the development, please consider donating here.

MSFS Landing Inspector displays the following data:
-	Current vertical G force
-	Current vertical speed
-	Touchdown G force
-	Touchdown vertical speed
-	Graph showing the G forces during landing
-	Graph showing the vertical speed during landing
-	Graph showing the altitude above ground during landing

Screenshot of MSFS Landing Inspector in action:

## Requirements
-	Python 3.7 or later
-	Python-SimConnect library
-	Flask library

## Installation
1. Install the latest Python 3 Release for Windows. Download the installer from https://www.python.org/downloads/windows/.
2. Run Command Prompt. Do this by pressing <kbd>Win</kbd> + <kbd>R</kbd>. Type *cmd.exe* and click OK.
3. In the Command Prompt windown type *pip install flask* and press <kbd>Enter</kbd>. When asked to download any Python dependencies, type *y* and press <kbd>Enter</kbd>. This will install the Flask Python library.
4. When finished installing Flask type *pip install SimConnect* and press <kbd>Enter</kbd>. When asked to download any Python dependencies, type *y* and press <kbd>Enter</kbd>.

## Running MSFS Landing Inspector
1. Start a flight in Microsoft Flight Simulator
2. Download and unzip the MSFS Landing Inspector repository and run *msfs_landing_inspector.py* by double clicking on it. This should launch a Command Prompt window.
3. Open your browser and load the site *localhost:5000*. This should load up the MSFS Landing Inspector in your browser.

## Running MSFS Ladning Inspector on your mobile device
1.  
2. Start a flight in Microsoft Flight Simulator
3. Download and unzip the MSFS Landing Inspector repository and run *msfs_landing_inspector.py* by double clicking on it. This should launch a Command Prompt window.
