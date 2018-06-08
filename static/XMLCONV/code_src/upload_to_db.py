import glob
import sys
import requests
from datetime import datetime

# templateID = '5b07119e168a760b249d2eda' # VM 052418
# templateID = '5b16a9c8168a76127e8b3231' # VM 060518
# templateID = '5b1989f2168a76103d722387' # VM 060618
# templateID = '5b199a60168a760fc428a0e7' # VM 060718
templateID = '5b1ac75eb3d52f2c0ddeb9e2' # Duke OIT 060718

USER = "hby" # change here
PSWD = "nanomine" # change here
MDCS_URL = "http://localhost"
push_files = glob.glob('./xml/*.xml')
# print "Number of .XML to post: %d" % (len(push_files))
url = MDCS_URL + "/rest/curate"

# for pfile in push_files:
pfile = push_files[0]
opfile = open(pfile,'r')
fileContent = opfile.read()
data_to_send = {"title": sys.argv[1].split(".")[0] + ".xml",
                "schema":templateID,"content":fileContent}
r = requests.post(url, data_to_send, auth=(USER,PSWD))
print r.ok
print r.json, r.status_code, r.history
# if upload is completed
if r.ok:
    dt = datetime.now()
    with open('up.success', 'w+') as f:
        f.write(dt.strftime("%A, %d. %B %Y %I:%M%p"))
