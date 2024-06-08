# ba_meta require api 8



import babase
import bascenev1 as bs
from datetime import datetime
import time

# ba_meta export plugin
class FileRunner(babase.Plugin):
    def on_app_running(self):
        run()

orginial_begin = bs._activity.Activity.on_begin

def new_begin(self):
    from datafiles import newvotehandler as vm
    now = datetime.now()
    orginial_begin(self)
#    vm.reset()
   # bs.cameraflash(duration=999)


 
def run():
 #   try:
     print("Importing Custom Files")
     from datafiles import characterchooser
     characterchooser.enable()
     bs._activity.Activity.on_begin = new_begin
     from bascenev1 import _hooks

     from datafiles import livestats
     livestats.ChatSaver().start()
     from datafiles import discordbot as db
     db.run()
     from datafiles import ModifiedSpaz as ms
     ms.enable()
     from datafiles import ModifiedElimination as nel
   #  nel.enable()
     from datafiles import afkremover as ar
     ar.start()
     from datafiles import playerhandler as ph
     ph.apply()
     print("Imported Custom Files")
   # except Exception as e:
     #   print(f"Error While Importing Custom Files: {e}")
      #  pass

