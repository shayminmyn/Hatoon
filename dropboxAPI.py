import pathlib
import dropbox
import re


class DropBoxAPI:
    def __init__(self,token):
        self.token = token
    
    def upload(self,filePath):
        drb = dropbox.Dropbox(self.token)
        path = pathlib.Path(filePath)
        filename = path.name
        target = "/cartoon/"              # the target folder
        targetfile = target + filename   # the target path and file name
        with path.open("rb") as f:
            # upload gives you metadata about the file
            # we want to overwite any previous version of the file
            meta = drb.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
        link = drb.sharing_create_shared_link(targetfile)

        # url which can be shared
        url = link.url

        # link which directly downloads by replacing ?dl=0 with ?dl=1
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        return dl_url



# d = DropBoxAPI('XfH4_Pu0F6gAAAAAAAAAAQ-40jVLAMkRrnkX1BFgBUNdB5dsGQ6ntCQtquIGoIWQ')
# d.upload('static/cartoonize/fd4aed92-7e98-4312-be9d-e4407aea1e8d.jpg_cartoon.jpg')
# # the source file
# folder = pathlib.Path(".")    # located in this folder
# filename = "test.txt"         # file name
# filepath = folder / filename  # path object, defining the file

# # target location in Dropbox
# target = "/Temp/"              # the target folder
# targetfile = target + filename   # the target path and file name

# # Create a dropbox object using an API v2 key
# d = dropbox.Dropbox(your_api_access_token)

# # open the file and upload it
# with filepath.open("rb") as f:
#    # upload gives you metadata about the file
#    # we want to overwite any previous version of the file
#    meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))

# # create a shared link
# link = d.sharing_create_shared_link(targetfile)

# # url which can be shared
# url = link.url

# # link which directly downloads by replacing ?dl=0 with ?dl=1
# dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
# print (dl_url)