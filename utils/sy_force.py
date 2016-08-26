def forceWriteable(absFilePath, verbose=False):
    import os, stat
    """
    Overwrites read-only flags on files incase internet drops
    or if Perforce interactions is unreachable/fails.
    """
    #Getting file stats to make any existing file off of read-only from perforce.
    fileAtt = os.stat(absFilePath)[0]
    if (not fileAtt & stat.S_IWRITE):
        # File is read-only, so make it writeable
        os.chmod(absFilePath, stat.S_IWRITE)

    if verbose:
        #Change this to logger
        print 'Made file "%s" writeable locally. Remember to check it on Perforce if intended to submit.' % absFilePath

if __name__ == '__main__':
    pass
    