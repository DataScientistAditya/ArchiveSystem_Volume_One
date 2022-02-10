from .models import UploadDocuments



def GetArchiveName(Ar_Name):
    pass

def GetArchives():
    try:
        List=[]
        Image_List = UploadDocuments.objects.all().values("Thumbnail")
        for i in Image_List:
            Media_Link = "../../media/{}".format(i['Thumbnail'])
            List.append(Media_Link)
        return List
    except:
        return None