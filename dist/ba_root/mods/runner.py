# ba_meta require api 8
import babase

# ba_meta export plugin
class File handler(babase.Plugin):
    def on_app_running(self):
        run()

def run():
    try:
        print("File Importing")
      
        print("File Imported")
    except Exception as e:
        print(e)
