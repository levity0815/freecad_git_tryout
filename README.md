# freecad_git_tryout

This is a playground to try to manage freecad documents with git. Basicly it contains folders which contain freecad files and each freecad file contains the geometry of one part.

The whole geometry of the model is composed of all parts. So the idea is to load all parts in freecad and create a part structure where the files of the individual parts are just linked into the assembly structure. The user than works in the assembly structure which contains all parts. If he changes something the changes will go into the individual frecad files since they are just linked. When the user finaly saves his work only the files that have actually changes are saved. 

The goal of this aproach is that multiple user can work together on the same model and the amount of conflicts created is as low as possible. With this aproach a conflict only arises if users are making changes to the same part.

