__author__ = 'primm'
__doc__ = '''
Easy access to a google doc to help synchronize the progress on animation work.
'''

'''
TODO: This should go into sy_utils once paths are good
'''
def pullUpGoogleDoc():
	import subprocess
	subprocess.call("start https://docs.google.com/spreadsheet/ccc?key=0Ah28BQRiViZ-dDF1XzFmYnltYkFNb19hM1RTc1ltMkE#gid=0", shell=True)
