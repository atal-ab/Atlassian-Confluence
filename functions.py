from atlassian import Confluence

confluence = Confluence(
    url="https://wiki-address",
    username='username',
    password="password")

#1- Get All Spaces and then filter for the specific one
#2- get all available pages inside of selected space 
#3- get all attachments of each page

#1 Getting Spaces
spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
spacelist = spaces['results']

def getAllSpaces ():
    for space in spacelist:
       print(space['key']+ ' - '+ space['name'])
    #count the spaces from results
    print('Total Spaces: ' ,len(spacelist))

def getSpaceWithKey (spaceKey):
    for space in spacelist:
        skey = space['key']
        if spaceKey == skey:
            print(space['name'])

def getSpaceWithName (spaceName):
    for space in spacelist:
        sName = space['name']
        if spaceName == sName:
            print(space['key'], space['name'])

#call the functions
getAllSpaces() 
#getSpaceWithKey('HHU')
#getSpaceWithName('azubi')

#2 Get all pages of selected space
def getAllPagesOfSpaceWithKey(space):
    limit = 500
    flag = True
    step = 0
    content_ids = []

    while flag:
        values = confluence.get_all_pages_from_space(space=space, start=limit * step, limit=limit)
        step += 1
        if len(values) == 0:
            flag = False
            print("Page not found, check permissions")
        else:
            for value in values:                                                            #go through all values
                print("Page ID: " + value['id'] + " Page title: " + value['title'])         #print the values
                content_ids.append((value['id']))  
                                                     #count number of pages found
    print("Found in space {} pages {}".format(space, len(content_ids)))                     #print total number of pages found
    return content_ids 

#call the function
#getAllPagesOfSpaceWithKey('ALMA')
#getAllPagesOfSpaceWithKey('ALMA')


