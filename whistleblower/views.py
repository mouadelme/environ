import smtplib

from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from .models import User, is_admin_group
from .models import UploadFile
from whistleblower.forms import FileForm
import boto3
from django.contrib.auth.decorators import login_required, user_passes_test


from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.timezone import localtime



def default(request):
    return HttpResponse("If you're seeing this the app is running properly")


class Question:
    objects = None


def home(request):
    return render(request, "whistleblower/home.html", {"is_admin": is_admin_group(request.user)})


def upload_form(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        data = request.POST.copy()

        if request.user.is_authenticated:
            data['email'] = request.user.email
            data['username'] = request.user.username
        else:
            data['email'] = ''
            data['username'] = ''

        data['public'] = 'public' in request.POST

        form = FileForm(data, request.FILES)

        if form.is_valid() and (request.FILES.get('picture') != None or data.get('reason') != ""):
            form.save()
            if request.user.is_authenticated:
                email = request.user.email
                if email.strip():
                    file_name = request.FILES['picture'].name if 'picture' in request.FILES else 'No file uploaded'
                    submission_time = timezone.now()
                    message = "Your submission has been successfully submitted!"
                    send("Submission Successful", message, [email], file_name=file_name, submission_time=submission_time)

            context = {'form': form, "is_admin": is_admin_group(request.user), 'form_success': True}
            return render(request, 'whistleblower/filehtml.html', context)

        else:
            context = {'form': form, "is_admin": is_admin_group(request.user)}
            if not form.is_valid():
                context['form_error'] = True
            else:
                context['nosub_error'] = True
            return render(request, 'whistleblower/filehtml.html', context)

    else:
        context = {'form': FileForm(), "is_admin": is_admin_group(request.user)}
        return render(request, 'whistleblower/filehtml.html', context)


def logout_view(request):
    logout(request)
    return redirect("/")


def auth(request):
    if request.user.is_authenticated:
        rank = "Layman"
        num = UploadFile.objects.filter(username=request.user.username).filter(status="R").count()
        if num < 5:
            rank = "Layman"
        elif num < 10:
            rank = "Green Thumb"
        else:
            rank = "Environmentalist"
        if is_admin_group(request.user):  # request.user.is_admin:
            return render(request, "whistleblower/admin_home.html", {"is_admin": is_admin_group(request.user), "rank": rank, "num": num})
        else:
            return render(request, "whistleblower/home.html", {"is_admin": is_admin_group(request.user), 'num': num, 'rank': rank})
    else:
        return render(request, "whistleblower/login.html", {"is_admin": is_admin_group(request.user)})


@login_required
@user_passes_test(is_admin_group)
def files(request, order='date_oldest'):
    # Don't need to call the amazon thing anymore, but have it here just in case -Karan
    # s3 = boto3.resource('s3',
    #                     aws_access_key_id='AKIAZI2LCDZPIJ4I2TU6',
    #                     aws_secret_access_key='YvrdWkz/TvsRUm0BLTcD4PFWp56IIfIgrfa3pG+b')
    #
    # bucket_name = 'whistleblowerapp'  # replace with your bucket name
    #
    # objects = [{'key': obj.key, 'last_modified': obj.last_modified} for obj in s3.Bucket(bucket_name).objects.all()]
    objects = None

    if order == 'date_oldest':
        uploaded_Files = UploadFile.objects.all().order_by('date')
    elif order == 'date_newest':
        uploaded_Files = UploadFile.objects.all().order_by('-date')
    else:
        uploaded_Files = UploadFile.objects.all().order_by('-date')

    return render(request, "whistleblower/file_looker.html",
                  {'objects': objects, "is_admin": is_admin_group(request.user), 'uploaded_files': uploaded_Files})


@login_required
@user_passes_test(is_admin_group)
def files_view(request, file_id):

    form_success = False

    ##form handling
    if request.method == 'POST':
        explanation = request.POST['explanation']
        if explanation != None:
            current_file = UploadFile.objects.get(id=file_id)
            current_file.explanation = explanation
            current_file.status = 'R'
            current_file.save()

            email = current_file.email
            if email.strip():
                try:
                    message = "Your submission has now been updated to Resolved! Log in to see your message"
                    send("Update on Submission", message, [email], file_name=current_file.picture.name, submission_time=current_file.date)
                except smtplib.SMTPException as e:
                    print("Failed to send email:", e)
            current_file.save()
            form_success = True

    ##done with form handling


    uploaded_Files = UploadFile.objects.all()

    current_file = UploadFile.objects.get(id=file_id)
    filename = current_file.picture.name

    file_url = 'https://whistleblowerapp.s3.us-east-2.amazonaws.com/' + filename

    if current_file.status == 'New':
        current_file.status = 'IP'

        email = current_file.email
        if email.strip():
            try:
                message = "Your submission has now been updated to In Progress!"
                send("Update on Submission", message, [email], file_name=current_file.picture.name, submission_time=current_file.date)
            except smtplib.SMTPException as e:
                print("Failed to send email:", e)
        current_file.save()

    # print(current_file.status)
    if filename.endswith('.pdf'):
        file_type = 'pdf'
    elif filename.endswith('.jpg'):
        file_type = 'jpg'
    elif filename.endswith('.txt'):
        file_type = 'txt'
    else:
        file_type = 'none'

    return render(request, "whistleblower/file_review.html",
                  {"is_admin": is_admin_group(request.user), 'uploaded_files': uploaded_Files, 'file_name': filename,
                   'file_url': file_url, 'file_type': file_type, "current_file": current_file,
                   'form_success': form_success, 'file_id': file_id})

@login_required
def my_submissions(request, order='date_asc'):
    if order == 'date_newest':
        users_submissions = UploadFile.objects.filter(username=request.user.username).order_by('-date')
    elif order == 'date_oldest':
        users_submissions = UploadFile.objects.filter(username=request.user.username).order_by('date')
    else:
        users_submissions = UploadFile.objects.filter(username=request.user.username).order_by('-date')



    return render(request, "whistleblower/my_submissions.html",
                  {"is_admin": is_admin_group(request.user), 'uploaded_files': users_submissions})

def about_page(request):

    return render(request, "whistleblower/about.html",
                  {"is_admin": is_admin_group(request.user)})

def current_report(request, order='date_asc'):
    if order == 'date_newest':
        users_submissions = UploadFile.objects.filter(public=True).order_by('-date')
    elif order == 'date_oldest':
        users_submissions = UploadFile.objects.filter(public=True).order_by('date')
    else:
        users_submissions = UploadFile.objects.filter(public=True).order_by('-date')

    return render(request, "whistleblower/reports.html",
                  {"is_admin": is_admin_group(request.user), 'uploaded_files': users_submissions})

def send(subject, message, recipients, file_name=None, submission_time=None):
    if file_name and submission_time:
        message += f"\n\nFile Submitted: {file_name}\nSubmitted At: {timezone.localtime(submission_time).strftime('%Y-%m-%d %H:%M:%S')}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients
    )

def custom_404(request, exception):
    response = render(request, 'whistleblower/404.html')
    response.status_code = 404
    return response


@login_required
def delete_submission(request, submission_id):
    submission = get_object_or_404(UploadFile, id=submission_id, username=request.user.username)
    try:
        if submission.picture:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            file_key = submission.picture.name
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)

        submission.delete()
        messages.success(request, "Submission has been deleted.")
    except Exception as e:
        messages.error(request, "An error occurred while attempting to delete the submission.")

    return redirect('my_submissions')

@login_required
def my_submissions_newest(request):
    # Get the submissions for the current user, ordered by date descending (newest first)
    users_submissions = UploadFile.objects.filter(username=request.user.username).order_by('-date')
    # Render the my_submissions.html template with the sorted submissions
    return render(request, "whistleblower/my_submissions.html", {
        "is_admin": is_admin_group(request.user),
        "uploaded_files": users_submissions
    })

@login_required
def my_submissions_oldest(request):
    # Get the submissions for the current user, ordered by date ascending (oldest first)
    users_submissions = UploadFile.objects.filter(username=request.user.username).order_by('date')
    # Render the my_submissions.html template with the sorted submissions
    return render(request, "whistleblower/my_submissions.html", {
        "is_admin": is_admin_group(request.user),
        "uploaded_files": users_submissions
    })
