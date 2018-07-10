# -*- coding: utf-8 -*-

import FreeCAD
import FreeCADGui
import os
import sys

# create a document to work in
#Gui.activateWorkbench("Assembly3Workbench")
App.newDocument("assembly")
App.setActiveDocument("assembly")
App.ActiveDocument=App.getDocument("assembly")
Gui.ActiveDocument=Gui.getDocument("assembly")


# find all files in current working dir
cwd='/home/marko.thiele/Downloads/freecad_git_tryout/freecad_assembly'
os.chdir(cwd)
parts=[]
groups=[]
for root, dirs, files in os.walk(cwd):
    for file in files:
        if file.endswith(".fcstd") and file!='assembly.fcstd':
             # extract relativ path
             rel_path=root.replace(cwd+'/','')
             parts.append([root,rel_path,file])
             groups.append(rel_path)

# make the list of groups uniq so we can use it to create the assembly structure
groups = list(set(groups))

print(groups)

# create a group structure as contained in groups
# go through all groups
for group in groups:
    # for each group create the whole part structure
    # create a list
    group = group.split("/")
    
    # walk through the list
    last_group_element=False
    for group_element in group:
        # TODO: check if part allready exists
        
        # create group_element as group below last_group_element or at root in the document
        print("creating group: {}").format(group_element)
        App.activeDocument().Tip = App.activeDocument().addObject('App::DocumentObjectGroup',str(group_element))
        App.activeDocument().getObject(group_element).Label = group_element

        if last_group_element:
            # moving group
            print("moving group: {0} to group: {1}").format(group_element,last_group_element)
            App.getDocument("assembly").getObject(last_group_element).addObject(App.getDocument("assembly").getObject(group_element))

        # remember the just created group_element because this will be the object where to move the next part
        last_group_element=group_element

        # recompute the document 
        App.ActiveDocument.recompute()



# load all documents and create links within the groups

# before we can start to create links we will have to save the assembly document
App.getDocument("assembly").saveAs(os.path.join(cwd,'assembly.fcstd'))

# now load all parts and create the links
for part in parts:
    # open the fcstd
    rel_file_path='{0}/{1}'.format(part[1],part[2])
    print('opening file: {}').format(rel_file_path)

    openingDoc=FreeCAD.open(rel_file_path)

    print(openingDoc.OutList)
    
    if openingDoc:
      print('file loaded')
      del(openingDoc)



#  sys.exit()
#  
#  #App.setActiveDocument("_9___bumper_bracket_R________________________")
#  #App.ActiveDocument=App.getDocument("_9___bumper_bracket_R________________________")
#  #Gui.ActiveDocument=Gui.getDocument("_9___bumper_bracket_R________________________")
#  if __openingDoc:
#    Gui.setActiveDocument(__openingDoc)
#    del(__openingDoc)
#  #App.setActiveDocument("assembly")
#  #App.ActiveDocument=App.getDocument("assembly")
#  #Gui.ActiveDocument=Gui.getDocument("assembly")
#  App.getDocument('assembly').addObject('App::Link','Link').setLink(App.getDocument('_9___bumper_bracket_R________________________').biw_____________EU_LL_______________________________________0783_d6a69ac9_key)
#  App.getDocument('assembly').getObject('Link').Label='Link_000039_bumper_bracket_R'
#  App.getDocument("assembly").getObject("radiator_frame").addObject(App.getDocument("assembly").getObject("Link"))
#  
