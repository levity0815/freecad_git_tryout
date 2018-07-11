# FreeCAD git tryout

## General idea

This is a playground with the purpose to try to manage freecad documents with git. Basicly it contains folders which contain freecad files and each freecad file contains the geometry of one part.

The whole geometry of the model is supposed to be composed of all parts. So the idea is to load all parts in freecad and create a part structure where the files of the individual parts are just linked into the assembly structure. To achive this freecad is run with the script `create_assembly.py`:

```
freecad create_assembly.py
```
This schript will require the [Assembly3](https://forum.freecadweb.org/viewtopic.php?t=25712) workbench of freecad in order to deal with the Links. Versions of freecad containing this workbench can be downloaded [here](https://github.com/realthunder/FreeCAD_assembly3/releases). Some basic ideas of how to colobarate with FreeCAD using git are also discussed in this [FreeCAD Forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=8688).

The user than works in the assembly structure which contains links of all parts. If he changes something the changes will go into the individual freecad files since they are just linked. When the user finaly saves the work only the files that have actually changes are saved. 

The goal of this aproach is that multiple user can work together on different branches of the same model and the amount of conflicts created is kept as low as possible. With this aproach a conflict only arises if users are making changes to the same part. So merging branches might become less painfull. 

## The model

The model used here is derived from the [public LS-DYNA models of the Toyota Yaris](https://www.nhtsa.gov/crash-simulation-vehicle-models). The geometry was generated using [ANSA](https://www.beta-cae.com/ansa.htm). This is offcourse not a real CAD model as designers would generate it. The purpose is to investigate/demonstrate ways of colaboration with CAD data when working in distrubted teams.

## Dealing with zipped frecad files

This repository uses Zippey from [here](https://bitbucket.org/sippey/zippey) in order to better deal with the zipped fcstd files. (e.g. saving storage, allowing ascii diff, ...)

In order to activate Zippey run the following commands:

```
git config filter.zippey.smudge "$PWD/zippey.py d"
git config filter.zippey.clean "$PWD/zippey.py e"
```

After applying the filters one has to switch bag to a commit before the fcstd files have been added (e.g. commit 98baa2110fdb09c7f5581ab133f45bacd6d9a3b5) and than get back to HEAD.

```
git checkout 98baa
git checkout master
```

Downloading the fcstd files from the WebSite will give you only the unziped content. In order to recover them you have do do the following:

```
zippey.py d < downloaded-file > recovered-file
```

