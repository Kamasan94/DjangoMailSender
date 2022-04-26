import sendgrid
import os


from multiprocessing import context
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from models import MailAddress
from sendgrid.helpers.mail import Mail, Email, To, Content

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
        my_sg = sendgrid.SendGridAPIClient('......IeltIytmFYeQ0aSOt2UBYvv2E6Xh...')
        # Change to your verified sender
        from_email = Email("pooldaimon94@gmail.com")  

        # Change to your recipient
        for email in MailAddress.objects.all():
            to_email = To(email.address)  

            subject = "Lorem ipsum dolor sit amet"
            content = Content("text/plain", text)

            mail = Mail(from_email, to_email, subject, content)

            # Get a JSON-ready representation of the Mail object
            mail_json = mail.get()

            # Send an HTTP POST request to /mail/send
            response = my_sg.client.mail.send.post(request_body=mail_json)
