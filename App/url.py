from django.urls import path
from . import views


urlpatterns = [
    path("",views.index, name="index"),
    #path("About", views.about, name="about"),
    path("Login", views.Login, name="Login"),
    path("Register", views.Registrations, name="Register"),
    path("Logout", views.Logout, name="Logout"),
    path("Mail_Sent",views.Mail_Sent,name="Mail_Sent"),
    path("Verify/<Token>",views.Verify, name="Verify"),
    path("RequestEditPassword",views.RequestEditPassword,name="RequestEditPassword"),
    path("Reset/<Email>",views.Reset,name="Reset"),
    path("Autosuggest",views.Autosuggest,name="Autosuggest"),
    path("Upload",views.Upload,name="Upload"),
    path("UploadDocs/<Username>",views.UploadDocs,name="UploadDocs"),
]