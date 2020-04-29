import pandas as pd
from datetime import datetime



def logs(arg):
    me = arg
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    fun = pd.DataFrame([[time, me, 'successful']], columns=['timestamp', 'task', 'status'])
   
    fun.to_csv('/home/akash/ProjectSelenium/reporting/foo.csv' , index = False, header = False, mode='a')



