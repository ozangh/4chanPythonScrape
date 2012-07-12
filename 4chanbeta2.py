# raw mainpage scrubber

import os.path
import re
import string
import sys
import time
import urllib
import urllib2
import thread
import shutil
import os
import sys


print "Starting up..."
#detect OS
print "..."
print "Detecting OS Environment..."
#Sets what character is used for a slash in directories
if os.name == "posix":
	print "...Unix/Linux based environment."
	os.uname()
	slash = chr(47)
	clearscreen = "clear"
elif os.name == "nt":
	print "...Windows NT based environment."
	clearscreen = "cls"
	slash = chr(92)
elif os.name == "mac":
	print "...Macintosh based environment."
	print "...Sorry, but Mac OS currently "
	print "...isn't supported by this script,"
	print "...as we don't have a testing  "
	print "...machine that runs on Mac OS."
	macuser = raw_input("...Press enter to exit. ")
elif os.name == "ce":
	print "...Windows CE based environment."
	print "...Continuing, but script might not work properly."
else:
	print "...WTF are you running?"
	wtfuser = raw_input("...Press enter to exit. ")
print "..."
nextscr = raw_input("Startup complete. Press enter to continue. ")
os.system(clearscreen)


# Queries user for locations, and gives warnings
# We are now crossing into userland. 
# The program must be able to run without the sterile Dev environment.
if len(sys.argv)==1:
	print 'WARNING! This program will automatically crawl and'
	print 'download ALL images and ALL threads on 4chan\'s   '
	print 'boards. Niether 4chan, r000t, or Calvin Graham    '
	print 'control, or are responsible for anything posted on'
	print 'these boards. This script is not capable of filter'
	print 'ing out pornographic, illegal, or unsavory content'
	print 'that may reside on these boards. YOU ALONE ARE ULT'
	print 'IMATLEY RESPONSIBLE FOR ANYTHING THAT THIS SCRIPT '
	print 'ENDS UP DOWNLOADING! This script downloads ALL ima'
	print 'ges and threads, as such, it tends to hog a lot of'
	print 'disk space, around 1GB an hour, on average. Please'
	print 'remember that this is BETA software. While all eff'
	print 'orts have been made to protect your computer from '
	print 'harm, YOU ALONE ARE ULTIMATLEY RESPONSIBLE FOR ANY'
	print 'DAMAGE THIS SCRIPT MAY CAUSE TO YOUR COMPUTER!    '
	warn = raw_input("Are you SURE you want to continue? (y/n) ")
	warn = warn.lower()
	if 'n' in warn:
		exit()
	os.system(clearscreen)
	print 'What directory do you want the script to place the'
	print 'content in? Type the location, but do not include '
	directory = raw_input("a trailing slash: ")
	os.system(clearscreen)
	verbose = raw_input("Verbose (detailed output) Mode? (y/n) ")
	if 'n' in verbose:
		verbose = False
	else:
		verbose = True
	os.system(clearscreen)
	if not os.path.exists(directory):
		os.mkdir(directory)
	boardtoscan = raw_input("Which board would you like to leech? ")
	directory = directory + slash + boardtoscan
	if not os.path.exists(directory):
		os.mkdir(directory)
	threadtoscan = raw_input("Which thread would you like to leech? (Leave empty for whole board)")
else:
	directory = sys.argv[2]
	if not os.path.exists(directory):
		os.mkdir(directory)
	boardtoscan = sys.argv[3]
	directory = directory + slash + boardtoscan
	if not os.path.exists(directory):
		os.mkdir(directory)
	verbose = sys.argv[1]
	
# Tabulation counts threads active
tabulation = 0
# This extra-crunchy 
def closethread(dname, dirname):
			global tabulation
			global directory
			tabulation = tabulation - 1
			dest = directory+slash+'Dead Threads'+slash+dname+slash
			shutil.move(dirname, dest)
			print dname+" has 404'd."
			exit()

def scrubthread(addr):
#initial release Nov. 5, 2009
#v6 release Jan. 20, 2009
#http://cal.freeshell.org
#v8 embedded by r000t
#embedded version won't work outside of archiver
    global tabulation
    while 1: #TODO: PUT THE EXCEPT TAG UNDER THERE!!!!

	
	
	
	#Regular Expressions
	imgurl = re.compile('//\w+\.4chan\.org/\w+/src/\d+\.(?:jpg|gif|png|jpeg)')
	thumb = re.compile('//.\.thumbs\.4chan\.org/\w+/thumb/\d+s\.(?:jpg|gif|png|jpeg)')
	thumbname = re.compile("\d+s\.(?:jpg|gif|png|jpeg)")
	imgurl2 = re.compile('//\w+\.4chan\.org/\w+/src/')
	picname = re.compile('\d+\.(?:jpg|gif|png|jpeg)')
	tname = re.compile('/\d+')
	rs = re.compile('http://rapidshare.com/files/\d+/.*\.(?:rar|zip|avi|wmv|part\d+\.rar|\d+)''|http://megaupload.com/?d=........''|http://megaporn.com/?d=........')
	
	#Initiate Variables
	thread = addr #get argument from initial command: this is the thread address
	#directory = "/home/vistro/4chan" TODO TAKE OUT THAT DIRECTORY COMPLETLEY!!!!
	delay = "25"
	arch = 1
	
	#Setup headers to spoof Mozilla
	dat = None
	ua = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:14.0) Gecko/20120329 Firefox/14.0a1"
	head = {'User-agent': ua}
	
	errorcount = 0
	
	
	#Create directory name
	dirname = str(tname.findall(thread))
	
	#Clean directory name
	dirname = dirname.replace('[', '')
	dirname = dirname.replace(']', '')
	dirname = dirname.replace(chr(39), '')
	dirname = dirname.replace(chr(92), '')
	dirname = dirname.replace(chr(47), '')
	dname = dirname
	dirname = directory + slash + dirname #from here on out, all chr(numbers) are being replaced with slash
	# slash is replaced with the right chr(numbers) automatically depending on the OS.
	if verbose:
		print "Downloading to: " + dirname 
	#Create directorty if it doesn't exist
	if not os.path.exists(dirname):
	    os.mkdir(dirname)
	if arch == 1:
	    if not os.path.exists(dirname + slash + "thumbs"):
	        os.mkdir(dirname + slash + "thumbs")
	    
	        
	#Add \ to directory name for image saving        
	dirname = dirname + slash
	
	#Start
	while 1:
	    numimg = 0
	    numthumb = 0
	    if verbose:
	    	print "Scraping: " + thread 
	
	#Get page
	    req = urllib2.Request(thread, dat, head)
	    try:
	        response = urllib2.urlopen(req)
	    except urllib2.HTTPError, e:
	        if errorcount < 1:
	            errorcount = 1
		    if verbose:
	            	print "Request failed, retrying in " + delay + " seconds"
	            time.sleep(int(delay))
		    try:
        	    	response = urllib2.urlopen(req)
		    except:
		    	closethread(dname, dirname)
	
		else:
		    closethread(dname, dirname)
	    except urllib2.URLError, e:
	        if errorcount < 1:
	            errorcount = 1
	            if verbose:
	            	print "Request failed, retrying in " + delay + " seconds"
	            time.sleep(int(delay))
	            response = urllib2.urlopen(req)
	
	    msg = response.read()
	    errorcount = 0
	    
	#Find all pictures and rapidshare links
	    kwl = imgurl.findall(msg)
	    rsl = rs.findall(msg)
	    tl = thumb.findall(msg)
	
	#Save pictures
	    for item in list(set(kwl)): #list(set(kwl)) removes duplicates
		
	#Clean image URL and clean file name
		filename = picname.findall(str(item))
	        fname = str(filename)
	        fname = fname.replace('[', '')
	        fname = fname.replace(']', '')
	        fname = fname.replace(chr(39), '')
		#Download the image if it doesn't exists
	        if not os.path.isfile(dirname + fname):
		    if verbose:
	            	print "Downloading: " + str(item)
	            try:
	                urllib.urlretrieve(str("http:" + item), dirname + str(fname))
			numimg = numimg + 1
	            except urllib.ContentTooShortError:
			if verbose:
	                    print "Image download failed, retrying in " + int(delay)/4 + " seconds"
	                time.sleep(int(delay)/4)
                	urllib.urlretrieve(str("http:" + item), dirname + str(fname))
                	time.sleep(0.25)
	
	#Download thumbnails
	    if arch == 1:
	        for item3 in list(set(tl)): #list(set(kwl)) removes duplicates
	    #Clean image URL and clean file name
	            filename = thumbname.findall(str(item3))
	            fname = str(filename)
	            fname = fname.replace('[', '')
	            fname = fname.replace(']', '')
	            fname = fname.replace(chr(39), '')
	    #Download the image if it doesn't exists
	            if not os.path.isfile(dirname + "thumbs" + chr(47) + fname):
			if verbose:
	                	print "Downloading thumbnail: " + str(item3)
	                try:
	                    urllib.urlretrieve(str("http:" + item3), dirname + "thumbs" + chr(47) + str(fname))
			    numthumb = numthumb + 1
	                except urllib.ContentTooShortError:
			    if verbose:
	                    	print "Thumbnail download failed, retrying in " + int(delay)/4 + " seconds"
	                    time.sleep(int(delay)/4)
	                    urllib.urlretrieve(str("http:" + item3), dirname + "thumbs" + chr(47) + str(fname))
	                    time.sleep(0.25)
	
	#Replace URLs with local images locations
	    outp = open(dirname + dname + ".html", "w")
	
	    for item3 in list(set(kwl)):
	        filename = picname.findall(str(item3))
	        fname = str(filename)
	        fname = fname.replace('[', '')
	        fname = fname.replace(']', '')
	        fname = fname.replace(chr(39), '')
	        msg = msg.replace(str(item3), fname)
	        
	    if arch == 1:
	        for item4 in list(set(tl)):
	            filename = thumbname.findall(str(item4))
	            fname = str(filename)
	            fname = fname.replace('[', '')
	            fname = fname.replace(']', '')
	            fname = fname.replace(chr(39), '')
	            msg = msg.replace(str(item4), chr(34) + "thumbs" + chr(47) + fname + chr(34))
	            
	    outp.write(msg)
	    outp.close()
	
	
	#Save download links to a text file if they exist
	    if not rs.search(msg):
			if verbose:
	        		print "Nothing to download."
			else:
				pass
	    else:
                    foutrs = open(dirname + "dl.txt", "w")
                    for item2 in list(set(rsl)):
                        foutrs.write(str(item2) + "\n")
                        foutrs.close()
	
	#Wait to execute code again
	    if verbose:
	    	print "Waiting " + delay + " seconds before retrying"
	    	print addr +" Fetched " + str(numimg) + " new images and " + str(numthumb) + " thumbnails this session. "
	    numimg = 0
	    numthumb = 0
	    time.sleep(int(delay))
    #except socket.error:
	#print sys.exc_info()
	#print addr+" has 404'd. Have a nice day!"
	#tabulation = tabulation - 1
	




delay = "5"

burl = re.compile('res/\d+')

dat = None
ua = "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.4) Gecko/20091007 Firefox/3.5.4"
head = {'User-agent': ua}

errorcount = 0

if len(sys.argv)==5:
	threadtoscan = sys.argv[4]
	tabulation = tabulation + 1
	addr2 = "http://boards.4chan.org/" + boardtoscan + "/res/" + threadtoscan
	scrubthread(addr2)
	exit()
#Start
inservice = []
while 1:
#Get page
    req = urllib2.Request('http://boards.4chan.org/'+boardtoscan+'/', dat, head)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        if errorcount < 1:
            errorcount = 0
            print "Request failed, retrying in " + delay + " seconds"
            time.sleep(int(delay))
            response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if errorcount < 1:
            errorcount = 0
            print "Request failed, retrying in " + delay + " seconds"
            time.sleep(int(delay))
            response = urllib2.urlopen(req)
	if not len(threadtoscan)==0:
		addr2 = "http://boards.4chan.org/"+boardtoscan+"/" + threadtoscan
		scrubthread(addr2)
		exit()
    msg = response.read()
    errorcount = 0 
    kwl = burl.findall(msg)
    comparetab = tabulation
    comparein = len(inservice)
    for item in list(set(kwl)): #list(set(kwl)) removes duplicates
	if not item in inservice:
		inservice.append(item)
		print "adding " + item + " to the archive looper"
		addr = "http://boards.4chan.org/"+boardtoscan+"/" + item
		thread.start_new_thread(scrubthread, (addr,))
		tabulation = tabulation + 1
    if comparetab != tabulation:
    	print " Number of threads currently in tracking... "+str(tabulation)
    if comparein != len(inservice):
    	print " Total number of threads tracked... "+str(len(inservice))
    time.sleep(.5)
    if not verbose:
	#os.system(clr)
	pass


	
