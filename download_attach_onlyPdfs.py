from atlassian import Confluence        #confluence
import requests                         #downlaoding files
import os                               #folder and path
import glob                             #delete files lib
 

#auth credentials
confluence = Confluence(
    url="https://wiki-Address",
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
            try:
                os.makedirs(dirName)    
                print("Creating directory: " + dirName)
                os.chdir(dirName)
            except FileExistsError:
                print(dirName + " directory is already exists ")
                os.chdir(dirName)
                #delete old files if they exists
                files = glob.glob('')
                for f in files:
                    os.remove(f)
                print("All old Files are deleted from: " + dirName)
            print('Start downloading up to dated pages')
            for value in values:
                #print("Page ID: " + value['id'] + " Page title: " + value['title'])
                attachments_container = confluence.get_attachments_from_content(page_id=value['id'] ,start=0, limit=500)
                attachments = attachments_container['results']
                
                #list all attachments and extract only files ending with .pdf
                onlyPDFList = [] 
                for attachment in attachments:
                    if attachment['title'].endswith('.pdf'):
                        onlyPDFList.append(attachment)
                        #print(attachment['title'])        
            
                #download files from onlyPDF list
                for pdf in onlyPDFList:
                    pdfName = pdf['title']
                    download_link = confluence.url + pdf['_links']['download']
                    r = requests.get(download_link, auth=(confluence.username, confluence.password))
                    if r.status_code == 200:
                        with open(pdfName, "wb") as f:
                            for bits in r.iter_content():
                                f.write(bits)
                content_ids.append((value['id']))
            #exit from current folder and go back to home dir
            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)
            #os.chdir("../")
    print("Found in space {} pages {}".format(space, len(content_ids)))
    return content_ids 


#you can create you own list with space keys and the function below will downlaod only from these given spaces
spaceKeyGivenList = [ 'fgf','ITSZIM','HHU', 'DATS', 'ALMA','fsphysik', 'WAW', 'OPENVPN']

#get all wiki spaces
spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
spaceWikilist = spaces['results']

                
def downloadPDF(givenList, wikiList):
    #check if the given space names are exist, if not then ignore it and continue ot the next one
    for space in wikiList:
        skey = space['key']
        for gskey in givenList:
            if skey == gskey:
                print(space['name'])
                getFiles(space['key'])
                
# or uncomment the following lines 107-109 and line 114
# comment the spaceKeyGivenList list on line 86
# comment from lline 93 - 100
# comment line 115
# then it will downlaod from whole wiki

#downlaod files from whole wiki
# def downloadPDF(wikiList):
#     for space in wikiList:
#         getFiles(space['key'])            

#call the function
#downloadPDF(spaceWikilist)
downloadPDF(spaceKeyGivenList, spaceWikilist)