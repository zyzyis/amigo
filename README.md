# Amigo

A python script to solve your mass photo storage.

Run
```
./amigo.py <Source Dir> <Dest Dir>
```

To organize the the photos from the source directory to the destination directory.

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
│   │   │   ├── 24
│   │   │   │   └── 2012-08-24\ 21.01.09.mov
│   │   │   └── 26
│   │   │       └── 2012-08-26\ 10.08.26.mov
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
    │           ├── IMG_7646.JPG
    │           ├── IMG_7647.JPG
    │           ├── IMG_7649.JPG
    │           ├── IMG_7650.JPG
    │           └── IMG_7652.JPG
```

The script will also identify duplicate photos, photos with the same name, and will deal with each of the type.
