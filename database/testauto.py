#---- calling for the necessary libraries
from datetime import datetime,timedelta
import glob
import os
now=datetime.now()
now=now + timedelta(hours=24)
print(now.strftime("%a"))

now=datetime.now().hour

print(now)