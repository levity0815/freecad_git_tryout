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
#
# getcwd will not work because it gives the dir where freecad is running and
# this is somewhere in the tmp dir (at least for the asm3 version for freecad)
# cwd=os.getcwd()

# asuming that the last argument given to freecad was this script
# extract the path from the script and use that as working dir
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
cwd=os.path.dirname(sys.argv[-1])
print('Working dir: {}').format(cwd)


sys.exit

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
        # TODO: check if part/group/assembly allready exists
        
        # TODO: create assemblies (asm3) instead of groups! (unfortunately this is not recorded by macro)

        # create group_element as group below last_group_element or at root in the document
        print("creating group: {}").format(group_element)
        # App.activeDocument().Tip = App.activeDocument().addObject('App::DocumentObjectGroup',str(group_element))
        App.activeDocument().Tip = App.activeDocument().addObject('App::Part',str(group_element))
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
    # the group this part belongs to is the last part of the relativ path
    group=part[1].split("/")[-1]
    
    print('opening file: {}').format(rel_file_path)
    print('belongs to group: {}').format(group)
 

    doc=FreeCAD.open(rel_file_path)
    
    objects=doc.RootObjects 

    for object in objects:
        # API here: https://www.freecadweb.org/wiki/Object_API
        label=object.Label
        name=object.Name
        content=object.Content    

        print(object.PropertiesList)
       
        # for each root object create a link in the assembly document
        App.getDocument('assembly').addObject('App::Link',label).setLink(object)
        App.getDocument('assembly').getObject(label).Label=label
        App.getDocument("assembly").getObject(group).addObject(App.getDocument("assembly").getObject(label))
    
    if doc:
      print('file loaded')
      del(doc)


# make the assembly document active
App.setActiveDocument("assembly")
App.ActiveDocument=App.getDocument("assembly")
Gui.ActiveDocument=Gui.getDocument("assembly")
# recompute the assembly document
FreeCAD.ActiveDocument.recompute()


# save the assembly document
App.getDocument("assembly").saveAs(os.path.join(cwd,'assembly.fcstd'))
