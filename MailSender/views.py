import smtplib, ssl
import os


from multiprocessing import context
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import MailAddress

port = 587 #For starttls
smtp_server = "smtp.gmail.com"
sender_email = "bdio59101@gmail.com"
password = "5BL4wu8CqAfWbPA"

class IndexView(generic.ListView):
    template_name = 'MailSender/index.html'
    context_object_name = 'mail_address_list'

    def get_queryset(self):
        """
        Return the list of mail address
        """
        return MailAddress.objects.all()

def send(request):
    text = request.POST['messageText']
    if text == '':
        return render(request, 'MailSender/index.html',{
            'mail_address_list': MailAddress.objects.all(),
            'error_message': "Empty email text",
        })
    else:
        context = ssl.create_default_context()
        for email in MailAddress.objects.all().values_list():
            print(email[1])
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, email[1], text)
        return render(request, 'MailSender/index.html',{
            'mail_address_list': MailAddress.objects.all(),
            'error_message': "Mail mandate?",
        })