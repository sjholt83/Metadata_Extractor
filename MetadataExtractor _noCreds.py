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
    map = '/getMetaDataFromDirectory' + ' = POST' + '\n' + '/getMetaDataFromFile' + ' = POST' + '\n' + '/getMetaDataFromUri' + ' = POST'
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
    return jsonify(getMetadataFromInput(getImageFromPathAndName(filePath, fileName)))


@app.route('/getMetaDataFromUri', methods=['POST'])
def getMetaDataFromUri():
    req_data = request.get_json()
    fileUri = req_data['FILE_URI']
    return jsonify(getMetadataFromInput(getImageFromUri(fileUri)))


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


def getImageFromPathAndName(filepath, filename):
    if filepath.endswith('/'):
        imageFile = filepath + filename
    else:
        imageFile = filepath + "/" + filename

    img = gdal.Open(imageFile)
    return img


def getImageFromUri(fileUri):
    # Only test for S3 uri's to start
    if fileUri.startswith('s3://'):
        imageFileUri = fileUri.replace('s3://', '/vsis3/')

    # Set up S3 gdal required variables.
    gdal.SetConfigOption('AWS_REGION', 'us-east-1')
    gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY',
                         'REDACTED')
    gdal.SetConfigOption('AWS_ACCESS_KEY_ID', 'REDACTED')
    gdal.SetConfigOption('GDAL_HTTP_UNSAFESSL', 'YES')

    # Call Gdal to open the file.
    img = gdal.Open(imageFileUri)
    print(gdal.GetLastErrorMsg)
    return img


def getMetadataFromInput(img):
    metadata = img.GetMetadata()
    return metadata

app.run()
