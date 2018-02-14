#!/usr/bin/python

__version__ ='1.3'
__author__ ='Sam Powell'
__date__ ='10/03/17'
__email__='batmunkey@hotmail.com'

import os
import time
import logging
import subprocess
from os.path import join

ONEWEEK = "changeme1week"
ONEMONTH = "changeme1month"
THREEMONTH "changeme3month"
LOGPATH = "/var/log/findanddelete.py"

# Create the logging file if it doesn't exist
if not os.path.exists('/var/log/findanddelete.log'):
    open('/var/log/findanddelete.log', 'w').close()

# Build a logger
def instantiateLogger():
    global logger
    logger = logging.getLogger("log")
    hdlr = logging.FileHandler(LOGPATH)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info('Set a cron notification here')

# Add python system statistics to log file
def pythonSystemStats():
    versionpy = subprocess.check_output("python --version", stderr=subprocess.STDOUT, shell=True)
    whichpy = subprocess.check_output("which python", shell=True)
    osslpy = subprocess.check_output("python -c 'import ssl; print ssl.OPENSSL_VERSION'", shell=True)
    logger.info("Your version of python is " + versionpy.rstrip("\n"))
    logger.info("Here is the path to your python " + whichpy.rstrip("\n"))
    logger.info("This is your pythons openssl version " + osslpy.rstrip("\n"))

def setvars():
    global weekPath
    global monthPath
    global threeMonthPath
    global now
    weekPath = str(ONEWEEK)
    monthPath = str(ONEMONTH)
    threeMonthPath = str(THREEMONTH)
    now = time.time()
    
# Remove files older than one week
def weekremove(dir):
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        if os.stat(fullpath).st_atime < (now - 604800):
            if os.path.isfile(fullpath):
                logger.warn('This file was deleted since it was older than a week=%s', fullpath)
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                weekremove(fullpath)

# Remove files older than one month
def monthremove(dir):
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        if os.stat(fullpath).st_atime < (now - 2592000):
            if os.path.isfile(fullpath):
                logger.warn('This file was deleted since it was older than a month=%s', fullpath)
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                monthremove(fullpath)

# Remove files older than three months
def threemonthremove(dir):
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        if os.stat(fullpath).st_atime < (now - 7776000):
            if os.path.isfile(fullpath):
                logger.warn('This file was deleted since it was older than three months=%s', fullpath)
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                threemonthremove(fullpath)

#### Now we need to remove empty directories
def remEmptyDir(path, recursive=True):
    for root, dirs, files in os.walk(path,topdown=True):
        for name in dirs:
            dirname = join(root,name)
            if os.stat(dirname).st_atime < (now - 604800):
                if not os.listdir(dirname): #to check wither the dir is empty
                    logger.warn('This directory was deleted because it was empty=%s', dirname)
                    os.removedirs(dirname)
                    
### Layout the logic
def main():
    instantiateLogger()
    pythonSystemStats()
    setvars()
    weekremove(weekPath)
    monthremove(monthPath)
    threemonthremove(threeMonthPath)
    remEmptyDir(ONEWEEK)
    remEmptyDir(ONEMONTH)
    remEmptyDir(THREEMONTH)
    # Log each time the cron job finishes successfully
    logger.info('The hourly cron job was finished successfully')

# Run Everything
if __name__ == '__main__':
    main() 
