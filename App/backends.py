from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Account
from django.core.mail import send_mail
from django.conf import settings


class AccountAuth(ModelBackend):

    def authenticate(Username=None, Password = None):
        UserModel = get_user_model()
        if Username is not None:
            try:
                id = UserModel.objects.all().filter(email = Username).values("id")[0]["id"]
            except:
                return None
        if id is not None:
            try:
                user_pass = UserModel.objects.all().filter(id = id).values("password")[0]['password']
                if user_pass == Password:
                    return id
            except:
                return None
        
        else:
            return None
    
    def get_user(self,id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk= id) # <-- must be primary key and number
        except User.DoesNotExist:
            return None


    def Get_Urls(Recipient, Token):
        Subject = "MightyNeurons Email Verification"
        Message = f"Your Account Needs to Be Verified http://127.0.0.1:8000/Verify/{Token}"
        Email_Sender = settings.EMAIL_HOST_USER
        Email_Reciever = [Recipient]
        send_mail(subject=Subject, message=Message, from_email=Email_Sender, recipient_list=Email_Reciever)
        
    def Reset_Pass(Recipient, email):
        try:
            Subject = "MightyNeurons Email Verification"
            Message = f"Reset Your Password Here, http://127.0.0.1:8000/Reset/{email}"
            Email_Sender = settings.EMAIL_HOST_USER
            Email_Reciever = [Recipient]
            send_mail(subject=Subject, message=Message, from_email=Email_Sender, recipient_list=Email_Reciever)
        except:
            return None
    
    def Check_Pass(Pass_One, Pass_Two):
        if Pass_One == Pass_Two:
            return Pass_One
        else:
            return None

    def Get_UserId(Userid):
        try:
            Id = Account.objects.all().filter(id = Userid).values("id")[0]["id"]
            return Id
        except:
            return None