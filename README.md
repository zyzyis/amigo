# Amigo

A python script to solve your mass photo storage.

## Quick Start ##
Run
```
./amigo.py <Source Directory> <Dest Directory>
```

To organize the photos / movies from the source directory to the destination directory.

All the files are organized by date, e.g. a tree structure can be like this
```
├── Movies
│   ├── 2012
│   │   ├── 07
│   │   │   └── 29
│   │   │       └── 2012-07-29\ 19.00.51.mov
│   │   ├── 08
│   │   │   ├── 05
│   │   │   │   └── 2012-08-05\ 18.48.18.mov
│   │   │   ├── 23
│   │   │   │   ├── 2012-08-23\ 08.55.03.mov
│   │   │   │   └── 2012-08-23\ 17.36.32.mov
└── Photos
    ├── 2005
    │   └── 08
    │       └── 20
    │           └── IMG_2480.JPG
    ├── 2007
    │   └── 07
    │       └── 16
    │           └── 3.jpg
    ├── 2009
    │   └── 01
    │       ├── 05
    │       │   ├── IMG_7641.jpg
    │       │   ├── IMG_7642.JPG
    │       │   └── IMG_7643.JPG
    │       └── 06
    │           ├── IMG_7644.JPG
    │           ├── IMG_7645.JPG
```

# Why do you need this file?

Most of the people today use Cloud drive provider (e.g. Amazon Cloud Drive) to store their photos. One of the steps before uploading is to oragnize them so that you feel it is clean with no duplication before you upload. By storing files based on the time it can prevent majority of the duplication problems and also provides a nice index structure for people to find photos. 

## Cases
For most of the cases it just works fine, except the following cases where Amigo is going to do differently.

### Duplicate Photos
Amigo will check whether the photo already exists in the Destination directory. If there is already a file with the same name exists, Amigo will compare two files to check whether they are identical. Amigo will check by comparing the MD5sum of part of the files. If both files are identical Amigo will just ignore the move of the files.

### Photos with the same name
When there are two files which are NOT identical but just have the same name, Amigo will rename the existing photo file with a random integer as the suffix.
