__author__ = 'mgolub2'
"""
Take photos based on rangefinder data and upload it to an azure blob container.
"""

import mraa
import time
from azure.storage import BlobService

aioPort = 1
azureAccount = 'bikeraxx'
accountKey = 'EltOIT0eHKLIBz4R6uc5xcOE1TynZQJwZh8p/3HwGAR4RlhsD+L22ClBst0pVZcxScX6Mp9wt1KVJsw/yHJ65w=='
container = 'images'

def main():
    blob_service = BlobService(account_name=azureAccount, account_key=accountKey)
    while 1:
        print (readAio())
        time.sleep(1)

def readAio():
    """
    Read the analog port from the rangfinder
    :return:
    """
    try:
        x = mraa.Aio(aioPort)
        return x.read()
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
    image.split('/')[-1], #just get the nbame without any potential path
    image,
    x_ms_blob_content_type='image/png'
)

if __name__ == "__main__":
    main()