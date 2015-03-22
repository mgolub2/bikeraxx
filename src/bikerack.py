__author__ = 'mgolub2'
"""
Take photos based on rangefinder data and upload it to an azure blob container.
"""

import mraa
import time
import subprocess
import requests
import os
from azure.storage import BlobService

#Constants, not globals
backendUrl = 'http://bikeraxx.azurewebsites.net/api/Photo/'
aioPort = 0
numPhotos = 5
triggerValue = 600
scaleFactor = (5.0 / .0049)  # 5 volts and 4.9mv a centimeter
x = mraa.Aio(aioPort)
trigDistance = mraa.Aio(5) # setable distance trigger
led = mraa.Gpio(13)
led.dir(mraa.DIR_OUT)
azureAccount = 'bikeraxx'
accountKey = 'EltOIT0eHKLIBz4R6uc5xcOE1TynZQJwZh8p/3HwGAR4RlhsD+L22ClBst0pVZcxScX6Mp9wt1KVJsw/yHJ65w=='
container = 'images'


def main():
    """
    Run the main loop for the magical bus detection sensor
    :return:
    """
    blob_service = BlobService(account_name=azureAccount, account_key=accountKey)
    subprocess.call('adb shell "am start -a android.media.action.STILL_IMAGE_CAMERA"', shell=True)
    while 1:
        distance = readAio()
        trigger = trigDistance.read()
        print(distance, ' : ', trigger)
        if distance < trigger and distance:  # probs need to have a better deciding logic
            led.write(1)
            images = takePhoto()
            print images
            for image in images:
                print ("uploading {0}".format(image))
                putImage(image, blob_service)
            putToApi(images)
            deleteImages(images)
        led.write(0)
        time.sleep(.1)

def deleteImages(images):
    """
    Delete all jpegs!
    :param images:
    :return:
    """
    for image in images:
        try:
            os.remove(image)
        except OSError as e:
            print ("Error removing file : {0}".format(e))

def takePhoto():
    """
    Take a photo using gphoto and return the filename
    :return:
    """
    # subprocess.call("gphoto --takephoto or some shit")
    jpegs = []
    for x in range(numPhotos):
        subprocess.call('adb shell "input keyevent 27"', shell=True)
    time.sleep(1)
    pulledFiles = subprocess.Popen('adb pull /sdcard/DCIM/Camera/', shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1]
    pulledFiles = pulledFiles.split('\n')
    for line in pulledFiles:
        if 'jpg' in line:
            jpegs.append(line.split('/')[-1])
    subprocess.call('adb shell "rm -rf /sdcard/DCIM/Camera/"', shell=True)
    subprocess.call('adb shell "mkdir /sdcard/DCIM/Camera/"', shell=True)
    return jpegs


def putToApi(jpegs):
    """
    Posts the images to the bikeraxx api
    :param jpegs:
    :return:
    """
    for pic in jpegs:
        #Weird and ugly
        while True:
            try:
                pic = pic.split('.')[0]
                print ("Posting to api: {0}".format(pic))
                r = requests.put(backendUrl+pic.upper())
                print(r.status_code)
            except requests.exceptions.ConnectionError as e:
                print (e)
                continue
            break

dataArray = [0,0,0,0,0,0,0]

def readAio():
    """
    Read the analog port from the rangfinder
    :return:
    """
    try:
        dataArray.append(x.readFloat() * scaleFactor)
        dataArray.pop(0)
        return sum(dataArray)/float(len(dataArray))
    except:
        print ("ADC Error")


def putImage(image, blob_service):
    """
    Put an image into the azure block storage
    :param image:
    :param blob_service:
    :return:
    """
    blob_service.put_block_blob_from_path(
        container,
        image.split('/')[-1].upper(),  # just get the nbame without any potential path
        image,
        x_ms_blob_content_type='image/png'
    )


if __name__ == "__main__":
    main()