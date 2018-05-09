# Run matlab
# Accepts parameters for
#     matlab proc name
#     matlab paramstr
#     username
#     email
#     email template name
#     server base directory
#     output base directory

# A Job id will be created and used to create the directory at the output path specified where files will be placed.
#     The output directory should be in the static/JOB_DATA path to ensure that Apache can find the files for linking
# The job id will be returned so that it can be displayed to the user.

# Before returning, the runner will kick off a matlab_job instance with the jobid and other parameters to actually
#   execute matlab and generate the email

import os
import uuid
import matlab_job
import logging

def formatparams(parms) :
    s = ""
    for p in parms:
        s += ("'" + p + "',")
    s = s.rstrip(',')
    return s


def matlab_runner(matlab_pgm_dir, matlab_pgm, matlab_pgm_params, username, email, email_template_name, server_base, output_base,link_base) :

    # create jobid as matlab-UUID
    jobid = 'matlab'+str(uuid.uuid4())

    logging.info('        MATLAB proc: ' + matlab_pgm)
    logging.info('     MATLAB pgm dir: ' + matlab_pgm_dir)
    logging.info('   MATLAB pgm parms: '.join(matlab_pgm_params))
    logging.info('           username: ' + username)
    logging.info('              email: ' + email)
    logging.info('email_template_name: ' + email_template_name)
    logging.info('       server_base : ' + server_base)
    logging.info('        output_base: ' + output_base)
    logging.info('          link_base: ' + link_base)
    logging.info('              jobid: ' + jobid)

    matlab_base_params = '-nodesktop -nodisplay -nosplash -r ' + '\'cd ' + server_base + '/' + matlab_pgm_dir + ';' + matlab_pgm + \
                         formatparams(matlab_pgm_params)
    logging.info('built params: ' + matlab_base_params) #this is incomplete, but need to get path working to test this
    #execute matlab job in the background
    return jobid
