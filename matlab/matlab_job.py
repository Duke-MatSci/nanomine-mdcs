# Run a matlab job
# Accepts parameters for
#     jobid
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
# The email template will be filled in with the username, email, job id and link to output files.

def matlab_job(matlab_proc, matlab_param_str, username, email, email_template_name, server_base, output_base) :
    # create jobid as UUID '.' datetime
    # Read email template into memory and replace parameters




