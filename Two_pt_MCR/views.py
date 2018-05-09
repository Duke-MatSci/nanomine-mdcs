from django.shortcuts import render_to_response, render, RequestContext, redirect
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from time import gmtime, strftime, localtime

from django.template import Context
from contextlib import contextmanager

from Two_pt_MCR.models import Document
from Two_pt_MCR.forms import *
from matlab_runner import *

import xmltodict
import os
import subprocess
import scipy.io


# Create your views here.


def Reconstruction_Choice(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('MCR_Reconstruction_Choice.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def submit_image(request):
    if request.user.is_authenticated():
        # Handle file upload
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = Document(docfile=request.FILES['docfile'])
                newdoc.save()
                file = request.FILES['docfile']
                server_base = os.environ['NM_SERVER_DIR']
                output_base = os.environ['NM_JOB_DATA']
                work_dir = server_base
                #os.chdir(work_dir)
                #os.system('pwd')
                user_email_id = request.POST['email_id']
                if not user_email_id:
                    return HttpResponse(
                        '<h3>Please provide an email address to receive Job ID!</h3>')  # if no email id was provided, report error
                input_type = request.POST['Characterize_input_type']
                if input_type == "1":
                    #p=re.compile('.*(\\.([Jj][Pp][Gg])|([Tt][Ii][Ff])|([Pp][Nn][Gg]))$'); p.match(str(file))
                    if not str(file).lower().endswith(".jpg"):
                        if not str(file).lower().endswith(".tif"):
                            if not str(file).lower().endswith(".png"):
                                return HttpResponse(
                                    '<h3>Please upload a JPEG file</h3>')  # report wrong file format
                elif input_type == "2":
                    if not str(file).lower().endswith(".zip"):
                        return HttpResponse('<h3>Please upload ZIP  file</h3>')  # report wrong file format
                else:
                    if not str(file).lower().endswith(".mat"):
                        return HttpResponse('<h3>Please upload .mat file</h3>')  # report wrong file format

                user_name = None
                user_name = request.user.username
                num_recon = request.POST['num_recon']
                correlation_choice = request.POST['correlation_choice']
                # Run MATLAB when file is valid
                """ed151 - replaced
                os.system(
                    'matlab -nodesktop -nodisplay -nosplash -r "cd '+work_dir+'/Two_pt_MCR/mfiles;run_2ptMCR(\'"' + str(
                        user_name) + '"\',"' + str(num_recon) + '","' + str(input_type) + '","' + str(
                        correlation_choice) + '",\'"' + str(file) + '"\');exit"')
                # if user_email_id:
                mail_to_user = 'echo sendmail ' + user_email_id + ' < '+work_dir+'/Two_pt_MCR/email.html'
                os.system(mail_to_user)
                #os.system('sendmail back2akshay@gmail.com < /home/NANOMINE/Production/mdcs/Two_pt_MCR/email.html')
                """

                job_data_uri = os.environ['NM_JOB_DATA_URI']
                link_base = os.environ['NM_WEB_ADDR']

                matlab_pgm_dir = '/Two_pt_MCR/mfiles'
                matlab_pgm = 'run_2ptMCR'
                email_template_name = 'two_pt_mcr_email.html'
                jobid = get_job_id()
                matlab_params = (str(user_name), str(num_recon), str(input_type), str(correlation_choice),
                                       str(file), str(output_base), str(server_base), str(jobid))

                # NOTE: matlab_runner will format and send the email after the matlab program completes
                matlab_runner(jobid,
                        user_name,
                        user_email_id, email_template_name, server_base, output_base, link_base, job_data_uri,matlab_pgm_dir, matlab_pgm, 
                        matlab_params, #list should be in same order as expected by matlab program
                        )


                form = DocumentForm()
                documents = Document.objects.all()
                return render_to_response('Two_pt_MCR_submission_notify.html', {'jobid': jobid,'documents': documents, 'form': form},
                                          context_instance=RequestContext(request))
            else:
                form = DocumentForm()
                documents = Document.objects.all()
                return HttpResponse('<h3>Please upload an image!</h3>')  # if no image was uploaded, report error

        else:
            form = DocumentForm()  # A empty, unbound form

        # Load documents for the list page
        documents = Document.objects.all()
        # Render list page with the documents and the form
        return render_to_response(
            'Two_pt_MCR_submit_image.html',
            {'documents': documents, 'form': form},
            context_instance=RequestContext(request)
        )
    else:
        return redirect('/login')


def landing(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('MCR_landing.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return redirect('/login')


def checkResult(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('Two_pt_MCR_Check_Result.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return redirect('/login')


def viewResult(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('Two_pt_MCR_view_result.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def submission_notify(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('Two_pt_MCR_submission_notify.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return '/login'


def Characterize_Choice(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('MCR_Characterize_Choice.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def Characterize_Check_Result(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('MCR_Characterize_Check_Result.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def Characterize_view_result(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('MCR_Characterize_view_result.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def Characterize(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = Document(docfile=request.FILES['docfile'])
                newdoc.save()

                user_email_id = request.POST['email_id']
                if not user_email_id:  # if no email provided, report error
                    return HttpResponse('<h3>Please provide an email address to receive Job ID!</h3>')
                work_dir = os.environ['NM_HOME']
                os.chdir(work_dir)
#                os.system('pwd')
                file = request.FILES['docfile']  # get name of incoming file
                print type(str(file))
                input_type = request.POST['Characterize_input_type']
                if input_type == "1":
                    if not str(file).endswith(".jpg"):
                        if not str(file).endswith(".JPG"):
                            if not str(file).endswith(".tif"):
                                if not str(file).endswith(".png"):
                                    if not str(file).endswith(".PNG"):
                                        if not str(file).endswith(".TIF"):
                                            return HttpResponse(
                                                '<h3>Please upload a file in supported format (.jpg, .tif, .png)</h3>')  # report wrong file format
                elif input_type == "2":
                    if not str(file).endswith(".zip"):
                        return HttpResponse(
                            '<h3>Please upload ZIP  file</h3>')  # report wrong file format
                else:
                    if not str(file).endswith(".mat"):
                        return HttpResponse('<h3>Please upload .mat file</h3>')  # report wrong file format

                correlation_choice = request.POST['correlation_choice']
                user_name = None
                user_name = request.user.get_username()
                print (user_name)
                # Run MATLAB when file is valid
                os.system(
                    'matlab -nodesktop -nodisplay -nosplash -r "cd '+work_dir+'/Two_pt_MCR/mfiles;Characterize(\'"' + user_name + '"\',"' + str(
                        input_type) + '","' + str(correlation_choice) + '",\'"' + str(file) + '"\');exit"')

                mail_to_user = 'echo sendmail ' + user_email_id + ' < '+work_dir+'/Two_pt_MCR/email.html'
                os.system(mail_to_user)
                #os.system('sendmail back2akshay@gmail.com < /home/NANOMINE/Production/mdcs/Two_pt_MCR/email.html')
                form = DocumentForm()
                documents = Document.objects.all()
                return render_to_response("MCR_Characterize_Check_Result.html", {'documents': documents, 'form': form},
                                          context_instance=RequestContext(request))
            else:
                return HttpResponse('<h3>Please upload an image!</h3>')  # if no image was uploaded, report error
        else:
            form = DocumentForm()
            documents = Document.objects.all()
            return render_to_response('Two_pt_MCR_Characterize.html', {'documents': documents, 'form': form},
                                      context_instance=RequestContext(request))
    else:
        return ('/login')


def Correlation_Fundamentals(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('MCR_Correlation_Fundamentals.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def SDF(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('SDF.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def Result_interpretation(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('MCR_Results_interpretation.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')


def time_estimate(request):
    if request.user.is_authenticated():
        form = DocumentForm()
        documents = Document.objects.all()
        return render_to_response('Two_pt_MCR_time_estimate.html', {'documents': documents, 'form': form},
                                  context_instance=RequestContext(request))
    else:
        return ('/login')
