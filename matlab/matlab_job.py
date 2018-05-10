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
import subprocess
import argparse
import os


email_server = os.environ['NM_EMAIL_HOST']
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

args =  parser.parse_args()
print('Args: ' + str(args))

try:
    mlparams = ""
    for mlp in args.matlabparams:
        mlparams += '\''+mlp+'\','
    mlparams = mlparams.rstrip(',')

    runstr = '\"cd ' + args.serverbase[0] + args.pgmdir[0] +';' + args.pgm[0] + '(' + mlparams + ');exit;\"'
    print('runstr: ' + runstr);
    p = subprocess.Popen(["echo","-nodesktop","-nodisplay","-nosplash","-nojvm","-r",runstr],shell=True)
    p.wait()
    with open( args.emailtemplate[0] ) as ftemplate:
        templatetext = ftemplate.read()
    print(templatetext)
except BaseException as be:
    logging.error('Exception running matlab program: ' + str(be))


