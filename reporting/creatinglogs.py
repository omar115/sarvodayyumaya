import pandas as pd
import datetime as dt
from datetime import datetime
import os

import config



def logs(time1,time2,claimid,ipnum):

    tarik = dt.datetime.today().strftime("%m/%d/%Y")
    fun = pd.DataFrame([[time1, time2, claimid, ipnum, tarik, 'successful']], 
        columns=['start_time', 'end_time', 'claim id','ip number','date','status'])
   
    loc = os.path.join(config.PROJECT_ROOT, 'reporting', 'foo.csv')
    fun.to_csv(loc , index = False, header = False, mode='a')



