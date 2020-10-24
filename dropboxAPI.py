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

