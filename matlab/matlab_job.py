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


def send_email(**kwargs):
    #ref: https://docs.python.org/2/library/email-examples.html

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

    s = smtplib.SMTP(email_host, email_port)
    s.sendmail(reply_to, send_to, msg.as_string())
    s.quit()


email_host = os.environ['NM_EMAIL_HOST']
email_port = os.environ['NM_EMAIL_PORT']

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

    runstr = '\"cd ' + args.serverbase[0] + args.pgmdir[0] + ';' + args.pgm[0] + '(' + mlparams + ');exit;\"'
    logging.error('runstr: ' + runstr);
    p = Popen(["echo", "-nodesktop", "-nodisplay", "-nosplash", "-nojvm", "-r", runstr],
              shell=True)  # change echo to matlab and remove shell=True
    p.wait()
    ttemplate = args.emailtemplate[0] + '.text'
    htemplate = args.emailtemplate[0] + '.html'

    with open(ttemplate) as ftemplate:
        templatetext = ftemplate.read()
    templatetext = templatetext.format(username=args.user[0], job_id=args.jobid[0], link_base=args.linkbase[0])

    with open(htemplate) as ftemplate:
        templatehtml = ftemplate.read()
    templatehtml = templatehtml.format(username=args.user[0], job_id=args.jobid[0], link_base=args.linkbase[0])

    send_email(subject='NanoMine job' + args.jobid[0], replyto='noreply@nanomine.oit.duke.edu', sendto=args.email[0],
               textver=templatetext, htmlver=templatehtml, email_host=email_host, email_port=email_port)

except BaseException as be:
    logging.error('Exception running matlab program: ' + str(be))
