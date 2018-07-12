# FreeCAD git tryout

## General idea

This is a playground with the purpose to try to manage freecad documents with git. Basically, it contains folders which contain freecad files and each freecad file contains the geometry of one part.

The whole geometry of the model is supposed to be composed of all parts. So the idea is to load all parts in freecad and create a part structure where the files of the individual parts are just linked into the assembly structure. To achieve this freecad is run with the script `create_assembly.py`:

```
freecad create_assembly.py
```
This script will require the [Assembly3](https://forum.freecadweb.org/viewtopic.php?t=25712) workbench of freecad in order to deal with the Links. Versions of freecad containing this workbench can be downloaded [here](https://github.com/realthunder/FreeCAD_assembly3/releases). Some basic ideas of how to collaborate with FreeCAD using git are also discussed in this [FreeCAD Forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=8688).

The user then works in the assembly structure which contains links of all parts. If he changes something the changes will go into the individual freecad files since they are just linked. When the user finally saves the work only the files that have actually changed are saved. 

The goal of this approach is that multiple users can work together on different branches of the same model and the amount of conflicts created is kept as low as possible. With this approach, a conflict only arises if users are making changes to the same part. So merging branches might become less painful. 

## The model

The model used here is derived from the [public LS-DYNA models of the Toyota Yaris](https://www.nhtsa.gov/crash-simulation-vehicle-models). The geometry was generated using [ANSA](https://www.beta-cae.com/ansa.htm). This is of course not a real CAD model as designers would generate it. The purpose is to investigate/demonstrate ways of collaboration with CAD data when working in distributed teams.

## Dealing with zipped freecad files

This repository uses Zippey from [here](https://bitbucket.org/sippey/zippey) in order to better deal with the zipped fcstd files. (e.g. saving storage, allowing ascii diff, ...)

In order to activate Zippey run the following commands:

```
git config filter.zippey.smudge "$PWD/zippey.py d"
git config filter.zippey.clean "$PWD/zippey.py e"
```

After applying the filters one has to switch bag to a commit before the fcstd files have been added (e.g. commit 98baa2110fdb09c7f5581ab133f45bacd6d9a3b5) and then get back to HEAD.

```
git checkout 98baa
git checkout master
```

Downloading the fcstd files from the WebSite will give you only the unzipped content. In order to recover them you have to do the following:

```
zippey.py d < downloaded-file > recovered-file
```

## Tries with merging

### working with a single file on two branches

In this use case I created two branches: `001_single_file_simple_change_user_Alice` and `001_single_file_simple_change_user_Bob` in both of them I worked with the frecad file: `Toyota_Yaris_-_freecad_single_file/body_in_white___________________________PID0.fcstd`. In the Alice branch I changed the color of the part 51 in the Bob branch I changed the color of part 48.

When trying to merge I got this:

```
marko.thiele@jasper:~/PROJEKTE/FreeCAD_git/freecad_git_tryout$ git merge 001_single_file_simple_change_user_Bob
Traceback (most recent call last):
  File "/home/marko.thiele/PROJEKTE/FreeCAD_git/freecad_git_tryout/zippey.py", line 198, in <module>
    main()
  File "/home/marko.thiele/PROJEKTE/FreeCAD_git/freecad_git_tryout/zippey.py", line 192, in main
    decode(input, output)
  File "/home/marko.thiele/PROJEKTE/FreeCAD_git/freecad_git_tryout/zippey.py", line 156, in decode
    (data_len, raw_len, mode, name) = [t(s) for (t, s) in zip((int, int, str, str), meta.split('|'))]
ValueError: invalid literal for int() with base 10: '<<<<<<< HEAD '
error: external filter /home/marko.thiele/PROJEKTE/FreeCAD_git/freecad_git_tryout/zippey.py d failed 1
error: external filter /home/marko.thiele/PROJEKTE/FreeCAD_git/freecad_git_tryout/zippey.py d failed
automatischer Merge von Toyota_Yaris_-_freecad_single_file/body_in_white___________________________PID0.fcstd
KONFLIKT (Inhalt): Merge-Konflikt in Toyota_Yaris_-_freecad_single_file/body_in_white___________________________PID0.fcstd
Automatischer Merge fehlgeschlagen; beheben Sie die Konflikte und committen Sie dann das Ergebnis.
marko.thiele@jasper:~/PROJEKTE/FreeCAD_git/freecad_git_tryout$ 
```
When I extract both freecad documents and unzip them I can see that most differences come from Document.xml and GuiDocument.xml and unfortunately they are conflicting.

![Document.xml](/images/Document.xml_diff.png)

![GuiDocument.xml](/images/GuiDocument.xml_diff.png)

Some other diffrerences are in files like `DiffuseColor*`, however I suspect these are changes to different files.

Conclusion is that out of the box merging with git will not work with freecad files.


