# Run a matlab job and send completion email
# MATLAB parameters sent at end of command line
# Parameters:
#    --jobid JOBID               - jobid
#    --pgmdir PGMDIR             - matlab program dir
#    --pgm   PGM                 - matlab program to run
#    --user USER                 - Username for greeting
#    --email EMAIL               - Email address to send completion email 
#    --emailtemplate TEMPLATE    - Email template file name
#    --serverbase SERVERBASE     - Physical location of server tree on disk
#    --outputbase OUTPUTBASE     - Directory where output JOBID directory will be created
#    --linkbase LINKBASE         - The web server base link address
#    --jobdatauri JOBDATAURI     - Job Data URI where JOBID directory will exist in web space
#    --matlabparams MATLABPARAMS - Appropriately quoted strings to send as parameters to matlab program
import logging
from subprocess import *
import argparse
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_host = os.environ['NM_EMAIL_HOST']
email_port = os.environ['NM_EMAIL_PORT']


def send_email(subject=None, reply_to='noreply@nanomine.oit.duke.edu', send_to=None,
               text_ver=None, html_ver=None, host=email_host, port=email_port):
    # ref: https://docs.python.org/2/library/email-examples.html

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = reply_to
    msg['To'] = send_to

    text = text_ver
    html = html_ver

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP(host, port)
    s.sendmail(reply_to, send_to, msg.as_string())
    s.quit()



parser = argparse.ArgumentParser(description='MATLAB job argument parser')
parser.add_argument('--jobid', nargs=1)
parser.add_argument('--pgmdir', nargs=1)
parser.add_argument('--pgm', nargs=1)
parser.add_argument('--user', nargs=1)
parser.add_argument('--email', nargs=1)
parser.add_argument('--emailtemplate', nargs=1)
parser.add_argument('--serverbase', nargs=1)
parser.add_argument('--outputbase', nargs=1)
parser.add_argument('--linkbase', nargs=1)
parser.add_argument('--jobdatauri', nargs=1)
parser.add_argument('--matlabparams', nargs='*')

args = parser.parse_args()
logging.error('matlab_job Args: ' + str(args))

try:
    mlparams = ""
    for mlp in args.matlabparams:
        mlparams += '\'' + mlp + '\','
    mlparams = mlparams.rstrip(',')

    #runstr = '\"cd ' + args.serverbase[0] + args.pgmdir[0] + ';' + args.pgm[0] + '(' + mlparams + ');exit;\"'
    runstr = 'cd ' + args.serverbase[0] + args.pgmdir[0] + ';' + args.pgm[0] + '(' + mlparams + ');exit;'
    logging.error('runstr: ' + runstr);
    p = Popen(["matlab", "-nodesktop", "-nodisplay", "-nosplash", "-r", runstr]
              )  # cannot use -nojvm because of functions used
    p.wait()
    ttemplate = args.emailtemplate[0] + '.text'
    htemplate = args.emailtemplate[0] + '.html'

    with open(ttemplate) as ftemplate:
        templatetext = ftemplate.read()
    templatetext = templatetext.format(username=args.user[0], job_id=args.jobid[0], link_base=args.linkbase[0])

    with open(htemplate) as ftemplate:
        templatehtml = ftemplate.read()
    templatehtml = templatehtml.format(username=args.user[0], job_id=args.jobid[0], link_base=args.linkbase[0])

    send_email(subject='NanoMine job - ' + args.jobid[0], reply_to='noreply@nanomine.oit.duke.edu', send_to=args.email[0],
               text_ver=templatetext, html_ver=templatehtml, host=email_host, port=email_port)

except BaseException as be:
    logging.error('Exception running matlab program: ' + str(be))
