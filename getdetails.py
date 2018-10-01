print """Content-type: text/html

"""


DEBUG=False

vpath=""
vwithimages=False

vftpuser="ftpuser"  #User of ftp
vftppass="ftppass"  #Pass of ftp
vftphost="ftphost"  #Host of ftp
vftppath="path-to-calibre-libraries"  #path to calibre libraries in ftp, ex: '/users/guess/Calibre-libraries/'


vservercalibre="ftp://"+vftpuser+":"+vftppass+"@"+vftphost+"/"+vftppath
vservercalibrepath="/public/guess/Calibre Library/"


import os
vparams=os.getenv("QUERY_STRING")
#print vparams
#for vvv in vparams.split('&'):

if "withimages" in vparams:
	vwithimages=True

ppp=vparams.split('&')	
for vp in ppp:
		=vp.split('=')
	if DEBUG:
		print aaa
	if len(aaa)>1:
		if aaa[0]=="path":
			vpath=aaa[1]
			

			# print 'wget '+vservercalibre+(vpath.replace('%20',' '))+'/metadata.opf -O temp/metadata.opf'
			# os.system('wget '+vservercalibre+(vpath.replace('%20',' '))+'/metadata.opf -O temp/metadata.opf' )
			
			import ftplib

			HOST = vftphost
			DIRN = vservercalibrepath+(vpath.replace('%20',' '))
			FILE = "metadata.opf"
			IMG = "cover.jpg"

			print " User: "+vftpuser 
			
			f = ftplib.FTP(HOST)
			f.login(vftpuser,vftppass)
			f.cwd(DIRN)			
			
			
			if DEBUG:
				f.retrlines('LIST')
			
			file = open(FILE, 'wb') 
			f.retrbinary('RETR %s' % FILE, file.write)
			file.close()
			f.retrbinary('RETR %s' % IMG, open(IMG, 'wb').write)		
			
			# f.retrbinary('RETR %s' % FILE, 

			f.quit()

			vpath="metadata.opf"
 
if not vpath=="":
	#print vpath.encode('ascii', 'xmlcharrefreplace')
	if os.path.isfile(vpath):
		from xml.dom.minidom import parse
		dom = parse(vpath)
		name = dom.getElementsByTagName('dc:description')
		if DEBUG or vwithimages:
			print "<table><tr><td><img src='cover.jpg'  alt='Portada' width='120' /></td><td>"
		print name[0].firstChild.nodeValue.encode('ascii', 'xmlcharrefreplace')
		if DEBUG or vwithimages:
			print "</td></tr></table>"		
		
		
		
				