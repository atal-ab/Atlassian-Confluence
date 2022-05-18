
from atlassian import Confluence        #confluence
import requests                         #downlaoding files
import os                               #folder and path
import glob                             #delete files lib


#auth credentials
confluence = Confluence(
    url="https://wiki-address",
    username='username',
    password="password")


#main function
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
    count_attach = 0
 
    while flag:
        values = confluence.get_all_pages_from_space(space=space, start=limit * step, limit=limit)
        step += 1
        if len(values) == 0:
            flag = False
            print("No pages any more or check permissions")
        else:
            #Create directory for the current space with the space name and download the pages in to that dir.
            dirName = str(getSpaceWithKey(space))
            try:
                os.makedirs(dirName)    
                #print("Directory " , dirName ,  " Created ")
                os.chdir(dirName)
            except FileExistsError:
                #print("Directory " , dirName ,  " already exists")
                os.chdir(dirName)
                #delete old files if they exists
                files = glob.glob('')
                for f in files:
                    os.remove(f)
                #print("All files inside", dirName, " are deleted")

            #start downloading Pages
            for value in values:                                                           
                #print("Page ID: " + value['id'] + " Page title: " + value['title']) 
                page = confluence.get_page_by_id(page_id=value['id'])
                pageId = value['id']  
                #the function creates pdf from byte-stream responce and save the page as pdf, named with pageID
                def save_file(content):
                    file_pdf = open(pageId, 'wb')
                    file_pdf.write(content)
                    file_pdf.close()
                    #print("downloaded Page: " + value['title'])
                #Get your confluence page as byte-stream
                response = confluence.get_page_as_pdf(page['id'])
                save_file(content=response) 
                content_ids.append(pageId) 
            
            #start downloading attachments in attachments dir
            #print('Start downloading new attachements')
            dirAttach = 'attachments'
            try:
                os.makedirs(dirAttach)
                os.chdir(dirAttach)
            except FileExistsError:
                #print(dirAttach + " directory is already exists ")
                os.chdir(dirAttach)
                #delete old files if they exists
                files = glob.glob('')
                for f in files:
                    os.remove(f)
                #print("All old Files are deleted from: " + dirAttach)
            for value in values:
                #print("Page ID: " + value['id'] + " Page title: " + value['title'])
                attachments_container = confluence.get_attachments_from_content(page_id=value['id'] ,start=0, limit=500)
                attachments = attachments_container['results']
                
                for attachment in attachments:
                    fileName = attachment['title']
                    download_link = confluence.url + attachment['_links']['download']
                    r = requests.get(download_link, auth=(confluence.username, confluence.password))
                    if r.status_code == 200:
                        with open(fileName, "wb") as f:
                            for bits in r.iter_content():
                                f.write(bits)
                        count_attach +=1
            #exit from current aattachments directory
            os.chdir('../')
            #end downlaoding attachments


            #exit from current Space folder
            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)
            
    print("Found in space {}:  \n[ {} ] Pages  \n[ {} ] Attachments ".format(space, len(content_ids), count_attach))
    print('--All Pages and Attachments are downloaded seccessfully--\n')
    
    return content_ids, count_attach



#get wiki space list 
spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
spaceWikilist = spaces['results']

#downlaod files from whole wiki
def downloadWikiContent(wikiList):
    for space in wikiList:
        getFiles(space['key'])            

#call the function
downloadWikiContent(spaceWikilist)