# ba_meta require api 8



import babase
import bascenev1 as bs
from datetime import datetime
import time

# ba_meta export plugin
class FileRunner(babase.Plugin):
    def on_app_running(self):
        run()
        check_modules()

orginial_begin = bs._activity.Activity.on_begin

def new_begin(self):
    from datafiles import newvotehandler as vm
    now = datetime.now()
    orginial_begin(self)
    vm.reset()


 
def run():
    try:
        print("Importing Custom Files")
        from datafiles import characterchooser
        characterchooser.enable()
        bs._activity.Activity.on_begin = new_begin
        from datafiles import livestats
        livestats.ChatSaver().start()
        from datafiles import discordbot as db
        db.run()
        from datafiles import ModifiedSpaz as ms
        ms.enable()
        from datafiles import afkremover as ar
        ar.start()
        from datafiles import playerlogger as ph
        ph.apply()
        print("Imported Custom Files")
    except Exception as e:
        print(f"Error While Importing Custom Files: {e}")
        pass

def check_modules():
    try:
        import discord
        import requests
        import lxml
        import bs4
        import jishaku
        print("------Modules Already Installed------")
    except ImportError:
        print("------Installing Custom Modules------")
        cur_folder_name = os.path.basename(os.getcwd())
        target_directory = f"/home/ubuntu/{cur_folder_name}/dist/ba_data/python-site-packages/"
        
        required_modules = ["discord", "requests", "lxml", "bs4", "jishaku"]
        for module in required_modules:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module, "--target", target_directory])
        print("------Installed Custom Modules------")
