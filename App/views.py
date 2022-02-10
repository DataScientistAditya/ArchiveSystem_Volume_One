from ast import If
from django.shortcuts import render, redirect
from .models import Account, UploadDocuments
from .backends import AccountAuth
from django.contrib.auth import  get_user_model, login, logout
from django.contrib import messages
from .forms import Register_Forms, AccountAuthenticationForm,OTP_form,Reset_Password,Reset_Password_Form,UploadDocumentsForm
from django.http import JsonResponse
from .Utility import GetArchiveName,GetArchives
# Create your views here.




def index(request):
    List_of_Url = GetArchives()
    if List_of_Url is not None:
        return render(request,'Landing/Landing.html',{"Pdf_List":List_of_Url})
    else:
        return render(request,'Landing/Landing.html')

    

"""
def about(request):
    return render(request,"about.html")
"""

def Registrations(request):
    context = {}
    if request.POST:
        forms = Register_Forms(request.POST)
        if forms.is_valid():
            forms.save()
            user_email = forms.cleaned_data["email"]
            Is_Verified = Account.objects.all().filter(email = user_email).values("is_email_varified")[0]["is_email_varified"]
            if Is_Verified==False:
                Uuid = Account.objects.all().filter(email = user_email).values("UUid_Token")[0]['UUid_Token']
                AccountAuth.Get_Urls(Recipient=user_email,Token=Uuid)
                return redirect('/Mail_Sent')
            else:
                return redirect("/Login")
        else:
            context['Registration_Form'] = forms
            return render(request, 'CreateAccount/Register.html', context)
    else:
        forms = Register_Forms()
        context['Registration_Form'] = forms
    return render(request, 'CreateAccount/Register.html', context)


def Mail_Sent(request):
    return render(request,"MailSent/MailSent.html")

def Login(request):
    if request.method == "POST":
        Login_form = AccountAuthenticationForm(request.POST)
        if Login_form.is_valid():
            user_email = Login_form.cleaned_data["email"]
            user_password = Login_form.cleaned_data["password"]
            user = AccountAuth.authenticate(Username= user_email, Password= user_password)
            if user is not None:
                user_model = get_user_model()
                user_profile = user_model.objects.get(id = user)
                if user_profile.is_active:
                    Is_Verified = Account.objects.all().filter(id = user).values("is_email_varified")[0]["is_email_varified"]
                    if Is_Verified == True:
                        request.session['uid'] = user_email
                        login(request,user_profile, backend='App.backends.AccountAuth')
                        User_Login_Id = AccountAuth.Get_UserId(user)
                        if User_Login_Id is not None:
                            return redirect('index')
                        else:
                            return redirect('Login')
                    else:
                        Uuid = Account.objects.all().filter(id = user).values("UUid_Token")[0]['UUid_Token']
                        AccountAuth.Get_Urls(Recipient=user_email,Token=Uuid)
                        messages.success(request,"An Email has been Sent to You")
                        Login_form = AccountAuthenticationForm()
                        return render(request,"Login/Login.html",{"Login":Login_form})
            else:
                Login_form = AccountAuthenticationForm()
                return render(request,"Login/Login.html",{"Login":Login_form,"Details":"User Name or Password is not Correct"})
    else:
        Login_form = AccountAuthenticationForm()

    return render(request,"Login/Login.html",{"Login":Login_form})

def Verify(request, Token):
    try:
        Profile_Obj = Account.objects.all().filter(UUid_Token = Token).first()
        if Profile_Obj:
            Account.objects.all().filter(UUid_Token = Token).update(is_email_varified = True)
            messages.success(request,"Your Account has been Verified")
            return redirect("/Login")
    except Exception as e:
        print(e)

def Logout(request):
    #del request.session['uid']
    logout(request=request)
    return redirect("/Login")


def RequestEditPassword(request):
    if request.method == "POST":
        Reset_Pass_Form = Reset_Password_Form(request.POST)
        if Reset_Pass_Form.is_valid():
            Email_Input = Reset_Pass_Form.cleaned_data["Email"]
            try:
                Account_Valided = Account.objects.get(email = Email_Input)
            except:
                Account_Valided = None
            if Account_Valided is not None:
                AccountAuth.Reset_Pass(Recipient=Email_Input,email=Email_Input)
                return redirect("/Mail_Sent")
            else:
                return render(request, "ResetPasswordForm/ResetPassword.html",{"Email_Form":Reset_Pass_Form,"Error":"Account dosent exists"})
        else:
            Reset_Pass_Form = Reset_Password_Form()
            return render(request, "ResetPasswordForm/ResetPassword.html",{"Email_Form":Reset_Pass_Form,"Error":"Please Enter Your Email"})
    else:
        Reset_Pass_Form = Reset_Password_Form()
    return render(request, "ResetPasswordForm/ResetPassword.html",{"Email_Form":Reset_Pass_Form})
    
    
def Reset(request,Email):
    if request.method == "POST":
        Reset_pass = Reset_Password(request.POST)
        if Reset_pass.is_valid():
            Passw_One = Reset_pass.cleaned_data["Password_one"]
            Passw_Two = Reset_pass.cleaned_data["Password_two"]
            Password_Valid = AccountAuth.Check_Pass(Pass_One=Passw_One, Pass_Two= Passw_Two)
            if Password_Valid is not None:
                try:
                    Account.objects.all().filter(email = Email).update(password = Password_Valid)
                    return redirect("/Login")
                except:
                    pass
            else:
                Reset_pass = Reset_Password()
                return render(request, "ResetPas/ResetPass.html",{"Email_Form":Reset_pass})
        else:
            Reset_pass = Reset_Password()
            return render(request, "ResetPass/ResetPass.html",{"Email_Form":Reset_pass})
    else:
        Reset_pass = Reset_Password()
    return render(request, "ResetPass/ResetPass.html",{"Email_Form":Reset_pass})


def Autosuggest(request):
    try:
        Query = request.GET
        Query_Terms = Query.get('term')
        Results = GetArchiveName(Ar_Name= Query_Terms)
        if Results is not None:
            Product_Names = Results[0]
            Autocomplete_List = []
            if Product_Names is not None:
                for i in Product_Names:
                    Autocomplete_List.append(i)
                return JsonResponse(Autocomplete_List,safe=False)
    except:
        return JsonResponse([],safe=False)


def Upload(request):
    try:
        Username = request.user.username
        return redirect("UploadDocs/{}".format(Username))
    except:
        pass
    return redirect("index")
    


def UploadDocs(request, Username):
    if request.user.id == None:
        return redirect("index")
    else:
        context = {}
        if request.method == "POST":
            Id =  Account.objects.all().filter(username = Username).values("id")[0]["id"]
            UploadForm = UploadDocumentsForm(request.POST, request.FILES)
            if UploadForm.is_valid():
                """
                    "Document","Thumbnail", "Category", "Language"
                """
                Docs = request.FILES["Document"]
                Thmbnl = request.FILES["Thumbnail"]
                Cats = UploadForm.cleaned_data["Category"]
                Langs = UploadForm.cleaned_data["Language"]
                Auth_user = Account.objects.filter(id = Id )[0]
                print("AuthUser is",Auth_user)
                Data = UploadDocuments(UserId=Auth_user,Document = Docs,Thumbnail = Thmbnl,Category = Cats,Language = Langs  )
                Data.save()
                Sucess = "Sucessfully Uploaded"
                print(Sucess)
                return render(request,"SuccessUpload/SucessUpload.html",context)
            else:
                Error = "Not Uploaded"
                print(Error)
                context["UploadForm"] = UploadForm
                UploadForm = UploadDocumentsForm(request.POST, request.FILES)
                return render(request,"UploadForm/UploadForm.html",context)
        else:
            Error = "Not Valid Request"
            print(Error)
            UploadForm = UploadDocumentsForm(request.POST, request.FILES)
            context["UploadForm"] = UploadForm
        return render(request,"UploadForm/UploadForm.html",context)
