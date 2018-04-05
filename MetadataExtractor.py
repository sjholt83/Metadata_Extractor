#!/usr/bin/python
# Written by Samuel Holt
# and Mike Hartman
# April 03, 2018
# Written for ODS contract
# Team Bachmanity

from osgeo import gdal
from os import listdir
from flask import Flask, request, jsonify

app = Flask(__name__)

extensions = ['ntf', 'tif', 'tiff', 'jpg', 'jpx', 'jp2', 'j2k', 'jpeg',
              'nsf', 'nitf', 'dt0', 'dted', 'pdf', 'shp', 'png', 'pds',
              'gta', 'bmp', 'gif', 'dt1', 'dt2', 'gen', 'thf', 'gn', 'hr',
              'ja', 'jg', 'jn', 'lf', 'kap']

@app.route('/')
def lander():
    map = '/getMetaDataFromDirectory' + ' = POST' + '\n' + '/getMetaDataFromFile' + ' = POST'
    return map


@app.route('/getMetaDataFromDirectory', methods=['POST'])
def getMetaDataFromDirectory():
    req_data = request.get_json()
    directory = req_data['DIRECTORY']
    return jsonify(getMetadataFromBatch(directory, getFilesFromBatch(directory, extensions)))


@app.route('/getMetaDataFromFile', methods=['POST'])
def getMetaDataFromFile():
    req_data = request.get_json()
    filePath = req_data['FILE_PATH']
    fileName = req_data['FILE_NAME']
    return jsonify(getMetadataFromInput(getFileFromInput(filePath, fileName)))


###########################################################################################################


def getFilesFromBatch(directory, extensions):
    filenames = []
    for files in listdir(directory):
        for extension in extensions:
            if files.lower().endswith('.' + extension):
                filenames.append(files)
    return filenames


def getMetadataFromBatch(directory, filenames):
    metadataList = []
    for element in filenames:
        if directory.endswith('/'):
            filename = directory + element
        else:
            filename = directory + "/" + element
        img = gdal.Open(filename)
        metadata = img.GetMetadata()
        metadataList.append(metadata)
    return metadataList


def getFileFromInput(fileuri, filename):
    if fileuri.endswith('/'):
        imageFile = fileuri + filename
    else:
        imageFile = fileuri + "/" + filename

    img = gdal.Open(imageFile)
    return img


def getMetadataFromInput(img):
    metadata = img.GetMetadata()
    return metadata

app.run()
