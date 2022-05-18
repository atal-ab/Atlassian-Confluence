from re import S
from atlassian import Confluence        #confluence
import requests                         #downlaoding files
import os                               #folder and path
import glob                             #delete files lib
 

#auth credentials
confluence = Confluence(
    url="https://wiki-address",
    username='username',
    password="password")



def getFiles(space):

    #return the name of space to create a folder with that space name.
    spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
    spacelist = spaces['results']
    def getSpaceWithKey (spaceKey):
        for space in spacelist:
            skey = space['key']
            if spaceKey == skey:
                return space['name']
        
    limit = 500
    flag = True
    step = 0
    content_ids = []
 
    while flag:
        values = confluence.get_all_pages_from_space(space=space, start=limit * step, limit=limit)
        step += 1
        if len(values) == 0:
            flag = False
            print("Did not find any pages, please, check permissions")
        else:
            #Create directory for the current space with the space name and download the files in to that dir.
            dirName = str(getSpaceWithKey(space))
            dirAttach = 'attachments'
            try:
                os.makedirs(dirName)    
                print("Creating directory: " + dirName)
                os.chdir(dirName)
                os.makedirs(dirAttach)
                os.chdir(dirAttach)
            except FileExistsError:
                print(dirName + " directory is already exists")
                os.chdir(dirName)
                try:
                    os.makedirs(dirAttach)
                    print("Creating directory: " + dirAttach)
                    os.chdir(dirAttach)
                except:
                    print(dirAttach + " directory is already exists ")
                    os.chdir(dirAttach)
                    #delete old files if they exists
                    files = glob.glob('')
                    for f in files:
                        os.remove(f)
                    print("All old Files are deleted from: " + dirAttach)
                
            print('Start downloading new attachements')
            for value in values:
                #print("Page ID: " + value['id'] + " Page title: " + value['title'])
                attachments_container = confluence.get_attachments_from_content(page_id=value['id'] ,start=0, limit=500)
                attachments = attachments_container['results']
                
                #download files from onlyPDF list
                for attachment in attachments:
                    fileName = attachment['title']
                    download_link = confluence.url + attachment['_links']['download']
                    r = requests.get(download_link, auth=(confluence.username, confluence.password))
                    if r.status_code == 200:
                        with open(fileName, "wb") as f:
                            for bits in r.iter_content():
                                f.write(bits)
                content_ids.append((value['id']))
            #exit from current folder and go back to home dir
            os.chdir("../../")
    print("Found in space {} pages {}".format(space, len(content_ids)))
    return content_ids 


#space keys list
spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
spaceWikilist = spaces['results']

#downlaod files from who wiki
def downloadAttachments(wikiList):
    for space in wikiList:
        getFiles(space['key'])            

#call the function
downloadAttachments(spaceWikilist)