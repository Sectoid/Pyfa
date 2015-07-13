import os
import sys

# TODO: move all logging back to pyfa.py main loop
# We moved it here just to avoid rebuilding windows skeleton for now (any change to pyfa.py needs it)
import logging
import logging.handlers

# Load variable overrides specific to distribution type
try:
    import configforced
except ImportError:
    configforced = None

# Turns on debug mode
debug = False
# Defines if our saveddata will be in pyfa root or not
saveInRoot = False

logLevel = logging.WARN

# Version data
version = "1.13.2"
tag = "Stable"
expansionName = "Aegis"
expansionVersion = "1.0"
evemonMinVersion = "4081"

pyfaPath = None
savePath = None
staticPath = None
saveDB = None
gameDB = None

def isFrozen():
    if hasattr(sys, 'frozen'):
        return True
    else:
        return False


def getPyfaRoot():
    base = sys.executable if isFrozen() else sys.argv[0]
    root = os.path.dirname(os.path.realpath(os.path.abspath(base)))
    root = unicode(root, sys.getfilesystemencoding())
    return root

def __createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def defPaths():
    global pyfaPath
    global savePath
    global staticPath
    global saveDB
    global gameDB
    global saveInRoot
    # The main pyfa directory which contains run.py
    # Python 2.X uses ANSI by default, so we need to convert the character encoding
    pyfaPath = getattr(configforced, "pyfaPath", pyfaPath)
    if pyfaPath is None:
        pyfaPath = getPyfaRoot()

    # Where we store the saved fits etc, default is the current users home directory
    if saveInRoot is True:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = os.path.join(pyfaPath, "saveddata")
    else:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = unicode(os.path.expanduser(os.path.join("~", ".pyfa")),
                               sys.getfilesystemencoding())

    __createDirs(savePath)

    format = '%(asctime)s %(name)-24s %(levelname)-8s %(message)s'
    logging.basicConfig(format=format, level=logLevel)
    handler = logging.handlers.RotatingFileHandler(os.path.join(savePath, "log.txt"), maxBytes=1000000, backupCount=3)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)

    logging.info("Starting pyfa")

    # Redirect stderr to file if we're requested to do so
    stderrToFile = getattr(configforced, "stderrToFile", None)
    if stderrToFile is None:
        stderrToFile = True if isFrozen() else False
    if stderrToFile is True:
        sys.stderr = open(os.path.join(savePath, "error_log.txt"), "w")

    # Same for stdout
    stdoutToFile = getattr(configforced, "stdoutToFile", None)
    if stdoutToFile is None:
        stdoutToFile = True if isFrozen() else False
    if stdoutToFile is True:
        sys.stdout = open(os.path.join(savePath, "output_log.txt"), "w")

    # Static EVE Data from the staticdata repository, should be in the staticdata
    # directory in our pyfa directory
    staticPath = os.path.join(pyfaPath, "staticdata")

    # The database where we store all the fits etc
    saveDB = os.path.join(savePath, "saveddata.db")

    # The database where the static EVE data from the datadump is kept.
    # This is not the standard sqlite datadump but a modified version created by eos
    # maintenance script
    gameDB = os.path.join(staticPath, "eve.db")

    ## DON'T MODIFY ANYTHING BELOW ##
    import eos.config

    #Caching modifiers, disable all gamedata caching, its unneeded.
    eos.config.gamedataCache = False
    # saveddata db location modifier, shouldn't ever need to touch this
    eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
    eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"
