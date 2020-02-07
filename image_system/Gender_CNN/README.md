Gender CNN
===========

Gender determination using CNN


## Description
2 class classification of men and women using CNN.


## Requirement

- macOS Mojave 10.14.6
- Python 3.5.2
- TensorFlow 2.0.0a0


## Where is the image fiels?
1. Original Data (variable length)
- ./original_data/man(or woman)/---.jpg

2. Teacher Data (128*128 size)
 - Generate teacher data
```
# Place image file in "./original_data/"
$ make teach.build
```


## Usage
- train
```
$ python train.py
```


## Installation
- Ubuntu
```
$ git clone https://github.com/AtLab-jp/Gender_CNN
$ cd Gender_CNN
$ sh ./setup.sh
```