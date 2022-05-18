
from atlassian import Confluence        #confluence
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
            try:
                os.makedirs(dirName)    
                print("Directory " , dirName ,  " Created ")
                os.chdir(dirName)
            except FileExistsError:
                print("Directory " , dirName ,  " already exists")
                os.chdir(dirName)
                #delete old files if they exists
                files = glob.glob('')
                for f in files:
                    os.remove(f)
                print("All files inside", dirName, " are deleted")

                #download files from onlyPDF list
            for value in values:                                                           
                #print("Page ID: " + value['id'] + " Page title: " + value['title']) 
                page = confluence.get_page_by_id(page_id=value['id'])
                pageId = value['id']  
                #A function to create pdf from byte-stream responce
                def save_file(content):
                    file_pdf = open(pageId, 'wb')
                    file_pdf.write(content)
                    file_pdf.close()
                    print("downloaded: " + value['title'])
                #Get your confluence page as byte-stream
                response = confluence.get_page_as_pdf(page['id'])
                save_file(content=response) 
                content_ids.append((value['id'])) 
                    
            #exit from current folder and go back to home dir
            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)
            #os.chdir('../')
    print("Found pages in space {}:  {}".format(space, len(content_ids)))
    return content_ids 



#wiki space list 
spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
spaceWikilist = spaces['results']

#export pages from whole wiki
def downloadPages(wikiList):
    for space in wikiList:
        getFiles(space['key'])            

#call the function
downloadPages(spaceWikilist)