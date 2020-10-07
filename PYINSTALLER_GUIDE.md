# MSFS LANDING INSPECTOR Pyinstaller Instructions

To compile an executable version of MSFS Landing Inspector using pyinstaller follow these 4 steps:

## 1. Change msfs_landing_inspector.py:

Change line 13 from:

`app = Flask(__name__)`

into:

```
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)
```

## 2. Remane SimConnect.dll

Rename the `SimConnect.dll` file located in the folder *SimConnectCust* into `SimConnect.dllc`.

## 3. Compile MSFS Landing Inspector using pyinstaller

Use the following pyinstaller settings to compile MSFS Landing Inspector:

```
pyinstaller -F --onefile --add-data "templates;templates" --add-data "static;static" --add-data "SimConnectCust;SimConnectCust" msfs_landing_inspector.py
```

## 4. Enjoy and have fun!
