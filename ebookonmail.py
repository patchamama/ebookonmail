# 
# -*- coding: utf-8 -*-

#vcoderich

# ver https://github.com/kparal/sendKindle
#sudo apt-get install zip python-xlwt
# crontab -e
# */1 * * * * python /opt/lampp/htdocs/ebookonmail/ebookonmail.py
# * 6 * * * bash /opt/lampp/htdocs/ebookonmail/recipe.sh 

vnewinlastmonths="1" #Definir período en meses para considerar novedades
vcantbookinlistexcel=10800 #Número de libros por archivo excel

vcheckemails=False
vHTMLDetails=True 
vmaxlimitemails=20

## init of definitions variable
vftpuser="ftpuser"  #User of ftp
vftppass="ftppass"  #Pass of ftp
vftphost="ftphost"  #Host of ftp
vftppath="path-to-calibre-libraries"  #path to calibre libraries in ftp, ex: '/users/guess/Calibre-libraries/'

#Email to check what ebook soll to send
vebookonmail_email = 'miemail@gmail.com'
vebookonmail_pass = 'contraseNa'
vebookonmail_imap = 'imap.gmail.com'
vebookonmail_smtp = 'smtp.gmail.com'
vebookonmail_smtpport = 587

vnotnewbooks=["FBS"]  #Fuentes no actualizadas... "KHA","FBS","EXT"
 
vcalibreabssrc='/path-to-calibre-library-in-server'  #ruta al servidor de calibre, por ejemplo /media/users/guest/Calibre-libraries/
vcalibresrc = {}

#Every library is define here (name, path, ..)
#First library of calibre define...	
vbiblio='gutenberg'  #biblio name
vcalibresrc[vbiblio+'name']='gutenberg'  #biblio name
vcalibresrc[vbiblio+'code']='GTB'   #biblio code to reference
vcalibresrc[vbiblio+'vcalibreabssrc']='/media/users/guess/Calibre-libraries/'   # ruta en ftp a bibliotecas
vcalibresrc[vbiblio+'path']='/media/users/guess/Calibre-libraries/gutenberg/'	# ruta en ftp a biblioteca
vcalibresrc[vbiblio+'dbpath']='/media/users/guess/Calibre-libraries/gutenberg/' # ruta en ftp a basedatos metadata.db en biblioteca
vcalibresrc[vbiblio+'id']='id'  		    #not change this
vcalibresrc[vbiblio+'type']='identifiers'	#not change this
vcalibresrc[vbiblio+'preidval']=''			#not change this
vcalibresrc[vbiblio+'postidval']=''			#not change this
vcalibresrc[vbiblio+'format']=''			#not change this
vcalibresrc[vbiblio+'lastupdateid']=999999	#not change this
vcalibresrc[vbiblio+'desc']='libro en gutenberg'
vcalibresrc[vbiblio+'urlid']=''				#not change this
vcalibresrc[vbiblio+'wherelangcode']='"spa"'   #idiomas de la base de datos
vcalibresrc[vbiblio+'ftphost']=vftphost		#not change this
vcalibresrc[vbiblio+'ftpuser']=vftpuser		#not change this
vcalibresrc[vbiblio+'ftppswd']=vftppass		#not change this
vcalibresrc[vbiblio+'ftppath']=vftppath		#not change this
	
#Second library of calibre define...	
vbiblio='feedbooks'
vcalibresrc[vbiblio+'name']='feedbooks'
vcalibresrc[vbiblio+'code']='FBS'
vcalibresrc[vbiblio+'vcalibreabssrc']='/media/users/guess/Calibre-libraries/'
vcalibresrc[vbiblio+'path']='/media/users/guess/Calibre-libraries/feedbooks/'
vcalibresrc[vbiblio+'dbpath']='/media/users/guess/Calibre-libraries/feedbooks/'
vcalibresrc[vbiblio+'id']='id'  		    #not change this
vcalibresrc[vbiblio+'type']='identifiers'	#not change this
vcalibresrc[vbiblio+'preidval']=''			#not change this
vcalibresrc[vbiblio+'postidval']=''			#not change this
vcalibresrc[vbiblio+'format']=''			#not change this
vcalibresrc[vbiblio+'lastupdateid']=999999	#not change this
vcalibresrc[vbiblio+'desc']='libro en gutenberg'
vcalibresrc[vbiblio+'urlid']=''				#not change this
vcalibresrc[vbiblio+'wherelangcode']='"spa"'   #idiomas de la base de datos
vcalibresrc[vbiblio+'ftphost']=vftphost		#not change this
vcalibresrc[vbiblio+'ftpuser']=vftpuser		#not change this
vcalibresrc[vbiblio+'ftppswd']=vftppass		#not change this
vcalibresrc[vbiblio+'ftppath']=vftppath		#not change this

#3,... 4... 5... library of calibre define...

vsrc=('feedbooks', 'gutenberg')
vsrcinlist=('feedbooks', 'gutenberg')  #los que aparecen en el listado de libros
vebookformats=['fb2','epub','azw3','mobi','htmlz','rtf','doc','pdf'] #Orden de calidad de fuente de conversión 

## End of definitions variable

vservercalibre="ftp://"+vftpuser+":"+vftppass+"@"+vftphost+"/"+vftppath
vservercalwebdav=""
ebookpath=''

vresumDB='allebooks.db'
vconfigfile="ebookonmailconfig.py"
vtodolist="booksftp.html"
vnovedades="novedades.html"
vebookonmaillist="ebookonmail-list"
vscriptpostgenlist="publicar.sh"

import sys
argv=""
if len(sys.argv)>=1:
	argv=sys.argv[1:]


	
import imaplib, email, re, shutil
import zipfile, os, sys, getopt, glob
import sqlite3
import logging
import datetime
import mimetypes
import email.mime.application
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib, MimeWriter, mimetools, base64, cgi
import ConfigParser
import optparse
import traceback
from StringIO import StringIO
from email import encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.generator import Generator
from HTMLParser import HTMLParser
parser = HTMLParser()

os.system('unset DISPLAY')



import os
inweb=False
vparams=os.getenv("QUERY_STRING")
if vparams==None:
	pass
elif "sebook" in vparams:
	inweb=True

def utf8_str(p, enc='utf-8'):
    if p is None:
        return None
    if isinstance(p, unicode):
        return p.encode('utf-8')
    if enc != 'utf-8':
        return p.decode(enc).encode('utf-8')
    return p

if os.path.isfile(vconfigfile):
	from ebookonmailconfig import *

print "Chequeando si existen las sinopsis: synopsis.php.htm ..."
if not os.path.isfile('synopsis.php.htm'):
	print "No se encuentra el archivo de sinopsis synopsis.php.htm... ¡Abortando!"
	sys.exit(7)
	
vlast = 0
varFrom=''
vaction=''
vformat=''
vebooknum=''
loczip=''
vebookfileinfo = ''
vsize=0
vnumbooks=0

print "--------------------"
print "eBookOnMail server: "+vebookonmail_email

for src in vsrc:
	print "src: "+src
	print "Biblio "+src+": "+vcalibresrc[src+'path']
	print "Copiando base de datos a local: "+src
	vdblocalroot=vcalibresrc[src+'path']
	vdblocalroot=vdblocalroot.replace(vcalibreabssrc,'')
	#os.system('mkdir -p "'+vdblocalroot+'"')
	#os.system('cp "'+vcalibresrc[src+'path']+'/metadata.db" "'+vdblocalroot+'"')	
	
print "--------------------"

print "Chequeando peticiones..."

def convertebook(ebookfile,vformatin,vformat):	
	vconvertprogram='calibre'
	vscriptpath = os.path.dirname(os.path.abspath(__file__))
	print vscriptpath
	if vformat != vformatin:
		#ebook-convert archivo.fb2 archivo.epub -d debug				
		ebookfileout = os.path.basename(ebookfile)
		shutil.copy2(ebookfile, vscriptpath +'/'+ebookfileout )

		#Try 1 (htmlz to rtf, doc, pdf, odt, ...)
		if vformat.lower() in ["rtf","doc","pdf","odt","txt","wiki"]: #Usar LibreOffice/OpenOffice conversión (mejor que calibre)
			if not vformatin.lower()=="htmlz":
				print "Calibre conviertiendo a htmlz..."
				os.system('/opt/calibre/ebook-convert "'+ebookfileout+'" "'+os.path.splitext (ebookfileout)[0]+'.htmlz"')
			if os.path.isfile( os.path.splitext(ebookfileout)[0]+'.htmlz' ):
				os.system('rm -R "'+vscriptpath +'/temp/"')				
				os.system('unzip -o "'+os.path.splitext(ebookfileout)[0]+'.htmlz'+'" -d temp')	
				os.system('rm "'+os.path.splitext(ebookfileout)[0]+'.htmlz'+'"')	
				print "Chequeando si existe la ruta: "+'"'+vscriptpath +'/temp/index.html"'		
				if os.path.isfile('temp/index.html'):						
					os.system("cat 'temp/index.html' | sed -e 's/<img src/<img width=""60%"" src/g' > 'temp/index1.html'")
					if os.path.isfile('temp/index1.html'):
						print "Renombrando index1.html a index.html..."
						os.system('rm temp/index.html')														
						os.system('mv temp/index1.html temp/index.html')															
					print "SOffice convirtiendo a "+vformat
					os.system('pkill soffice')
					os.system('cd temp && soffice --headless --convert-to '+vformat.lower()+' index.html')	
					#os.system('soffice --headless --convert-to '+vformat.lower()+' --outdir temp temp/index.html')	
					if os.path.isfile( 'temp/index.'+vformat.lower() ):
						print "Copiando temp/index."+vformat.lower()+' a "'+os.path.splitext (ebookfileout)[0]+'.'+vformat+'"'
						shutil.copy2('temp/index.'+vformat.lower(), os.path.splitext (ebookfileout)[0]+'.'+vformat )
					if os.path.isfile( os.path.splitext (ebookfileout)[0]+'.'+vformat ):
						vconvertprogram='soffice'
					

		#Try 2 
		if not os.path.isfile( os.path.splitext (ebookfileout)[0]+'.'+vformat ):
			print ""
			print "Calibre convirtiendo a "+vformat
			os.system('/opt/calibre/ebook-convert "'+ebookfileout+'" "'+os.path.splitext (ebookfileout)[0]+'.'+vformat+'"')
			if not os.path.isfile( os.path.splitext (ebookfileout)[0]+'.'+vformat ):
				ebooks_files = [f for f in os.listdir(ebookpath) if f.endswith('.'+vf)]
				if len(ebooks_files)>1:
					ebookfile = ebookpath+'/'+ebooks_files[1]
					vebookfileinfo = ebooks_files[1]
					vformatin = vf	
					ebookfileout = os.path.basename(ebookfile)
					shutil.copy2(ebookfile, vscriptpath +'/'+ebookfileout )								
					os.system('/opt/calibre/ebook-convert "'+ebookfileout+'" "'+os.path.splitext (ebookfileout)[0]+'.'+vformat+'"')
		if not os.path.isfile( os.path.splitext (ebookfileout)[0]+'.'+vformat ) and \
				(vformat.lower()=="mobi" or vformat.lower()=="azw3" or vformat.lower()=="kf8") and \
				(vformatin.lower()=="epub"):
			os.system('kindlegen/kindlegen "'+ebookfileout+'" -c1 -locale es -o "'+os.path.splitext (ebookfileout)[0]+'.'+vformat+'"')
			os.system('python kindlestrip.py "'+os.path.splitext (ebookfileout)[0]+'.'+vformat+'" "'+os.path.splitext (ebookfileout)[0]+'.'+vformat+'"') 																
		if os.path.isfile( os.path.splitext(ebookfileout)[0]+'.'+vformat ):
			os.system('rm "'+ebookfileout+'"')
			#os.remove(ebookfileout)
			ebookfileout = os.path.splitext (ebookfileout)[0]+'.'+vformat
		else:
			logger.error(varFrom+'|'+vaction+'|'+vgetline+'|'+loczip+'|'+str(vsize)+'k|Error en conversiOn de formato de'+ebookfileout+' a '+vformat)	
			print "Error: "+varFrom+'|'+vaction+'|'+vgetline+'|'+loczip+'|'+str(vsize)+'k|Error en conversiOn de formato de'+ebookfileout+' a '+vformat
	else:
		ebookfileout = os.path.basename(ebookfile)
		shutil.copy2(ebookfile, vscriptpath +'/'+ebookfileout )
	return ebookfileout
		
def mailresponse(mailto, subject, body, bodyhtml, attachtment):
	#Enviar adjunto el loczip
	print "Enviando email con asunto: "+subject+" a "+mailto

	# Create a text/plain message
	msg = email.mime.Multipart.MIMEMultipart()
	msg['Subject'] = subject #'EbookOnMail '+vebooknum
	msg['From'] = vebookonmail_email
	msg['To'] = mailto

	# The main body is just another attachment
	body = email.mime.Text.MIMEText(body)
	msg.attach(body)

	if bodyhtml=='':
		bodyhtml=body
	else:
		vbodyhtml = MIMEText(bodyhtml, 'html')
		msg.attach(vbodyhtml)

	if not attachtment=='':		
		part = MIMEBase('application', "zip")
		b = open(attachtment, "rb").read()
		# Convert from bytes to a base64-encoded ascii string
		#bs = encodebytes(b).decode()
		bs = base64.b64encode(b)
		# Add the ascii-string to the payload
		part.set_payload(bs)
		# Tell the e-mail client that we're using base 64
		part.add_header('Content-Transfer-Encoding', 'base64')
		part.add_header('Content-Disposition', 'attachment; filename="%s"' %
				os.path.basename(attachtment))
		msg.attach(part)
		print "Adjuntando archivo: "+attachtment

	# send via Gmail server
	# NOTE: my ISP, Centurylink, seems to be automatically rewriting
	# port 25 packets to be port 587 and it is trashing port 587 packets.
	# So, I use the default port 25, but I authenticate. 
	s = smtplib.SMTP(vebookonmail_smtp, vebookonmail_smtpport)
	s.starttls()
	s.login(vebookonmail_email,vebookonmail_pass)
	s.sendmail(mailto,[mailto], msg.as_string())
	s.quit()
	return

def send_mail(mailto, subject, body, bodyhtml, attachtment):
        '''Send email with attachments'''

        vconvert=False

        # create MIME message
        msg = MIMEMultipart()
        msg['From'] = vebookonmail_email
        msg['To'] = mailto
        msg['Subject'] = 'Convert' if vconvert else 'Sent to Kindle'
        text = 'This email has been automatically sent by SendKindle tool.'
        msg.attach(MIMEText(text))

        # attach files
        msg.attach(get_attachment(attachtment))

        # convert MIME message to string
        fp = StringIO()
        gen = Generator(fp, mangle_from_=False)
        gen.flatten(msg)
        msg = fp.getvalue()

        # send email
        try:
            mail_server = smtplib.SMTP_SSL(host=vebookonmail_smtp,
                                          port=465)
            mail_server.login(vebookonmail_email, vebookonmail_pass)
            mail_server.sendmail(vebookonmail_email, mailto, msg)
            mail_server.close()
        except smtplib.SMTPException:
            traceback.print_exc()
            message = ('Communication with your SMTP server failed. Maybe '
                       'wrong connection details? Check exception details and '
                       'your config file: %s' % self.conffile)
            print >> sys.stderr, message
            sys.exit(7)

        print('Sent email to %s' % mailto)

def soundexstr(st):
	st=utf8_str(st)
	vst=st.replace("…", " ").replace(".", " ")
	vst=st.replace("  ", " ").strip()
	vst=st.replace("  ", " ").strip()
	vst=st.replace("…", " ").replace(".", " ")
	vst = vst.replace("Á", "a").replace("É", "e").replace("Ñ", "n").replace("Í", "i").replace("Å", "a").replace("å", "a").replace("Ó", "o").replace("ò", "o").replace("Ö", "o").replace("Ü", "u").replace("ū", "u").replace("ī", "i").replace("Č", "c").replace("ć", "c").replace("´","").replace("'","").replace("-"," ").replace("-"," ")
	vst = vst.lower()
	vst = vst.replace("á", "a").replace("é", "e").replace("ê", "e").replace("è", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("è", "e").replace("ø", "o").replace("à", "a").replace("ô", "o").replace("ś", "s")
	vst = vst.replace("ä", "a").replace("ë", "e").replace("ø", "o").replace("ö", "o").replace("ü", "u").replace("š", "s").replace("ç", "c").replace("ï", "i").replace("ñ", "n").replace("m", "n").replace("/", " ").replace("\\", " ").replace("ō", "o")
	vst = vst.replace(":", " ").replace(",", " ").replace(".", " ").replace(";", " ").replace("-", " ").replace("&", " ").replace("!", "").replace("¡", "").replace("?", "").replace("¿", "").replace("i", "y")
	# .replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ")
	vst=' '+vst+' '
	vst=vst.replace(" la ", " ").replace(" de ", " ").replace(" en ", " ").replace(" a ", " ").replace(" y ", " ").replace(" von ", " ").replace(" una ", " ").replace(" el ", " ").replace(" los ", " ").replace(" las ", " ").replace(" su ", " ").replace(" con ", " ").replace(" le ", " ").replace(" , ", ", ").replace(" van ", " ")
	vst=vst.replace(" unas ", " ").replace(" sin ", " ").replace(" sin ", " ").replace(" und "," ").replace(" and "," ").replace(" et "," ")
	vst=vst.replace("as ", "a ").replace("es ", "e ").replace("is ", "i ").replace("os ", "o ").replace("us ", "u ")
	vst = vst.replace("  ", " ").strip()
	
	import re
	vst = re.sub(r" [a-z]\.", "", " "+vst)
	
	if vst.find(" «")>1:
		vst=vst[0:vst.find(" «")]
	if vst.find(" (")>1:
		vst=vst[0:vst.find(" (")]
	if vst.find(" [")>1:
		vst=vst[0:vst.find(" [")]
	return vst.strip()


def get_attachment(file_path):
        '''Get file as MIMEBase message'''

        try:
            file_ = open(file_path, 'rb')
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file_.read())
            file_.close()
            encoders.encode_base64(attachment)

            attachment.add_header('Content-Disposition', 'attachment',
                                  filename=os.path.basename(file_path))
            return attachment
        except IOError:
            traceback.print_exc()
            message = ('The requested file could not be read. Maybe wrong '
                       'permissions?')
            print >> sys.stderr, message
            sys.exit(6)


def createzip(locfile, loczip,passwd,volsize):
	#Comprimir archivo...
	#http://stackoverflow.com/questions/17250/create-an-encrypted-zip-file-in-python
	print "Comprimiento ",locfile," en ",loczip,"..."

	if os.path.isfile(loczip):
		os.remove(loczip)
	
	if volsize=='':	
		os.system('zip "'+loczip+'" "'+locfile+'"')
	else:
		os.system('zip -s '+volsize+' "'+loczip+'" "'+locfile+'"')
	#zip -s 900k 1.zip ebookonmail.py	
	#zip = zipfile.ZipFile (loczip, "w", zipfile.ZIP_DEFLATED)
	#zip.write (locfile,locfile)
	#zip.close()
	if os.path.isfile(loczip):
	 	return loczip
	else:
		return ""

def ebookconvert(filetoconvert,toformat):
 return


def GenList(type, byfield, calibreroot, vprefix, vformat, vcheck, lastupdateid, src, vnewinlastmonths):
	#type=identifiers,customfield,id
	sql=""
	prefix=vprefix

	print "Generando lista de tabla "+calibreroot+" e idenficador "+byfield+" con prefijo: "+prefix+" y formato: "+vformat+" type: "+type

	vdballebooks = sqlite3.connect(vresumDB)
	c = vdballebooks.cursor()

	sqlall = 'delete from books where source="'+vprefix+'";'
	print sqlall
	c.execute(sqlall)

	sqlall = 'delete from data where source="'+vprefix+'";'
	print sqlall
	c.execute(sqlall)
	
	fsqllogs  = open('sqllogs.sql','a')

	print "Conectando con base de datos "+calibreroot+'metadata.db...'
	vdb = sqlite3.connect(calibreroot+'metadata.db')
	vformatbydefault=''
	voperator=' '
	vbyfield=byfield
	if not byfield=='' and not byfield=='id':
		 vbyfield="identifiers.type='"+vbyfield+"' "
		 voperator=' and '
	if not vformat=='':		
		vformatbydefault=voperator+" format='"+vformat+"' "		 
		voperator=' and '
	
	if vnewinlastmonths=="":
		vnewinlastmonths="1"
	if int(vnewinlastmonths)==0 or int(vnewinlastmonths)>10:
		vnewinlastmonths="1"
	vpagesqlfrom=""
	vpagesqlval=", '' "
	
	try:
		sqlpageid = 'select id from custom_columns where label="pages" or label="paginas"'	
		print sqlpageid
		cur = vdb.execute(sqlpageid)
		rows = cur.fetchall()
		if len(rows)>0:
			vpagesqlfrom=" left join custom_column_"+str(rows[0][0])+" pg on books.id=pg.book "	
			vpagesqlval=", pg.value "
	except:
		print("Error: no se encuentra la tabla custom_columns")
		pass
		
	vdballebooks.commit()
	vdb.close()
	
	vdb = sqlite3.connect(calibreroot+'metadata.db')
	c = vdballebooks.cursor()
		
	if type=='identifiers':
		if byfield=='' or byfield=='id':
			sql = """
				select distinct books.id, author_sort, title, strftime("%Y",pubdate), (data.uncompressed_size/1000),  data.format, books.path, series.name, books.series_index, comments.text, inotasimages.val, 
					( SELECT GROUP_CONCAT(t.name) FROM books_tags_link b left join tags t on b.tag=t.id where b.book=books.id GROUP BY b.book )
					"""+vpagesqlval+"""
					, (timestamp BETWEEN datetime( 'now', '-"""+vnewinlastmonths+""" month') AND datetime('now', 'localtime') )
				from books 
							inner join data on books.id=data.book 						
							left join books_series_link on books.id=books_series_link.book
							left join series on books_series_link.series=series.id
							left join comments on books.id=comments.book 
							left join identifiers inotasimages on books.id=inotasimages.book AND inotasimages.type='notes_images'
							left join books_languages_link on books.id=books_languages_link.book
							"""+vpagesqlfrom+"""
				where (1) 
				"""
			# comments.text is not null and comments.text <> ''
			if 	vcalibresrc[src+'wherelangcode']<>"":
				sql = sql+"""
				and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code in ("""+vcalibresrc[src+'wherelangcode']+""") ))"""
			sql = sql+"""
				order by author_sort, pubdate desc, title desc"""	
					# and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code="spa"))
				# order by author_sort, pubdate desc, title desc"""
				
				#left join books_languages_link on books.id=books_languages_link.book
				#and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code="spa"))
		else:
			sql = """
				select distinct identifiers.val, author_sort, title, strftime("%Y",pubdate), (data.uncompressed_size/1000),  data.format, books.path, series.name, books.series_index, comments.text, inotasimages.val,
					( SELECT GROUP_CONCAT(t.name) FROM books_tags_link b left join tags t on b.tag=t.id where b.book=books.id GROUP BY b.book )
					"""+vpagesqlval+"""
					, (timestamp BETWEEN datetime( 'now', '-"""+vnewinlastmonths+""" month') AND datetime('now', 'localtime') )
				from books 
						inner join identifiers on books.id=identifiers.book 
						inner join data on books.id=data.book 						
						left join books_series_link on books.id=books_series_link.book
						left join series on books_series_link.series=series.id
						left join comments on books.id=comments.book
						left join identifiers inotasimages on books.id=inotasimages.book AND inotasimages.type='notes_images'
						left join books_languages_link on books.id=books_languages_link.book 
						"""+vpagesqlfrom+"""
				where
					"""+vbyfield+""" """+vformatbydefault+voperator+""" 
					(1) 
					"""
				# comments.text is not null and comments.text <> ''
			if 	vcalibresrc[src+'wherelangcode']<>"":
				sql = sql+"""
				and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code in ("""+vcalibresrc[src+'wherelangcode']+""") ))"""
			sql = sql+"""
				order by author_sort, pubdate desc, title desc"""	
					
					
				# and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code="spa"))
				# order by author_sort, pubdate desc, title desc"""	
				
				#left join books_languages_link on books.id=books_languages_link.book
				#and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code="spa"))
				
				# left join books_languages_link on books.id=books_languages_link.book  left join languages on books_languages_link.lang_code=languages.id
				# and (languages.lang_code="spa")
			
			# sqlid = 'select distinct identifiers.type from identifiers' 
			# cur = vdb.execute(sqlid)
			# rows = cur.fetchall()
			# if len(rows)>0:
				# print "====\nIdentificadores encontrados:"
				# for identif in rows:	
					# print "   ", identif[0]
				# print "\n====\n"
				
				
	
	if type=='customfield':
		#Localizar la custom_column del campo customfield
		sqlid = 'select id from custom_columns where label="'+byfield+'"'	
		print "SQl Init: "+sqlid
		cur = vdb.execute(sqlid)
		rows = cur.fetchall()
		if len(rows)>0:
			vcustom_no=str(rows[0][0])
			sql = """
			select cast(custom_column_"""+vcustom_no+""".value AS INTEGER), author_sort, title, strftime("%Y",pubdate), (data.uncompressed_size/1000),  data.format, books.path, series.name, books.series_index, comments.text, inotasimages.val,
				( SELECT GROUP_CONCAT(t.name) FROM books_tags_link b left join tags t on b.tag=t.id where b.book=books.id GROUP BY b.book )
				"""+vpagesqlval+"""
				, (timestamp BETWEEN datetime( 'now', '-"""+vnewinlastmonths+""" month') AND datetime('now', 'localtime') )
			from books 
				inner join custom_column_"""+vcustom_no+""" on books.id=custom_column_"""+vcustom_no+""".book 
				inner join data on books.id=data.book 				 
				left join books_series_link on books.id=books_series_link.book
				left join series on books_series_link.series=series.id
				left join comments on books.id=comments.book
				left join identifiers inotasimages on books.id=inotasimages.book AND inotasimages.type='notes_images'
				left join books_languages_link on books.id=books_languages_link.book
				"""+vpagesqlfrom+"""				
			where 
				(1) 
				"""+vformatbydefault
			# comments.text is not null and comments.text <> ''
			if 	vcalibresrc[src+'wherelangcode']<>"":
				sql = sql+"""
				and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code in ("""+vcalibresrc[src+'wherelangcode']+""") ))"""
			sql = sql+"""
				order by author_sort, pubdate desc, title desc"""
			
			#left join books_languages_link on books.id=books_languages_link.book
			#and (books_languages_link.lang_code in (select languages.id from languages where languages.lang_code="spa"))

			#left join books_languages_link on books.id=books_languages_link.book books_languages_link.lang_code=1 and 
	print "\n-------\n"+sql+"\n-----\n"
	if not sql=='': 
		cur = vdb.execute(sql)
		rows = cur.fetchall()
		vlastautor=''
		vlastautor1=''
		vlastautor2=''
		vbgcolor=' bgcolor="#A2B0F9" '
		vbgcolor1=' bgcolor="#A2B0F9" '
		vcountrecord=len(rows)
		if len(rows)>0:
			print "Cantidad de ebooks encontrados:",len(rows)
			listno=1
			#import codecs
			#fwrite = codecs.open(vprefix+'_list'+str(listno)+'.html', "w", "utf-8")
			#fwrite = open(vprefix+'_list'+str(listno)+'.html','w')
			#fnovedades = open(vprefix+'_novedades'+'.html','w')
			
	
			vheadtable = u'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<table cellspacing="0" cellpadding="0" border=1 ><tr bgcolor="#E63B3B"><td align=center ><b>Autor</b></td><td align=center><b>Título</b></td><td align=center ><b>Año</b></td><td align=center ><b>Tamaño</b></td><td  align=center ><b>Referencia</b></td><td align=center ><b>Pedir por Email</b></td><td align=center >Notas/Premios</td></tr>'
			# vheadtable=vheadtable.encode('ascii', 'xmlcharrefreplace')
			#fwrite.write(vheadtable)
			#fnovedades.write(vheadtable)
			a=0

			vnew=0

			if not os.path.isfile('premios.sql'):
				fsqlgold = open('premios.sql','a')
				fsqlgold.write('')
				fsqlgold.close() 
			
			if vcheck:
				febookstatus = open('ebookstatus.log','a')
				febookstatus.write('\n-----')
				febookstatus.write('\nBiblioteca: '+calibreroot)
				febookstatus.write('\nSQL: '+sql)
				febookstatus.write('\n-----')
				febookstatus.write('\nEbooks sin contenido (archivos):')
			ebno=0
			eberr=0
			lastebookcode=''
			vprintautor=''
			vauthgold=""
			
			for ebook in rows:	
				ebno=ebno+1		
				try:
					print ebook[0], ebook[1], ebook[2], ebook[3], ebook[4], ebook[5]
				except:
					pass				
				
				# vnewbook='0'
				vnewbook=str(int(ebook[13]))  #si el libro se ha añadido en el último mes...
				vnewbook=vnewbook.strip()
			
				#Actualizar algunos datos...
					
				vauthor=" "+ebook[1]+" "
				vauthor=vauthor.replace(" De "," de ").replace(" Del "," del ").replace(" Von "," von ").replace(" Van "," van ").replace(" Di "," di ")
				vauthor=vauthor.replace("  "," ").replace("'","`")
				vauthor=vauthor[:50]
				vauthor=vauthor.strip()
				
				vtitleInit=ebook[2].replace(". ",".")
				vtitleInit=vtitleInit.replace(" De "," de ").replace(" Del "," del ").replace(" La "," la ").replace(" En "," en ").replace(" Un "," un ").replace(" Y "," y ").replace(" El "," el ")
				vtitleInit=vtitleInit.replace(".",". ")
				for x in range(1, 5):
					vtitleInit=vtitleInit.replace("(c. "+str(x)+")","")	
					vtitleInit=vtitleInit.replace("(v. "+str(x)+")","")
				vtitleInit=vtitleInit.replace("(s)","s")
				vtitleInit=vtitleInit.replace("NO","No")
				vtitleInit=vtitleInit.replace("- (","(")				
				vtitleInit=vtitleInit.replace("  "," ")
				vtitleInit=vtitleInit.replace("( ","(")
				vtitleInit=vtitleInit.replace(" )",")")
				vtitleInit=vtitleInit.strip()				
				vtitleInit2=""
				try:
					 # vtitleInit2=vtitleInit.decode('utf-8')	 
					 vtitleInit=utf8_str(vtitleInit)
					 vtitleInit2=vtitleInit
				except:
					 try:
						 vtitleInit2=vtitleInit.encode('utf-8')	
					 except:
						vtitleInit2=vtitleInit
				

				vlines = file('replace.txt')						
				vtype=""
				for gline in vlines:
					if gline[:1]==":":
						vtype=gline
					if ">" in gline:
						#if vtype==":Author":
							gline=gline.split(">")
							vvvfor=gline[0].strip().decode('utf-8')	
							vvvto=gline[1].strip().decode('utf-8')
							# vvvfor=utf8_str(gline[0].strip())
							# vvvto=utf8_str(gline[1].strip())			
							
							vauthor=vauthor.replace(vvvfor,vvvto).strip()				
					if "::" in gline:
						#if vtype==":Author":
							gline=gline.split("::")
							vvvfor=utf8_str(gline[0])
							vvvfor=vvvfor.strip()
							vvvto=utf8_str(gline[1])
							vvvto=gline[1].strip()
							# vvvfor=utf8_str(gline[0].strip())
							# vvvto=utf8_str(gline[1].strip())								
							vtitleInit=vtitleInit.replace(vvvfor,vvvto).strip()				
							
				vfollow=True
				
				vvid = str(ebook[0])
				try:
					vvid=str(int(vvid.replace(".0","")))
				except:
					vvid=""
					vfollow=False
					
				print "vvid: ",vvid				
				

				# if vprefix=='EXT' and ("-" in vtitleInit or "." in vtitleInit):
					# vfollow=False

				if lastebookcode==str(ebook[0]):
					vfollow=False
				else:
					lastebookcode=str(ebook[0])
					
				if "(cat)" in vtitleInit.lower() or "(gal)" in vtitleInit.lower() or "(por)" in vtitleInit.lower():
					vfollow=False
						
				if vfollow:
					ebookpath = calibreroot+ebook[6]
					if vcheck and ebno>0:	
						ebookfile=''	
						verrortype='ebook '+ebook[6]+' not found'
						if os.path.isdir(ebookpath):
							for vf in vebookformats:
								if ebookfile=='':
									print 'Buscando ('+str(ebno)+'/'+str(vcountrecord)+'|'+str(eberr)+') '+vf+' en '+ebookpath+'...'
									ebooks_files = [f for f in os.listdir(ebookpath) if f.endswith('.'+vf)]
									if len(ebooks_files)>0:
										ebookfile = ebookpath+'/'+ebooks_files[0]
										vebookfileinfo = ebooks_files[0]
										vformatin = vf
										vfilesize = str(os.path.getsize(ebookfile))

										sqlall = 'insert into data values(null, "'+vprefix+vvid+'", "'+vprefix+'", "'+vf+'", "'+vfilesize+'", "'+ebookfile+'");'
										print "            "+sqlall
										c.execute(sqlall)
										
										#create table if not exists data(id int, code varchar(20), source varchar(10), format varchar(5), size varchar(6), path varchar(150));

						else:
							verrortype='\ndirectory '+ebookpath+' not found'
						if ebookfile=='':
							eberr=eberr+1
							# .encode('ascii', 'xmlcharrefreplace')
							febookstatus.write('\n'+verrortype+'|'+str(ebook[0])+'|'+vauthor+'|'+vtitleInit+'|'+ebook[3]+'|'+str(ebook[4])+'|'+ebook[5]+'|'+ebook[6])
							print '\n'+'Ebook no encontrado...'

					vtautor=vauthor.strip()
					vtautor=utf8_str(vtautor)
					vreplacefile = file('replace.txt')
					for vrline in vreplacefile:
					  if vrline.lower().strip()==":author":
						vreplatyp="author"
					  if vreplatyp=="author":						
						vrline=vrline.strip().split(">")
						if len(vrline)==2:
							try:
								if vrline[0].lower().replace("  "," ").strip() in vtautor.lower().replace("  "," "):
									vtautor=vauthor
									vtautor=vtautor.replace(vrline[0].strip(),vrline[1].strip())
							except:
								pass
							

					print vlastautor2," vs ",vtautor," --- ",vtautor
					if not vlastautor.strip()==vtautor.strip() and not vlastautor2==vtautor:
						vlastautor2=vtautor
						vlastautor=vtautor #.encode('ascii', 'ignore')  
						vprintautor=vlastautor
						if len(vprintautor)>50:
							vprintautor=vprintautor[:50]+'...'
						vprintautor='<td align=center >'+vprintautor+'</td>'	
						vbgcolor= ' bgcolor="#A2B0F9" '

						vauthgold=""

						if a>=vcantbookinlistexcel:
							a=0
							#fwrite.write("</table>")
							#fwrite.close()
							
							listno=listno+1
							#fwrite = open(vprefix+'_list'+str(listno)+'.html','w')			
							#fwrite.write(vheadtable)
					else:
						vbgcolor= ''
						vprintautor='<td></td>'
	
					vnote=''
					vnotestyle=''
					visnew=False
					
					# vnewbook='0'
					# print "new? lastupdateid<vvid",lastupdateid,"",vvid
					# if int(vvid)>lastupdateid:  #1 lista: 23469 (abril)
					if vnewbook=='1':
						visnew=True
						# vnewbook='1'
						if vnote=='':
							vnote='New'
							vnotestyle=' align=center bgcolor="#E63B3B"'
							vnew=vnew+1
						else:
							vnote=vnote+',New'
				
					a=a+1
					if ebook[4]==0:
						vsize='-'
					else:
						vsize=str(ebook[4])
					vdate=ebook[3]
					if vdate=='0100' or vdate=='0101' or vdate=="0180":
						vdate='-'
					vautor=vtautor
					if len(vautor)>40:
						vautor=vautor[:40]

					vtitle=vtitleInit.replace("  ", " ").strip()
					vtitle=vtitleInit.replace("  ", " ").strip()

					vlastautor = vlastautor.replace('"', "'").replace("  ", " ").strip()

					#Chequear las obras y autores con premios...					
					# vauthorwords=soundexstr(vtautor.encode('utf-8'))
					vauthorwords=soundexstr(vtautor)
					vauthorwords=vauthorwords.split()

					#vtitle=vtitleInit.encode('ascii', 'xmlcharrefreplace').replace("  ", " ").strip()	
					vtitlewords=soundexstr(vtitleInit)
					vtitlewords=vtitlewords.split()

					vgoldtype=""					
					vobragold=""
					vgoldvalue=""
					vpremio=""

					#import codecs
					#goldfile = codecs.open('premios.txt', "r", "utf-8")

					if False:
						goldfile = file('premios.txt')						
						for gline in goldfile:
						  vline=gline.strip()

						  if len(vline)>0 and len(vlastautor)>0 and len(vtitle)>0:
							#vline=vline.encode('ascii', 'xmlcharrefreplace')
		
							vline=soundexstr(vline)

							if gline[:1]==">":
								vgoldvalue=gline[1:]
								vgoldvalue=vgoldvalue.strip()
								vgoldtype="auth"
							else: 
								if gline[:1]=="#":
									vgoldvalue=gline[1:]
									vgoldvalue=vgoldvalue.strip()
									vgoldtype="book"
								else:
									#if vauthgold=="":
									vauthorpremium=False
									vinit=True
									for vword in vauthorwords:
									  if vauthorpremium or vinit:
										vinit=False
										if vword in vline:
											vauthorpremium=True
										else:
											vauthorpremium=False
									if vgoldtype=="auth":
										if vauthorpremium:
											#cgi.escape(vgoldvalue)
											try:
												 vpremio= "<span style='background-color: green;'>"+vgoldvalue+"</span>"
											except:												
												 vpremio= "<span style='background-color: green;'>"+vgoldvalue.encode('ascii', 'xmlcharrefreplace')+"</span>"											
											
											# if not '("'+vtautor.encode('utf-8')+'","'+vgoldvalue in open('premios.sql').read():
											if not '("'+utf8_str(vtautor)+'","'+vgoldvalue in open('premios.sql').read():
												fsqlgold = open('premios.sql','a')
												# fsqlgold.write('insert into authpremium values("'+vtautor.encode('utf-8')+'","'+vpremio.replace('"','')+'")'+"\n")
												fsqlgold.write('insert into authpremium values("'+utf8_str(vtautor)+'","'+vpremio.replace('"','')+'")'+"\n")
												fsqlgold.close()


									if vgoldtype=="book":
										if vauthorpremium:
											vbookpremium=False
											vinit=True
											for vword in vtitlewords:
												if vbookpremium or vinit:
													vinit=False
													if vword in vline:
														vbookpremium=True
													else:
														vbookpremium=False
											if not vbookpremium:
												vtitleInit2split=vtitleInit2.split()
												for vword in vtitleInit2split:
													if vbookpremium or vinit:
														vinit=False
														if vword in vline:
															vbookpremium=True
														else:
															vbookpremium=False											
											if vbookpremium:		
												try:
													vpremio= "<span style='background-color: yellow;'>"+vgoldvalue+"</span>"
													vptext=vgoldvalue
												except:												
													vpremio= "<span style='background-color: yellow;'>"+vgoldvalue.encode('ascii', 'xmlcharrefreplace')+"</span>"	
													vptext=vgoldvalue.encode('ascii', 'xmlcharrefreplace')
												if not '("'+vprefix+str(ebook[0])+'","'+vgoldvalue in open('premios.sql').read():
													fsqlgold = open('premios.sql','a')									
													# fsqlgold.write('insert into obrapremium values("'+vprefix+vvid+'","'+vpremio.replace('"','')+'","'+vtautor.encode('utf-8')+'","'+vtitleInit.encode('utf-8', 'ignore')+'")'+"\n")
													fsqlgold.write('insert into obrapremium values("'+vprefix+vvid+'","'+vpremio.replace('"','')+'","'+utf8_str(vtautor)+'","'+utf8_str(vtitleInit)+'")'+"\n")
													fsqlgold.close()
													
													fsss = open('calibre-premios.txt','a')
													fsss.write("\n"+vprefix+vvid+'###'+vptext)
													fsss.close()	



					vpremio=("") if ebook[11]==None else ebook[11]
					vpagesno=("") if ebook[12]==None or ebook[12]=="" else str(ebook[12])+"p"
					

					
					if not vpremio=="":
						vnotestyle=' align=center bgcolor="yellow"'
						if vnote=="":
							vnote=vpremio
						else:
							vnote=vnote+", "+vpremio
							
					vserie1=("") if ebook[7]==None else ebook[7]
					# try:
						# vserie.encode('ascii', 'ignore')						 
					# except:
						 # try:
							 # vserie=vserie.decode('utf-8')	
						 # except:
							# vserie=vserie	
					vserie1=vserie1.strip().replace("  "," ")
					vserie=vserie1
					try:
						 # vserie=vserie1.decode('utf-8')	
						 vserie=utf8_str(vserie1)
						 
					except:
						 try:
							 vserie=vserie1		
						 except:
							vserie=vserie1.encode('ascii', 'ignore')							
					if not vserie.strip()=="":
						vserieno=str(ebook[8])
						vserie='('+vserie+' '+(vserieno.replace(".0",""))+')'
						vserie=vserie.replace('"','')
						
					vcoments=("") if ebook[9]==None else utf8_str(ebook[9])
					vcoments=vcoments.replace('"',"'").replace("\n"," ").replace("\r"," ")
					vnotesimages=(vpagesno) if ebook[10]==None else str(ebook[10])+"/"+vpagesno
					if ebook[10]==None:
						vnotesimages=vpagesno
					else:
						vnotesimages=str(ebook[10])
						if not vpagesno=="":
							vnotesimages=vnotesimages+"/"+vpagesno
							
					while vnotesimages[0:1]=="0":
						vnotesimages=vnotesimages[1:]
					if vnotesimages[0:1]=="n":
						vnotesimages="0"+vnotesimages
					
					#vsoundauth = soundexstr(vlastautor)
					try:
						# vsoundauth = soundexstr(vtautor.encode('utf-8'))
						vsoundauth = soundexstr(utf8_str(vtautor))						
						sqlall = 'insert into books values(null, "'+vprefix+vvid+'", "'+vprefix+'", "'+vautor+'", "'+'", "'+vdate+'", "'+vlang+'", "'+ebookpath+'", "'+vsoundauth+'", "'+'", "'+vsoundauth1+'", "'+'","","'+vnewbook+'", "'+vserie+'", "'+vcoments+'", "'+vnotesimages+'", "'+vpremio+'");'
						print "pass vsoundauth 1"
					except: 
						vsoundauth = soundexstr(vlastautor)
						print "pass vsoundauth 2"
					  	pass

					vsoundauth = vsoundauth.replace("'", "").replace('"', '')

					vsoundauth1 = vsoundauth.replace("v", "b").replace("ch", "k").replace("sh", "k").replace("s", "k").replace("z", "k").replace("c", "k").replace("gu", "g").replace("qu", "k").replace("r", "l")
					vsoundauth1 = vsoundauth1.replace("j", "y").replace("ll", "y").replace("i", "y").replace("?", " ").replace("¿", " ").replace('  ', ' ').strip()


					try:
						vtitle = vtitleInit.replace('"', '""')
						# vsoundtitle = soundexstr(vtitleInit.encode('utf-8'))
						vsoundtitle = soundexstr(utf8_str(vtitleInit))						
						vsoundtitle = vsoundtitle.replace("'", "").replace('"', '')
						sqlall = 'insert into books values(null, "'+vprefix+vvid+'", "'+vprefix+'", "'+vautor+'", "'+vtitle+'", "'+vdate+'", "'+vlang+'", "'+ebookpath+'", "'+vsoundauth+'", "'+vsoundtitle+'", "'+vsoundauth1+'", "'+'","","'+vnewbook+'", "'+vserie+', "'+vcoments+'", "'+vnotesimages+'", "'+vpremio+'");'
						print "pass vtitle 1"
					except: 
						vtitle = vtitleInit.replace('"', '""')
						vsoundtitle = soundexstr(vtitle)
						vsoundtitle = vsoundtitle.replace("'", "").replace('"', '')
						print "pass vtitle 2"
					  	pass				
					

					vsoundtitle1 = vsoundtitle.replace("v", "b").replace("ch", "k").replace("sh", "k").replace("s", "k").replace("z", "k").replace("c", "k").replace("gu", "g").replace("qu", "k").replace("r", "l")
					vsoundtitle1 = vsoundtitle1.replace("j", "y").replace("ll", "y").replace("i", "y").replace("?", " ").replace("¿", " ").replace('  ', ' ').strip()

					#vautor=vtautor.encode('ascii', 'ignore').replace("  ", " ").strip()


					# print "  "
					# print "autor0: ",vtautor, len(vtautor)
					# print "autor1: ",vautor, len(vautor)
					# print "autor2: ",vtautor.encode('ascii', 'ignore').replace("  ", " ").strip()
					# print "autor3: ",vtautor.encode('utf-8', 'ignore').replace("  ", " ").strip()
					# print "autor4: ",vtautor.encode('ascii', 'xmlcharrefreplace').replace("  ", " ").strip()	
					# print "autor5: ",vtautor.encode('utf-8', 'xmlcharrefreplace').replace("  ", " ").strip()
					
					vlang='es'					
					
					print "  "
					vautor=utf8_str(vautor)
					vtitle=utf8_str(vtitle)
					print "Autor: ",vautor+" "
					print "Title: ",vtitle+" "
					print "vsoundauth: ",vsoundauth+" "
					print "vsoundtitle: ",vsoundtitle+" "
					print "vsoundauth1: ",vsoundauth1+" "
					print "vsoundtitle1: ",vsoundtitle1+" "
					print "comment: ",vcoments+" "
					vpartttt=utf8_str(vdate)+'", "'+utf8_str(vlang)+'", "'+utf8_str(ebookpath)+'", "'+utf8_str(vsoundauth)+'", "'+utf8_str(vsoundtitle)+'", "'+utf8_str(vsoundauth1)+'", "'+utf8_str(vsoundtitle1)+'","","'+utf8_str(vnewbook)+'", "'+utf8_str(vserie)+'", "'
					print "test2: ",vautor+'", "'+vtitle
					print "test3: ",vpartttt+vcoments
					print "test1: ",vautor+'", "'+vtitle+'", "'+vpartttt+vcoments
					print "test: ",vprefix+vvid+'", "'+vprefix+'", "'+vautor+'", "'+vtitle+'", "'+vpartttt+vcoments
					print "  "

					#if ebno==284:
					
					#if ebno>285:
					#	sys.exit(7)
					
					

					
					# vserie1=("") if ebook[7]==None else ebook[7].encode('ascii', 'ignore')
					# print "Serie: ",vserie," - ",ebook[7]," ... ",vserie1
					sqlall = 'insert into books values(null, "'+vprefix+vvid+'", "'+vprefix+'", "'+(vautor.replace('"',''))+'", "'+(vtitle.replace('"',''))+'", "'+vpartttt+vcoments+utf8_str('", "'+vnotesimages)+utf8_str('", "'+vpremio.replace('"',''))+'", "'+vsize+'");'
					print "            "+sqlall
					fsqllogs.write('\n'+sqlall)

#Filtro 					
					#if not "La ciudad y los perros (377)" in sqlall:
					c.execute(sqlall)
								

					try:
						vnote=utf8_str(vnote)
					except:
						vnote=vnote.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
					
					print "Nota: ",vnote 

					#fwrite.write('<tr'+vbgcolor+'>'+vprintautor+'<td align=left >'+vtitleInit.encode('ascii', 'xmlcharrefreplace')+'</td><td align=center >'+vdate+'</td><td align=center >'+vsize+'</td><td align=center >'+prefix+str(ebook[0])+'</td><td align=center ><a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vprefix+str(ebook[0])+'">Pedir</a></td><td'+vnotestyle+'>'+vnote+'</td></tr>')				
					if not vnote=='':
						if not vlastautor1==vtautor:
							vlastautor1=vtautor	
							vbgcolor1= ' bgcolor="#A2B0F9" '							
						else:
							vbgcolor1= ''

					# if visnew:					
						# fnovedades.write('<tr'+vbgcolor1+'>'+vprintautor+'<td align=left >'+vtitleInit.encode('ascii', 'xmlcharrefreplace')+'</td><td align=center >'+ebook[3]+'</td><td align=center >'+vsize+'</td><td align=center >'+prefix+str(ebook[0])+'</td><td align=center ><a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vprefix+str(ebook[0])+'">Pedir</a></td><td'+vnotestyle+'>'+vnote+'</td></tr>')				

			#fwrite.write("</table>")
			#fwrite.close()
			
			#fnovedades.write("</table>")
			#fnovedades.close()
			
			print "\n------\nCantidad de ebooks encontrados:",len(rows)
			
			if vcheck:
				febookstatus.write('\n'+str(eberr)+' errores encontrados...')
				febookstatus.close()
		else:
			print "\n------\nNo se encuentran registros con campo "+byfield+" y formato "+vformat+" en biblioteca calibre..."
			print sql+"\n------\n"

	vdballebooks.commit()
	vdb.close()

	c.close()
	fsqllogs.close()
	vdballebooks.close()
	return 

def getebookpath_fromidentifiers(identifierid, identifierfield, calibreroot, ebookroot):
	#Localizar ruta en biblioteca calibre...
	ebookpath=''
	vdb = sqlite3.connect(calibreroot+'metadata.db')
	
	# sqlid = 'select distinct identifiers.type from identifiers' 
	# cur = vdb.execute(sqlid)
	# rows = cur.fetchall()
	# if len(rows)>0:
		# print "====\nIdentificadores encontrados:"
		# for identif in rows:	
			# print "   ", identif[0]
		# print "\n====\n"	

	if identifierfield=='id':
		sql = 'select books.path, books.author_sort, books.title, strftime("%Y",books.pubdate) from books where books.id='+identifierid
	else:
		sql = 'select books.path, books.author_sort, books.title, strftime("%Y",books.pubdate) from books inner join identifiers on books.id=identifiers.book where identifiers.type="'+identifierfield+'" and identifiers.val="'+identifierid+'"'
	cur = vdb.execute(sql)
	rows = cur.fetchall()
	if len(rows)>0:
		#print rows[0][0]
		ebookpath = ebookroot+rows[0][0]
		print "Ruta del libro ("+identifierfield+"): "+ebookpath
	else:
		print "\n------\nNo se encuentra "+identifierid+" en campo "+identifierfield+" de biblioteca calibre..."
		print sql+"\n------\n"
		return "", "", "", ""

	vdb.close()
	return ebookpath, rows[0][1], rows[0][2], rows[0][3]


def getebookpath_fromcustom(customid,customfield,calibreroot,ebookroot):
	print "Localizando "+customid+" en campo "+customfield+" de biblioteca calibre..."
	#Localizar ruta en biblioteca calibre...
	ebookpath=''
	vdb = sqlite3.connect(calibreroot+'metadata.db')

	# sqlid = 'select distinct label from custom_columns' 
	# cur = vdb.execute(sqlid)
	# rows = cur.fetchall()
	# if len(rows)>0:
		# print "====\nCustomfields encontrados:"
		# for identif in rows:	
			# print "   ", identif[0]
		# print "\n====\n"	
		
	#Localizar la custom_column del campo customfield
	sqlid = 'select id from custom_columns where label="'+customfield+'"'
	
	cur = vdb.execute(sqlid)
	rows = cur.fetchall()
	if len(rows)>0:
		vcustom_no=str(rows[0][0])
		# Localizar la ruta del libro
		# select books.path from books inner join custom_column_4 on books.id=custom_column_4.book where value=2442.0
		sqlpath = 'select books.path, books.author_sort, books.title, strftime("%Y",books.pubdate) from books inner join custom_column_'+vcustom_no+' on books.id=custom_column_'+vcustom_no+'.book where value='+customid
		cur = vdb.execute(sqlpath)
		rows = cur.fetchall()
		if len(rows)>0:
			ebookpath = ebookroot+rows[0][0]
			print "Ruta del libro ("+customfield+"): "+ebookpath
		else:
			print "\n------\nNo se encuentra "+customid+" en campo "+customfield+" de biblioteca calibre..."
			print sqlid
			print sqlpath+"\n------\n"
	else:
		print "Error: No se ha encontrado la columna personalizada en biblioteca con el campo "+customfield+"..."
		logger.error("No se ha encontrado la columna personalizada en biblioteca con el campo "+customfield+"...")	

	vdb.close()
	return ebookpath, rows[0][1], rows[0][2], rows[0][3]

#=============================

try:
	logger = logging.getLogger('ebookonmail')
	hdlr = logging.FileHandler('ebookonmail.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.WARNING)
except:
	pass

if len(sys.argv)==1 and vcheckemails:		
	if os.path.isfile('lastemail.log'):
		fread = open('lastemail.log','r')
		for line in fread:
		    if line=='':
			vlast=0
		    else:
		    	vlast = int(line);
		fread.close()
	print "Lastmessage: ",vlast

	# for src in vsrc:
		# if not os.path.isfile(vcalibresrc[src+'path']+'metadata.db'):
			# print 'Error: No se encuentra la base de datos de '+src+' en '+vcalibresrc[src+'path']+'metadata.db'
			# logger.error('No se encuentra la base de datos de '+src+' en '+vcalibresrc[src+'path']+'metadata.db')
			# sys.exit()

	mail = imaplib.IMAP4_SSL(vebookonmail_imap)
	
	#mail = imaplib.IMAP4(vebookonmail_imap, 143)
	
	mail.login(vebookonmail_email, vebookonmail_pass)
	mail.select('inbox')

	mail.select(readonly=1) # Select inbox or default namespace
	(retcode, messages) = mail.search(None, '(UNSEEN)')
	print "Procesando mensajes: ",messages
	if retcode == 'OK':  
	    for num in messages[0].split(' '):
	     if len(num)>0:
	      if vlast==0 or int(num)>vlast:
		print 'Processing :', num, '/', messages[0]
		typ, data = mail.fetch(num,'(RFC822)')
		if typ == 'OK' and isinstance(data, (list)):

			vlast = int(num)
		
			fwrite = open('lastemail.log','w')
			fwrite.write(str(vlast))
			fwrite.close()

			msg = email.message_from_string(data[0][1])

			vsize=0
			varSubject = msg['subject']
			varFrom = msg['from'].lower().replace('@googlemail.','@gmail.').strip()
		
			varFromOnlyEmail=varFrom
			if '<' in varFromOnlyEmail:
				varFromOnlyEmail = re.sub(r'.*<(.*)>.*', r'\1', varFrom)
			#varFrom = varFrom.replace('<', '')
			#varFrom = varFrom.replace('>', '')
			#print data,'\n',30*'-','\n'
			print 'From: ', varFrom, '\n', 'Subject: ', varSubject, '\n'
			vallmesg = data[0][1]
			#print vallmesg,'\n',30*'-'	



			vfollow=True
			if os.path.isfile('spam.txt'):	
				print "Checking if the email is in spamlist..."
				for line in open('spam.txt'):	
					line=line.strip()
					if line.lower() in varSubject.lower():
						vfollow=False
					if line.lower() in varFrom.lower():
						vfollow=False					
			if "Re:" in varSubject or "Fwd:" in varSubject :
				vfollow=False
			if "failed" in varSubject:
				vfollow=False		
			if not os.path.isfile('emaillist.txt'):		
				with open('emaillist.txt', "a") as myfile:
						myfile.write('')		
						
			varSubjects=varSubject.replace(";",",").split(",")
			vallto=''
			if 'to ' in varSubject.lower():
				vvvp=varSubject.lower().index('to ')
				if vvvp>1:
					vvvp=vvvp+3
					vallto=varSubject[vvvp:]
				
			if vfollow:		
			  for varSubject in varSubjects:
				if not varFromOnlyEmail in open('emaillist.txt').read():
					with open('emaillist.txt', "a") as myfile:
						myfile.write('\n'+varFromOnlyEmail)

				vaction = ''
				vformat = ''
				vebooknum = ''	
				vtoemail = ''
				vattachment = ''

				vcalibrebiblio = ''
				vgetline = ''

				m = re.search("((LIST)+\s*)(TO\s+(.*))*",varSubject.upper().strip())
				if m:
					vaction = 'list'
					vformat = ''
					vcalibrebiblio = m.groups()[2]
					vebooknum = ''			
					vtoemail = (m.groups()[3]) if not m.groups()[3]==None else "" 

				if not m:
				    m = re.search("((UPDATE)+\s*)([A-Z]*)",varSubject.upper().strip())
				    if m:
						vaction = 'update'
						vformat = ''
						vcalibrebiblio = m.groups()[2]
						vebooknum = ''			
						vtoemail = ''

				if not m:
					m = re.search("((AYUDA|HELP)+\s*)(TO\s+(.*))*",varSubject.upper().strip())
					if m:					
						vaction = 'ayuda'
						vformat = ''
						vcalibrebiblio = ''
						vebooknum = ''
						vtoemail = (m.groups()[3]) if not m.groups()[3]==None else "" 

				print "Subject: ",varSubject,m		
				if not m:
					m = re.search("((CONVERT)\s*)([A-Z,2,3,8]*)(\s+TO\s+(.*))*",varSubject.upper().strip())
					if m:
						vaction = 'convert'
						vformat = m.groups()[2]
						vtoemail = (m.groups()[4]) if not m.groups()[3]==None else "" 
						print "action:",vaction," format:",vformat," to:",vtoemail 
												
						#Check if any attachments at all
						if msg.get_content_maintype() != 'multipart':
							sys.exit()
							
						import re
						name_pat = re.compile('name=\".*\"')							
						
						# we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
						for part in msg.walk():
							# multipart are just containers, so we skip them
							if part.get_content_maintype() == 'multipart':
								continue
							# is this part an attachment ?
							if part.get('Content-Disposition') is None:
								continue
								
							file_type = part.get_content_type().split('/')[1]
							if not file_type:
								file_type = 'epub'
							vformatin = file_type

							filename = part.get_filename()
							if not filename:
								filename = name_pat.findall(part.get('Content-Type'))[0][6:-1]

							counter = 1
							if not filename:
								filename = 'file-%03d%s' % (counter, file_type)
								counter += 1								
								
							# filename = part.get_filename()
							# counter = 1
							# if there is no filename, we create one with a counter to avoid duplicates
							# if not filename:
								# filename = 'part-%03d%s' % (counter, 'bin')
								# counter += 1
								
							from email.header import decode_header	
							if decode_header(filename)[0][1] is not None:
								filename = str(decode_header(filename)[0][0]).decode(decode_header(filename)[0][1])

							detach_dir="convert"
								
							filename=filename.encode('utf-8')	
							att_path = os.path.join(detach_dir, filename)
							#Check if its already there
							if not os.path.isfile(att_path) :
								# finally write the stuff
								fp = open(att_path, 'wb')
								fp.write(part.get_payload(decode=True))
								fp.close() 	
							print "Attachment ---",att_path,"--- descargado y grabado..."
							if os.path.isfile(att_path):
								vattachment=att_path
						
				if not m:
					m = re.search("((GET)?\s*)([A-Z,2,3]*\s+)*([A-Z]*)(\d+)(\s+TO\s+(.*))*",varSubject.upper().strip())
					if m:
						vaction = 'sendebook'
						vformat = m.groups()[2]
						vcalibrebiblio = m.groups()[3]	
						vebooknum = m.groups()[4]
						vtoemail = m.groups()[6]
					else:	
						vaction="ayuda"
						
					
				if m:
					print m.groups()
					print "Action: ",vaction
					print "Format: ",vformat 
					print "Calibrebiblio: ",vcalibrebiblio
					print "Ebookno: ",vebooknum
					print "ToEmail: ",vtoemail

				    # m = re.search("((GET)?\s*)([A-Z,2,3]*\s+)*([A-Z]*)(\d+)(\s+TO\s+(.*))*",vallmesg.upper().strip())
				    # if m:
						# vaction = 'sendebook'
						# vformat = m.groups()[2]
						# vcalibrebiblio = m.groups()[3]
						# vebooknum = m.groups()[4]

				if vformat==None:
					vformat="RTF"
				print '\n',30*'-','\n',"Biblio: "+vcalibrebiblio
				print "Action: "+vaction
				print "Referencia (ebooknum): "+vebooknum
				print "Formato: ",vformat
				print "To: "+varFrom,'\n',30*'-'

				vtoemail=(vallto) if vtoemail=='' else vtoemail
									
				#Chequear si ya se envió este email anteriormente...
				if False:
					if vaction == 'sendebook':
						logtexts = file('ebookonmail.log')						
						for logtext in logtexts:
							logtext=logtext.lower()
							if 	("get"+vformat.lower()+" "+vcalibrebiblio.lower()+vebooknum+"|" in logtext) or \
								("get"+vformat.lower()+" "+vebooknum+"|" in logtext):
								if "WARNING" in logtext:
									if varFrom.lower() in logtext:				
										vaction = 'repeated'			
			
				if vaction == 'list':
					vcalibrebiblio = vcalibrebiblio.upper()
					# for src in vsrc:						
						# print "Biblio "+src+": "+vcalibresrc[src+'path']
						# if vcalibrebiblio==vcalibresrc[src+'code'].upper() or vcalibrebiblio=='':
					volext=0				
					vaction = 'ayuda'
					if not vtoemail.strip()=='':
						varFrom=vtoemail.lower().strip()
					
					for zipfile in glob.glob("toshare/"+vebookonmaillist+"*.zip"):
						volext=volext+1		
						print "Enviando..."+zipfile
						mailresponse(varFrom,'Re: EbookOnMail List  ('+str(int(volext))+")","El adjunto contiene un listado excel con todos los libros de varias fuentes de bibliotecas electrónicas. Una vez descomprimido el zip, puede ver el listado de libros en excel y proceder a localizar los libros y hacer peticiones enviando un email a ebookonmail@gmail.com y especificando en el asunto el código del libro que desea solicitar.",'',zipfile)	
						logger.warning(varFrom+'|'+vaction+'| - |'+zipfile+'| - |'+vcalibrebiblio+str(int(volext)))									
					
					for zipfile in glob.glob("toshare/novedades*.zip"):
						print "Enviando..."+zipfile
						mailresponse(varFrom,'Re: EbookOnMail Novedades ',"El adjunto contiene un listado excel con todos los libros de varias fuentes de bibliotecas electrónicas. Una vez descomprimido el zip, puede ver el listado de libros en excel y proceder a localizar los libros y hacer peticiones enviando un email a ebookonmail@gmail.com y especificando en el asunto el código del libro que desea solicitar.",'',zipfile)	
						logger.warning(varFrom+'|'+vaction+'| - |'+zipfile+'| - |'+vcalibrebiblio)									
						
				
				if vaction == 'ayuda':
					vhelp = open('help.txt').read()
					volext=0
					if not vtoemail.strip()=='':
						varFrom=vtoemail.lower().strip()
					mailresponse(varFrom,'Re: EbookOnMail Información/Ayuda',vhelp,'','')					
					
				if vaction == 'convert' and vattachment != '':
					if not vtoemail==None and not vtoemail=='':
						varFrom=vtoemail.lower().strip()

					if vformat=='' or vformat==None:
						vformat='RTF'
					vformat = vformat.lower().strip()

					if "kindle.com" in varFrom.lower():
						vformat='mobi'		
					
					ebookfile = vattachment
					ebookfileout = ''
					
					ebookfileout=convertebook(vattachment,vformatin,vformat)
					if os.path.isfile(ebookfileout):
						if "kindle." in varFrom:
							vrespsubject='convert'
						else:
							vrespsubject='Re: '+ebookfileout
						mailresponse(varFrom,vrespsubject,"""Conversion sucessful! Open the attachment...""",'',ebookfileout)						
						os.remove(ebookfileout)
				
				
				if vaction == 'sendebook' and vebooknum != '':
					if not vtoemail==None and not vtoemail=='':
						varFrom=vtoemail.lower().strip()

					if vformat=='' or vformat==None:
						vformat='RTF'
					if vcalibrebiblio==None:
						vcalibrebiblio=''
					vformat = vformat.lower().strip()
					vgetline="GET"+vformat.upper()+" "+vcalibrebiblio+vebooknum

					if vcalibrebiblio=='' or vcalibrebiblio==None:
						vcalibrebiblio=''
					if "kindle.com" in varFrom.lower():
						vformat='mobi'		
					
					ebookfile = ''
					vformatin = ''
					ebookfileout = ''
					ebookpath = ''
					ebookauth = ''
					ebooktitle = ''
					ebookyear = '' #, ebookauth, ebooktitle, ebookyear

					#Buscar ruta de libro en biblioteca calibre...	
					for src in vsrc:
						vdblocalroot=vcalibresrc[src+'path']
						vdblocalroot=vdblocalroot.replace(vcalibreabssrc,'')	
					
						print "Biblio "+src+": "+vcalibresrc[src+'path']
						print "Comparando1: ",vcalibrebiblio.upper(),"==",vcalibresrc[src+'code'].upper()
						if vcalibrebiblio.upper()==vcalibresrc[src+'code'].upper():
							if vcalibresrc[src+'code']=='KHA':
								vebooknum=vebooknum.zfill(8)
								print "Cambiado la ref. del libro (KHA) a: ",vebooknum	
				
							vebooknum=vebooknum.replace("\r","").replace("\n","")
							print "Comparando2: ",vcalibresrc[src+'type'],"==identifiers|custom"
							if vcalibresrc[src+'type']=='identifiers':						
								ebookpath, ebookauth, ebooktitle, ebookyear=getebookpath_fromidentifiers(vcalibresrc[vbiblio+'preidval']+vebooknum+vcalibresrc[src+'postidval'],vcalibresrc[src+'id'],vdblocalroot,vcalibresrc[src+'path'])
							if vcalibresrc[src+'type']=='custom' or vcalibresrc[src+'type']=='customfield':
								ebookpath, ebookauth, ebooktitle, ebookyear=getebookpath_fromcustom(vcalibresrc[vbiblio+'preidval']+vebooknum+vcalibresrc[src+'postidval'],vcalibresrc[src+'id'],vdblocalroot,vcalibresrc[src+'path'])

					#Buscar libro en algUn formato...				
					if not ebookpath=='':
						if vformat == 'fb2' and ".cu>" in varFrom :
							vformat = 'rtf'
				
						import random
						import string
						vfilerandomname = "".join( [random.choice(string.letters) for i in xrange(15)] )
							
						vdblocalroot=vcalibresrc[src+'path']
						vdblocalroot=vdblocalroot.replace(vcalibreabssrc,'')
						os.system('mkdir -p temp')
						os.system('rm -r temp/*')
						os.system('mkdir -p "temp/'+vfilerandomname+'"')
						
						if True:
							import ftplib

							HOST = 'ftp-hostname'
							DIRN = ebookpath.strip().replace('/media/guessname','') #.replace(vcalibreabssrc,'')

							print "Descargando archivos por FTP de: ",DIRN
							ftp = ftplib.FTP(HOST)
							ftp.login("guess","guesspass")
							ftp.cwd(DIRN)
							
							filelist=ftp.nlst()

							for file in filelist:
								if (not ".opf" in file) and (not ".jpg" in file) and (not file in [".",".."] ):
									try:
										vdest=os.path.join('temp/'+vfilerandomname,file)
										ftp.retrbinary('RETR %s' % file, open(vdest,"wb").write )
										ebookpath="temp/"+vfilerandomname
										print "Descargado (ftp): "+ebookpath+"/"+file
									except:
										pass				
								# f.retrlines('LIST')							
								# f.retrbinary('RETR %s' % IMG, open(IMG, 'wb').write)									
								# f.retrbinary('RETR %s' % FILE, 

							ftp.quit()						
						
						
						# print 'wget "'+vservercalibre+ebookpath.replace(vcalibreabssrc,'')+'" -O "temp/'+vfilerandomname+'/*"'
						# os.system('wget "'+vservercalibre+ebookpath.replace(vcalibreabssrc,'')+'" -O "temp/'+vfilerandomname+'/"')						
											
						ebooks_files = [f for f in os.listdir(ebookpath) if f.endswith('.'+vformat)]
						if len(ebooks_files)>0:
							ebookfile = ebookpath+'/'+ebooks_files[0]
							vformatin = vformat
							vebookfileinfo = ebooks_files[0]

						for vf in vebookformats:
							if ebookfile=='':
								print 'Buscando '+vf+'... '+ebookfile
								ebooks_files = [f for f in os.listdir(ebookpath) if f.endswith('.'+vf)]
								if len(ebooks_files)>0:
									ebookfile = ebookpath+'/'+ebooks_files[0]
									vebookfileinfo = ebooks_files[0]
									vformatin = vf	
					else:
						#mailresponse(varFrom,'EbookOnMail '+vebooknum+' no encontrado.','La referencia con nUmero '+vebooknum+" no se ha encontrado. En general esto se debe a que hay una actualizaciOn o versiOn nueva del libro deseado. Ha solicitado acceso a las nuevas recopilaciones?",'','')
						print "Error: "+varFrom+'|'+vaction+'|'+vgetline+' to '+varFrom+'|'+loczip+'|'+str(vsize)+'k|EbookOnMail '+vebooknum+' no encontrado.'
						logger.error(varFrom+'|'+vaction+'|'+vgetline+' to '+varFrom+'|'+loczip+'|'+str(vsize)+'k|EbookOnMail '+vebooknum+' no encontrado.')	

					print ebookfile
					vconvertprogram='calibre'
					if ebookfile=='':
						print varFrom+'|'+vaction+'|'+vformat+'|'+vebooknum+'| No se encuentra la ruta del ebook...'
					else:
						#Realizar conversiOn a archivo solicitado!
						ebookfileout=convertebook(ebookfile,vformatin,vformat)

						#Comprimir archivo...
						loczip = ''
						vsize = 0
						if os.path.isfile(ebookfileout):
							vsize=int(os.path.getsize(ebookfileout)/1000)
							print u'TamaNo de '+ebookfileout+': ',vsize,"kbytes"
							#os.system('7z a "'+loczip+'" "'+locfile+'" -v900k')
							if "kindle.com" in varFrom.lower():
								loczip=ebookfileout
								#loczip = createzip(ebookfileout, vebooknum + ".zip" ,'','')
							else:
								loczip = createzip(ebookfileout, vebooknum + ".zip" ,'','900k')
								vsize=int(os.path.getsize(loczip)/1000)
								print u'TamaNo de '+loczip+': ',vsize,"kbytes"
								os.remove(ebookfileout)
		
				
						if loczip=='' or vsize==0:
							mailresponse(varFrom,'EbookOnMail '+vebooknum,"""Siento mucho las molestias pero por alguna irregularidad interna (quizAs de conversiOn de formato o problema de espacio) no se ha podido generar y enviar el ebook. Pronto se analizarA la incidencia...""",'','')		
							logger.error(varFrom+'|'+vaction+'|'+vgetline+'|'+loczip+'|'+str(vsize)+'k|Error generando el zip...')		
							print "Error: "+varFrom+'|'+vaction+'|'+vgetline+'|'+loczip+'|'+str(vsize)+'k|Error generando el zip...'
						else:
							#Enviar adjunto el loczip
							if os.path.isfile(vebooknum + ".z01"):
								vlastvolext=''
								for volext in ['01','02','03','04','05','06','07','08','09']:
									if os.path.isfile(vebooknum + ".z"+ volext):
										vlastvolext=volext
								mailresponse(varFrom,'Re: EbookOnMail zip 01/0'+str(int(vlastvolext)+1)+' '+vgetline,"El adjunto contenido en este archivo es la 01 parte de 0"+str(int(vlastvolext)+1)+" partes. Proceda primeramente a descargar cada adjunto en una misma carpeta y a continuación tras completar la descarga de todas las partes intente descomprimir el zip para que funcione correctamente... Si no coincide el libro enviado con el deseado, por favor, infórmelo por esta vía...",'',vebooknum + ".zip")	
								os.remove(vebooknum + ".zip")
								for volext in ['01','02','03','04','05','06','07','08','09']:
									if os.path.isfile(vebooknum + ".z"+ volext):
										mailresponse(varFrom,'Re: EbookOnMail zip 0'+str(int(volext)+1)+'/0'+str(int(vlastvolext)+1)+' '+vgetline,"El adjunto contenido en este archivo es la "+str(int(volext)+1)+" parte de "+str(int(vlastvolext)+1)+" partes. Proceda primeramente a descargar cada adjunto en una misma carpeta y a continuación tras completar la descarga de todas las partes intente descomprimir el zip para que funcione correctamente... Si no coincide el libro enviado con el deseado, por favor, infórmelo por esta vía...",'',vebooknum + ".z"+ volext)	
										os.remove(vebooknum + ".z"+ volext)
								logger.warning(varFrom+'|'+vaction+'|'+vlastvolext+' partes: '+vgetline+'|'+loczip+'|'+str(vsize)+'k|'+vconvertprogram+' '+vebookfileinfo)			
							else:
								if "kindle.com" in varFrom.lower():
									send_mail(varFrom,loczip,loczip,'',loczip)
								else:
									mailresponse(varFrom,'Re: EbookOnMail '+vgetline,"""Abra el adjunto... Si no coincide el libro enviado con el deseado, por favor, infOrmelo por esta vIa...""",'',loczip)	
								logger.warning(varFrom+'|'+vaction+'|'+vgetline+'|'+loczip+'|'+str(vsize)+'k|'+vconvertprogram+' '+vebookfileinfo)			
								#Eliminar zip (trazas)
								if os.path.isfile(loczip):
									os.remove(loczip)
									
				if vaction == 'repeated':
					logger.error(varFrom+'|'+varSubject+'|PeticiOn repetida> no se procede...')
				if vaction == '':
					logger.warning(varFrom+'|'+varSubject+'|No action...')
					mailresponse(varFrom,'RE: '+varSubject,'No se ha especificado ninguna action a ejectuar. Recuerde especificar el formato deseado (RTF, PDF, MOBI, EPUB) junto con el número del libro en el asunto o cuerpo del email, ejemplo: GETRTF 25540','','')
	
		mail.store(num, '+FLAGS', r'\Deleted')

	 
	mail.expunge()
	mail.close()
	mail.logout()

	now = datetime.datetime.now()
	flog = open('lastrun.log','w')
	flog.write(str(now))
	flog.close()
	print str(now)

vnewsletter=False
vgenlist=False
vgentable=False
vcheckebooks=False
vgencalibrelist=False
print ''
print 'python ebookonmail.py -genlist -gentable -de'
print 'python ebookonmail.py -newsletter'
print 'python ebookonmail.py -genlist -checkebooks -gentable'
print 'python ebookonmail.py -sendnew [SEL|GTB|FBS]'
print 'python ebookonmail.py -sendfulllist'
print 'python ebookonmail.py -sendnewlist'
print 'python ebookonmail.py -resendfromerrors'
print 'python ebookonmail.py -sendebooklist <mail@destino>'
print 'python ebookonmail.py -gencalibrelist'
print ''
if len(sys.argv)>=1:
	argv=sys.argv[1:]
	vapos=0
	#print str(argv)
	for arg in argv:
		vapos=vapos+1
		if arg=='-genlist':
			vgenlist = True
		if arg=='-gencalibrelist':
			vgencalibrelist=True
		if arg=='-checkebooks':
			vcheckebooks = True
		if arg=='-gentable':
			vgentable = True			
		if arg=='-resendfromerrors':
			vemaillist = file('pendiente.error.txt')	
			for veemail in vemaillist:
				m = re.search("(.*) TO (.*)",veemail.upper().strip())
				if m:
					vcodeebook = m.groups()[0]
					vtoemail = m.groups()[1]
					print "Reenviar libro: ",vcodeebook," a ",vtoemail.lower()
					try:
						mailresponse(vebookonmail_email,veemail,'','','')
					except:
						pass
		if arg=='-sendebooklist':
			vtoemail=argv[vapos]
			print "Envío de ebooks a: ",vtoemail
			vebookslist = file('selection.txt')	
			for vebooks in vebookslist:
				vebooksplit=vebooks.split(",")
				for vcodeebook in vebooksplit:
					print "Enviando ebook: "+vcodeebook+" a "+vtoemail
					try:
						mailresponse(vebookonmail_email,vcodeebook+' to '+vtoemail,'','','')
					except:
						pass
			
		if arg=='-newsletter':
			vemaillist = file('emaillist.txt')	
			vnewslettertext = open('newsletter.txt').read()
			print vnewslettertext
			for vTO in vemaillist:
				volext=0
				if not vTO.strip()=="":		
					print "Envío de newsletter para :",vTO
					now = datetime.datetime.now()
					vmonth=("0"+str(now.month)) if now.month<10 else str(now.month)
					
					mailresponse(vTO,'Re: EbookOnMail Información/Ayuda',vnewslettertext,'','')	
					
					for zipfile in glob.glob("toshare/"+vebookonmaillist+"*.zip"):
						volext=volext+1		
						print "Enviando..."+zipfile						
						mailresponse(vTO,'Re: EbookOnMail Todo List ('+str(int(volext))+") "+vmonth+"/"+str(now.year),"El adjunto contiene un listado excel con todos los libros de varias fuentes de bibliotecas electrónicas. Una vez descomprimido el zip, puede ver el listado de libros en excel y proceder a localizar los libros y hacer peticiones enviando un email a ebookonmail@gmail.com y especificando en el asunto el código del libro que desea solicitar.",'',zipfile)	
						logger.warning(vTO+'|newsletter| - |'+zipfile+'| - |')

					for zipfile in glob.glob("toshare/novedades*.zip"):
						volext=volext+1		
						print "Enviando..."+zipfile						
						mailresponse(vTO,'Re: EbookOnMail Novedades '+vmonth+"/"+str(now.year),"El adjunto contiene un listado excel con las novedades de libros de varias fuentes de bibliotecas electrónicas. Una vez descomprimido el zip, puede ver el listado de libros en excel y proceder a localizar los libros y hacer peticiones enviando un email a ebookonmail@gmail.com y especificando en el asunto el código del libro que desea solicitar.",'',zipfile)	
						logger.warning(vTO+'|newsletter| - |'+zipfile+'| - |')								

if vgenlist:
	vdballebooks = sqlite3.connect(vresumDB)
	c = vdballebooks.cursor()
	sqlall = 'create table if not exists books(id INTEGER PRIMARY KEY, code varchar(20), source varchar(10), author varchar(50), title varchar(100), year varchar(4), lang varchar(10), dirpath varchar(150), orderauth varchar(50), ordertitle varchar(50), soundauth varchar(50), soundtitle varchar(100), mark varchar(10), new varchar(1), serie varchar(50), comments TEXT, notasimages varchar(15), premios varchar(100), size varchar(10));'
	print sqlall
	c.execute(sqlall)
	
	sqlall = 'create table if not exists data(id INTEGER PRIMARY KEY, code varchar(20), source varchar(10), format varchar(5), size varchar(6), path TEXT);'
	print sqlall
	c.execute(sqlall)

	sqlall = 'CREATE INDEX if not exists books_code_idx ON books(code);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists books_author1_idx ON books(author);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists books_soundauth_idx ON books(soundauth);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists books_soundtitle_idx ON books(soundtitle);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists books_orderauth_idx ON books(orderauth);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists books_ordertitle_idx ON books(ordertitle);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists books_year_idx ON books(year);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists data_code_idx ON data(code);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists data_format_idx ON data(format);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists data_idx ON data(code,format);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists books_source ON books(source);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists data_source ON data(source);'
	print sqlall
	c.execute(sqlall)
	
	sqlall = 'create table if not exists booksresum(id INTEGER PRIMARY KEY, codes varchar(100), author varchar(50), title varchar(50), year varchar(4), size varchar(6), lang varchar(10), new varchar(1), codesrich TEXT, notes TEXT, orderauth varchar(50), serie varchar(50), comments TEXT, notasimages varchar(15), premios varchar(100));'
	#Nuevo o cambio: codes (todos los códigos del libro), notes (notas)...
	print sqlall
	c.execute(sqlall)	
	sqlall = 'CREATE INDEX if not exists booksresum_codes_idx ON booksresum(codes);'
	print sqlall
	c.execute(sqlall)	
	sqlall = 'CREATE INDEX if not exists booksresum_author_idx ON booksresum(author);'
	print sqlall	
	c.execute(sqlall)	
	sqlall = 'CREATE INDEX if not exists booksresum_year_idx ON booksresum(year);'
	print sqlall	
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists booksresum_orderauth_idx ON booksresum(orderauth);'
	print sqlall
	c.execute(sqlall)		
	
	fsss = open('calibre-premios.txt','w')
	fsss.close()	

	c.close()
	vdballebooks.close()
	
	for src in vsrc:
		print "Biblio "+src+": "+vcalibresrc[src+'path']
		print "Copiando base de datos a local: "+src
		vdblocalroot=vcalibresrc[src+'path']
		vdblocalroot=vdblocalroot.replace(vcalibreabssrc,'')
		os.system('mkdir -p "'+vdblocalroot+'"')
		# os.system('cp "'+vcalibresrc[src+'path']+'/metadata.db" "'+vdblocalroot+'"')
		vpathftp=vcalibresrc[src+'path']
		vpathftp=vpathftp.replace("/media/users","")  
		print 'wget '+vservercalibre+vdblocalroot+'/metadata.db -O "'+vdblocalroot+'/metadata.db"' 
		os.system('wget '+vservercalibre+vdblocalroot+'/metadata.db -O "'+vdblocalroot+'/metadata.db"' )

	for src in vsrc:
		if src in vsrcinlist:
			print "Biblio "+src+": "+vcalibresrc[src+'path']
			vdblocalroot=vcalibresrc[src+'path']
			vdblocalroot=vdblocalroot.replace(vcalibreabssrc,'')
			GenList(vcalibresrc[src+'type'],vcalibresrc[src+'id'], vdblocalroot, vcalibresrc[src+'code'], vcalibresrc[src+'format'], vcheckebooks, vcalibresrc[src+'lastupdateid'],src,vnewinlastmonths)

	#Inyectar SQL de premios
	vdballebooks = sqlite3.connect(vresumDB)
	c = vdballebooks.cursor()

#insert into obrapremium values("KHA00002240","Finalista Minotauro","Vaquerizo, Eduardo","Danza De Tinieblas")
#insert into authpremium values("Cela, Camilo José","Cervantes")

	sqlall = 'create table if not exists obrapremium(code varchar(20), premio varchar(100), author varchar(50), title varchar(50))'
	print sqlall
	c.execute(sqlall)

	sqlall = 'create table if not exists authpremium(author varchar(50), premio varchar(100));'
	print sqlall
	c.execute(sqlall)

	sqlall = 'CREATE INDEX if not exists obrapremium_code_idx ON obrapremium(code);'
	print sqlall
	c.execute(sqlall)
	sqlall = 'CREATE INDEX if not exists authpremium_author_idx ON authpremium(author);'
	print sqlall
	c.execute(sqlall)


	sqlall = 'delete from obrapremium'
	print sqlall	
	c.execute(sqlall)	
	
	sqlall = 'delete from authpremium'
	print sqlall	
	c.execute(sqlall)	

	vlines = file('premios.sql')	
	for vline in vlines:
		if not vline.strip()=="":
			print vline
			c.execute(vline)
	vdballebooks.commit()
	
	
	# #Actualizar algunos datos...
	# vlines = file('replace.txt')						
	# vtype=""
	# for gline in vlines:
		# if gline[:1]==":":
			# vtype=gline
		# if ">" in gline:
			# if vtype==":Author":
				# gline=gline.split(">")
				# if len(gline)>1:	
					# c.execute("UPDATE books SET author='"+(gline[1].strip())+"' WHERE author='"+(gline[0].strip())+"'")
					# vdballebooks.commit()	
			
	c.close()
	vdballebooks.close()
	
	vcond="" #where books.soundauth, books.soundtitle		
			 #where books.title like "%á%"	

	
	fupdate = open('update.sql','w')
	


	import xlwt
	#stylered = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
	#styleblue = xlwt.easyxf('font: name Times New Roman, colour blue')
	#styleyellow = xlwt.easyxf('font: name Times New Roman, colour yellow')
	#stylegreen = xlwt.easyxf('font: name Times New Roman, colour green')

	alignment = xlwt.Alignment() # Create Alignment
	alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
	alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED


	stylenormal = xlwt.easyxf('font: colour black')
	stylenormal.alignment = alignment # Add Alignment to Style

	pattern1 = xlwt.Pattern() # Create the Pattern
	pattern1.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern1.pattern_fore_colour = 7 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	styleblue = xlwt.XFStyle() # Create the Pattern
	styleblue = xlwt.easyxf('font: colour black')
	styleblue.pattern = pattern1 # Add Pattern to Style
	styleblue.alignment = alignment # Add Alignment to Style

	pattern2 = xlwt.Pattern() # Create the Pattern
	pattern2.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern2.pattern_fore_colour = 2 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	stylered = xlwt.XFStyle() # Create the Pattern
	stylered = xlwt.easyxf('font: colour black')
	stylered.pattern = pattern2 # Add Pattern to Style
	stylered.alignment = alignment # Add Alignment to Style

	pattern3 = xlwt.Pattern() # Create the Pattern
	pattern3.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern3.pattern_fore_colour = 5 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	styleyellow = xlwt.XFStyle() # Create the Pattern
	styleyellow = xlwt.easyxf('font: colour black')
	styleyellow.pattern = pattern3 # Add Pattern to Style
	styleyellow.alignment = alignment # Add Alignment to Style

	pattern4 = xlwt.Pattern() # Create the Pattern
	pattern4.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern4.pattern_fore_colour = 3 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	stylegreen = xlwt.XFStyle() # Create the Pattern
	stylegreen = xlwt.easyxf('font: colour black')
	stylegreen.pattern = pattern4 # Add Pattern to Style
	stylegreen.alignment = alignment # Add Alignment to Style

	wb = xlwt.Workbook()
	ws = wb.add_sheet('Libros',cell_overwrite_ok=True)
	ws.write(1, 0, 'Autor', stylered)
	ws.write(1, 1, 'Título', stylered)
	ws.write(1, 2, 'Año', stylered)
	ws.write(1, 3, 'Tamaño', stylered)
	ws.write(1, 4, 'Referencia', stylered)
	ws.write(1, 5, 'Pedir por email', stylered)
	ws.write(1, 6, 'Notas/Premios', stylered)
	vstylenote=stylenormal
	
	vdb = sqlite3.connect(vresumDB)
	# vdb.text_factory = lambda x: utf8_str(x, "utf-8", "ignore")
	# vdb.text_factory = str
	
	
	vbgcolor= ' bgcolor="#A2B0F9" '
	ebno=0
	vlastauthor=""
	vlastcode=""
	vlasttitle=""
	vlastsoundtitle=""
	vbook=""
	vcodes=""
	vnumbooks=0	
	vauthorS=""
	vtitleS=""
	vyearS=""
	vsizeS=""
	vcodeS=""
	vcoderichs=""
	vauthororderS=""
	vnewbookS="0"
	vlastnote=""
	vorderauthS=""
	vnote=""
	vserieS=""
	vcommentS=""
	vnotasimagesS=""	
	
	vsqlresume="""
		select 	books.source, books.code, books.author, books.title, books.year, books.lang, books.dirpath, books.mark,
			data.format, (data.size/1000), data.path,
			books.premios,
			"",
			books.soundauth, books.soundtitle, books.ordertitle, books.new, books.orderauth, books.serie, '', books.notasimages, books.size
			
		from books 
				left join data on books.code==data.code

		"""+vcond+"""  
		order by books.orderauth asc, books.ordertitle asc"""  #books.comments	
	
	
	# """
		# select 	books.source, books.code, books.author, books.title, books.year, books.lang, books.dirpath, books.mark,
			# data.format, (data.size/1000), data.path,
			# obrapremium.premio,
			# authpremium.premio,
			# books.soundauth, books.soundtitle, books.ordertitle, books.new, books.orderauth, books.serie, '', books.notasimages
			
		# from books 
				# left join data on books.code==data.code
				# left join obrapremium on books.code=obrapremium.code
				# left join authpremium on books.author=authpremium.author
				
		# """+vcond+"""  
		# order by books.orderauth asc, books.ordertitle asc"""  #books.comments	
	
	vdb.text_factory = str
	vcantebooks=1
	iSQLPosInit=0
	iSQLPosCount=30000
	
	# while vcantebooks>0:
	if vcantebooks>0:
	
		# cur = vdb.execute(vsqlresume +" LIMIT " + str(iSQLPosInit) + ", " + str(iSQLPosCount))
		cur = vdb.execute(vsqlresume)
		rows = cur.fetchall()
		vcantebooks=len(rows)
		print "SQL: ",vsqlresume +" LIMIT " + str(iSQLPosInit) + ", " + str(iSQLPosCount)
		print "Cantidad de ebooks ",vcantebooks 
		
		iSQLPosInit=iSQLPosInit+iSQLPosCount+1
		
		if vcantebooks>0:
		
		  vpremiosauthintags=""
		  vpremiosbookintags=""
		  goldfile = file('premios.txt')									
		  for gline in goldfile:
			  vline=( gline.strip() )  #utf8_str

			  if len(vline)>0:

				if vline[:1]==">" and (vline[1:] not in vpremiosauthintags):
					vgoldvalue=vline[1:]
					vgoldvalue=vgoldvalue.strip()
					vgoldtype="auth"
					vpremiosauthintags=vpremiosauthintags+","+vgoldvalue+"," #.append(vgoldvalue)
				else: 
					if vline[:1]=="#" and (vline[1:] not in vpremiosbookintags):
						vgoldvalue=vline[1:]
						vgoldvalue=vgoldvalue.strip()
						vgoldtype="book"
						vpremiosbookintags=vpremiosbookintags+","+vgoldvalue+"," #.append(vgoldvalue)
						
		  for ebook in rows:
			
			ebno=ebno+1
			vsource=ebook[0]
			vcode=ebook[1]
			vauthor=ebook[2]
			vtitle=ebook[3]
			vyear=ebook[4]
			vlang=ebook[5] 
			vdirpath=ebook[6]
			vmark=ebook[7]
			vformat=ebook[8]
			vsize=str(ebook[9])
			vepath=(ebook[10]) if not ebook[10]==None else ""
			vpremios=(ebook[11]) if not ebook[11]==None else ""
			# vobrapremium=(ebook[11]) if not ebook[11]==None else ""
			# vauthpremium=(ebook[12]) if not ebook[12]==None else ""
			vsoundauth=ebook[13]
			vsoundtitle=ebook[14]
			# vnewbookS=str(ebook[16])
			vorderauth=ebook[17]	
			vserie=ebook[18]	
			vcomment=ebook[19]
			vnotasimages=ebook[20]
			vsize=str(ebook[21])
			
			vobrapremium=""
			vauthpremium=""
			
			
			if vauthorS=="":
				vauthorS=ebook[2]
				vtitleS=ebook[3]
				vyearS=ebook[4]
				vsizeS=str(ebook[9])
				vsizeS=str(ebook[21])
				vcodeS=ebook[1]	
				vauthororderS=ebook[15]		
				vnewbookS=str(ebook[16])	
				vcoderichs=''
			
			vnotestyle=""
			vlastnote=vnote
			vnote=""
			vstylenote=stylenormal	
				
			for vvvp in vpremios.split(","):
				vvvp=vvvp.strip()
				if ","+vvvp.lower()+"," in vpremiosauthintags.lower() and (vvvp not in vauthpremium) and (vvvp not in vobrapremium):
					vauthpremium=(vvvp) if vauthpremium=="" else vauthpremium+", "+vvvp 
				if ","+vvvp.lower()+"," in vpremiosbookintags.lower() and (vvvp not in vobrapremium) and (vvvp not in vauthpremium):
					vobrapremium=(vvvp) if vobrapremium=="" else vobrapremium+", "+vvvp 
			
			if not vobrapremium=="":  
				vnote=(vobrapremium) if vnote=="" else vnote+","+vobrapremium
				vnotestyle=' align=center bgcolor="green"'
				vstylenote=stylegreen		
			if not vauthpremium=="":
				vnote=(vauthpremium) if vnote=="" else vnote+","+vauthpremium 
				vnotestyle=' align=center bgcolor="yellow"'
				vstylenote=styleyellow		
				
			#vnote=vnote.encode('ascii', 'xmlcharrefreplace')
			
			vnewbook=False
			if not vlastauthor==vsoundauth and not soundexstr(vlastauthor) in soundexstr(vsoundauth) and not soundexstr(vsoundauth) in soundexstr(vlastauthor):  #.encode('ascii', 'ignore')
				vbgcolor= ' bgcolor="#A2B0F9" '
				vlastauthor=vsoundauth
				vauthor='<td align=center >'+ebook[2]+'</td>'	#.encode('ascii', 'xmlcharrefreplace')
				vnewbook=True
				try:
					fupdate.write('\n\n'+'#Author: '+ebook[2])
				except:
					fupdate.write('\n\n'+'#Author: '+ebook[2].encode('ascii', 'ignore'))
				
			else:
				vauthor="<td></td>"
				vbgcolor= ''
			
			if not vlastsoundtitle==vsoundtitle:
				try:
					vtitle1=vtitle.lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú","")
					vlasttitle1=vlasttitle.lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú","")
				except:
					vtitle1=vtitle.encode('ascii', 'ignore').lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú","")
					vlasttitle1=vlasttitle.encode('ascii', 'ignore').lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú","")

				if vtitle1==vlasttitle1:
					# or vtitle.encode('ascii', 'ignore').lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú","") in vlasttitle.encode('ascii', 'ignore').lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú","") \
					# or vlasttitle.encode('ascii', 'ignore').lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú","") in vtitle.encode('ascii', 'ignore').lower().replace("á","").replace("é","").replace("í","").replace("ó","").replace("ú",""):
					# or vlastsoundtitle.encode('ascii', 'ignore') in vsoundtitle.encode('ascii', 'ignore') \
					# or vsoundtitle.encode('ascii', 'ignore') in vlasttitle.encode('ascii', 'ignore'):
					if len(vtitle)>len(vlasttitle):
						try:
							vbook='<tr bgcolor="#A2B0F9"><td align=center >'+ebook[2]+'</td><td align=left >'+vtitle+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'</td><td align=center >'+vnotasimages+'</td><td align=center >vcodeshere</td><td align=center ><a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vcode+'">Pedir</a></td><td'+vnotestyle+'>'+vnote+'</td></tr>'
						except:	
							vbook='<tr bgcolor="#A2B0F9"><td align=center >'+ebook[2].encode('ascii', 'xmlcharrefreplace')+'</td><td align=left >'+vtitle.encode('ascii', 'xmlcharrefreplace')+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'</td><td align=center >'+vnotasimages+'</td><td align=center >vcodeshere</td><td align=center ><a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vcode+'">Pedir</a></td><td'+vnotestyle+'>'+vnote.encode('ascii', 'xmlcharrefreplace')+'</td></tr>'	
						
							
						# vauthorS=ebook[2]
						vtitleS=ebook[3]
						# vyearS=ebook[4]
						# vsizeS=str(ebook[9])
						# vcodeS=ebook[1]		
						# vauthororderS=ebook[15]						
				else:
					vnewbook=True
					vlastsoundtitle=vsoundtitle
					vlasttitle=vtitle
				
			if vnewbook:
				vnumbooks=vnumbooks+1
				vlastbook=vbook
				try:
					vbook='<tr'+vbgcolor+'>'+vauthor+'<td align=left >'+vtitle+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'</td><td align=center >'+vnotasimages+'</td><td align=center >vcodeshere</td><td align=center ><a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vcode+'">Pedir</a></td><td'+vnotestyle+'>'+vnote+'</td></tr>'
				except:	
					vbook='<tr'+vbgcolor+'>'+vauthor+'<td align=left >'+vtitle.encode('ascii', 'xmlcharrefreplace')+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'</td><td align=center >'+vnotasimages+'</td><td align=center >vcodeshere</td><td align=center ><a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vcode+'">Pedir</a></td><td'+vnotestyle+'>'+vnote.encode('ascii', 'xmlcharrefreplace')+'</td></tr>'
				
					
				#fwrite.write(vlastbook.replace("vcodeshere",vcodes.encode('ascii', 'xmlcharrefreplace')))

				print str(ebno)+"/"+str(iSQLPosInit+iSQLPosCount),ebook[0], ebook[1], ebook[2], ebook[3], ebook[4]  #, ebook[6], ebook[7], ebook[8], ebook[9], ebook[10], ebook[11]		
				if not vcodes=="":
					try:
						fupdate.write('\n'+'insert into booksresum values(null, "'+vcodes+'", "'+vauthorS.replace('"',' ')+'", "'+vtitleS.replace('"',' ')+'", "'+vyearS+'", "'+vsizeS+'", "'+vlang+'", "'+vnewbookS+'", "'+vcoderichs.replace('\\"','""')+'", "'+vlastnote.replace('"',' ')+'", "'+vorderauthS.replace('"',' ')+'","'+vserieS+'","'+vcommentS.replace('"',' ')+'", "'+vnotasimagesS+'", "'+vnote+'");')	
					except:
						fupdate.write('\n'+'insert into booksresum values(null, "'+vcodes+'", "'+vauthorS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vtitleS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vyearS+'", "'+vsizeS+'", "'+vlang+'", "'+vnewbookS+'", "'+vcoderichs.encode('ascii', 'xmlcharrefreplace').replace('\\"','""')+'", "'+vlastnote.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vorderauthS.encode('ascii', 'ignore').replace('"',' ')+'","'+vserieS.encode('ascii', 'ignore')+'","'+vcommentS.encode('ascii', 'ignore').replace('"',' ')+'", "'+vnotasimagesS+'","'+vnote.encode('ascii', 'ignore').replace('"',' ')+'");')				

				vstyle=stylenormal
				if not vbgcolor=="":
					vstyle=styleblue
					if vstylenote==stylenormal:
						vstylenote=styleblue
				ws.write(vnumbooks, 0, vauthorS, vstyle)
				ws.write(vnumbooks, 1, vtitleS, vstyle)
				ws.write(vnumbooks, 2, vyearS, vstyle)
				ws.write(vnumbooks, 3, vsizeS, vstyle)
				ws.write(vnumbooks, 4, vcodes, vstyle)
				ws.write(vnumbooks, 5, xlwt.Formula('HYPERLINK("mailto:'+vebookonmail_email+'?subject=GETRTF '+vcodeS+'";"Pedir")'), vstyle)
				ws.write(vnumbooks, 6, vnote, vstylenote)


				vauthorS=ebook[2]
				vtitleS=ebook[3]
				vyearS=ebook[4]
				#vsizeS=str(ebook[9])+'k' if (not ebook[9]==None) else ""
				vsizeS=str(ebook[9]) if (not ebook[9]==None) else ""
				vsizeS=str(ebook[21]) if (not ebook[21]==None) else ""
				vcodeS=ebook[1]		
				vauthororderS=ebook[15]
				vnewbookS=str(ebook[16])
				vcoderichs=''
				vorderauthS=vorderauth
				vserieS=vserie
				vcommentS=vcomment
				vnotasimagesS=ebook[20]	
						
				vstylenote=stylenormal
				vcodes=""
				

			while "KHA0" in vcode:
				vcode=vcode.replace("KHA0","KHA")
				
			# if not vnewbook and vnewbookS=='1' and ebook[16]=='0':
				# vnewbookS='0'
				
			vedpath=""
			if not vcode==vlastcode:
				vlastcode=vcode
				vcoderich=''
				if vHTMLDetails:
					vfounded=False
					for src in vsrc:
						if vcalibresrc[src+'code'] in vcode and not vcalibresrc[src+'urlid']=="":
							vid=vcode.replace(vcalibresrc[src+'code'],"")
							vid=str(int(vid.replace(".0","")))

							vedpath=vdirpath.replace("'","&apos;")
							vedpath=vdirpath.replace('"',"&quot;")
							
							vurl="<a href='javascript:"+vcalibresrc[src+'code']+'(\\"'+vid+'\\")'+"'>w</a><a href='javascript:vd("+'\\"'+vcode+'\\",\\"'+vedpath+'\\")'+"'>d</a><a href='javascript:smail("+'\\"'+vcode+'\\",\\"\\"'+')'+"'>@</a>"
				
							vcoderich="<a href='javascript:dl("+'\\"'+vedpath+'\\"'+")'>"+vcode+"</a><sup>"+vurl+"</sup>"
							vfounded=True
					if not vfounded:

						vedpath=vdirpath.replace("'","''")
						vcoderich="<a href='javascript:dl("+'\\"'+vedpath+'\\"'+")'>"+vcode+"</a><sup><a href='javascript:vd("+'\\"'+vcode+'\\",\\"'+vedpath+'\\"'+")'>d</a><a href='javascript:smail("+'\\"'+vcode+'\\",\\"\\"'+')'+"'>@</a></sup>"	
					 
	

				vcodes=(vcode) if vcodes=="" else vcodes+","+vcode
				vcoderichs=(vcoderich) if vcoderichs=="" else vcoderichs+", "+vcoderich
				
				print "   ",vauthorS," - ", vauthororderS," - ", ebook[1]," ("+vedpath+")"
				#				fupdate.write('\n'+'insert into booksresum values(null, "'+vcodes+'", "'+vauthorS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vtitleS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vyearS+'", "'+vlang+'", "'+vnewbookS+'", "'+vcoderichs.encode('ascii', 'xmlcharrefreplace').replace('"','')+'", "'+vlastnote.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vorderauthS.encode('ascii', 'ignore').replace('"',' ')+'");')	

				try:
					fupdate.write('\n'+'#'+ebook[2])
				except:
					fupdate.write('\n'+'#'+ebook[2].encode('ascii', 'ignore'))				
				
				
				#print ebook[0], ebook[1], ebook[2], ebook[3], ebook[4], ebook[5], ebook[6], ebook[7], ebook[8], ebook[9], ebook[10], ebook[11]

			
		if not vlasttitle==vsoundtitle:	
			
			#vbook='<tr bgcolor="#A2B0F9"><td align=center >'+ebook[2].encode('ascii', 'xmlcharrefreplace')+'</td><td align=left >'+vtitle.encode('ascii', 'xmlcharrefreplace')+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'</td><td align=center >vcodeshere</td><td align=center ><a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vcode+'">Pedir</a></td><td'+vnotestyle+'>'+vnote.encode('ascii', 'xmlcharrefreplace')+'</td></tr>'					
			#fwrite.write(vbook.replace("vcodeshere",vcodes.encode('ascii', 'xmlcharrefreplace')))		
			print str(ebno)+"/"+str(iSQLPosInit+iSQLPosCount),ebook[0], ebook[1], ebook[2], ebook[3], ebook[4]  #, ebook[6], ebook[7], ebook[8], ebook[9], ebook[10], ebook[11]		
			#fupdate.write('\n'+'insert into booksresum values(null, "'+vcodes+'", "'+vauthorS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vtitleS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vyearS+'", "'+vsizeS+'", "'+vlang+'", "'+vnewbookS+'", "'+vcoderichs.encode('ascii', 'xmlcharrefreplace').replace('\\"','""')+'", "'+vlastnote.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vorderauthS.encode('ascii', 'ignore').replace('"',' ')+'","'+vserieS.encode('ascii', 'ignore')+'","'+vcommentS.encode('ascii', 'ignore').replace('"',' ')+'");')
			try:
				fupdate.write('\n'+'insert into booksresum values(null, "'+vcodes+'", "'+vauthorS.replace('"',' ')+'", "'+vtitleS.replace('"',' ')+'", "'+vyearS+'", "'+vsizeS+'", "'+vlang+'", "'+vnewbookS+'", "'+vcoderichs.replace('\\"','""')+'", "'+vlastnote.replace('"',' ')+'", "'+vorderauthS.replace('"',' ')+'","'+vserieS+'","'+vcommentS.replace('"',' ')+'", "'+vnotasimagesS+'", "'+vnote+'");')	
			except:
				try:
					fupdate.write('\n'+'insert into booksresum values(null, "'+vcodes+'", "'+vauthorS.replace('"',' ')+'", "'+vtitleS.replace('"',' ')+'", "'+vyearS+'", "'+vsizeS+'", "'+vlang+'", "'+vnewbookS+'", "'+vcoderichs.replace('\\"','""')+'", "'+vlastnote.replace('"',' ')+'", "'+vorderauthS.encode('ascii', 'ignore').replace('"',' ')+'","'+vserieS.encode('ascii', 'ignore')+'","'+vcommentS.encode('ascii', 'ignore').replace('"',' ')+'", "'+vnotasimagesS+'","'+vnote.encode('ascii', 'ignore').replace('"',' ')+'");')
				except:
					fupdate.write('\n'+'insert into booksresum values(null, "'+vcodes+'", "'+vauthorS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vtitleS.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vyearS+'", "'+vsizeS+'", "'+vlang+'", "'+vnewbookS+'", "'+vcoderichs.encode('ascii', 'xmlcharrefreplace').replace('\\"','""')+'", "'+vlastnote.encode('ascii', 'xmlcharrefreplace').replace('"',' ')+'", "'+vorderauthS.encode('ascii', 'ignore').replace('"',' ')+'","'+vserieS.encode('ascii', 'ignore')+'","'+vcommentS.encode('ascii', 'ignore').replace('"',' ')+'", "'+vnotasimagesS+'","'+premios.encode('ascii', 'ignore').replace('"',' ')+'");')
				# except:
					# pass
			
			ws.write(vnumbooks, 0, vauthorS, vstyle)
			ws.write(vnumbooks, 1, vtitleS, vstyle)
			ws.write(vnumbooks, 2, vyearS, vstyle)
			ws.write(vnumbooks, 3, vsizeS, vstyle)
			ws.write(vnumbooks, 4, vcodes, vstyle)
			ws.write(vnumbooks, 5, xlwt.Formula('HYPERLINK("mailto:'+vebookonmail_email+'?subject=GETRTF '+vcodeS+'";"Pedir")'), vstyle)
			ws.write(vnumbooks, 6, vnote, vstylenote)
								
			
	
	c = vdb.cursor()
	c.execute("delete from booksresum")
	vdb.commit()	
	vlines = file('update.sql')	
	dd=0
	aa=0
	for vline in vlines:
		if not vline.strip()=="" and not vline[0:1]=='#':
			dd=dd+1
			aa=aa+1
			print aa,". ",vline
			try:
				c.execute(vline)
			except:
				fsqlgold = open('errores.txt','a')
				fsqlgold.write('\nSQL: '+vline)
				fsqlgold.close()			
				pass			
			if dd==5000:
				vdb.commit()
				dd=0
				
	vdb.commit()
	vdb.close()
	
	fupdate.close()
	vgentable=True
	
	
if vgentable:	
	#======================
	listno=1
	listpos=0
	fwrite = open(vtodolist,'w')
	fnovedades = open(vnovedades,'w')
	flist = open(vebookonmaillist+str(listno)+'.html','w')
	
	vheadtable = u'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<table cellspacing="0" cellpadding="0" border=1 ><tr bgcolor="#E63B3B"><td align=center ><b>Autor</b></td><td align=center><b>Título</b></td><td align=center ><b>Año</b></td><td align=center ><b>Tamaño</b></td><td align=center ><b>Referencia</b></td><td align=center ><b>Pedir por Email</b></td><td align=center >Notas/Premios</td></tr>'
	# vheadtable=vheadtable.encode('ascii', 'xmlcharrefreplace')
	now = datetime.datetime.now()
	
	vheaddetail="""
<html>
<title></title>
<head>
<meta http-equiv=Content-Type content="text/html; charset=utf-8">
<style type="text/css">
	tr:hover { background: yellow; }
</style>
<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js' type='text/javascript' ></script>
<script  type='text/javascript' >
	var vserver='"""+vservercalibre+"""'
	var vwebdav='"""+vservercalwebdav+"""'

	
	function dl(vpath)
	{
	if (document.main.widthdetails.checked) {
		m=vserver+vpath;
		w=window.open(m,'addwindow','status=no,toolbar=no,width=575,height=545,resizable=yes');
		w.focus();
		} else {	
			open(vserver+vpath)
		}
	}

	function vdclose(vcode)
	{
	$("div#"+vcode).html("")
	}
	
	function vd(vcode,vpath)
	{
	vdesc=""
	// vimage=vwebdav+vpath+"cover.jpg"
	vimage="http://guess.com/cover.jpg?"+vcode
	if (document.main.widthdetails.checked) {
		m='http://guess.com/getdetails.py?path='+vpath+'&withimages';
		w=window.open(m,'addwindow','status=no,toolbar=no,width=575,height=545,resizable=yes');
		w.focus();
	} else {		
	$.get('http://guess.com/getdetails.py?path='+vpath, function(data) {
		vdesc=data
		$("div#"+vcode).html("<hr/><table><tr><td><img src='"+vimage+"' alt='Portada' width='120' /></td><td valign='top'><p align='right'><i>"+vcode+"</i>[<a href='javascript:vdclose("+'"'+vcode+'"'+");void(0)'>X</a>]</p>"+vdesc+"</td></tr></table>")
		//document.location="http://"+document.location.hostname+document.location.pathname+"#"+vcode
		}).ready( document.location="#"+vcode );	
	$("div#"+vcode).html("<hr/><table><tr><td><img src='"+vimage+"' alt='Portada' width='120' /></td><td valign='top'><p align='right'><i>"+vcode+"</i>[<a href='javascript:vdclose("+'"'+vcode+'"'+");void(0)'>X</a>]</p><p>Cargando sinopsis...<img src='loading.gif' /> "+vdesc+"</p></td></tr></table>")
	}
	}"""
	
	for src in vsrc:
		if not vcalibresrc[src+'urlid']=="":
			vheaddetail=vheaddetail+"""
	function """+vcalibresrc[src+'code']+"""(vid)
	{
	if (document.main.widthdetails.checked) {
		m='"""+vcalibresrc[src+'urlid'].replace("vid","'+vid+'")+"""';
		w=window.open(m,'addwindow','status=no,toolbar=no,width=799,height=545,resizable=yes');
		w.focus();
	} else {	
	open('"""+vcalibresrc[src+'urlid'].replace("vid","'+vid+'")+"""')
	}
	}
	"""
	vheaddetail=vheaddetail+"""

	function smail(vcode,vformat)
	{
		if (vformat==''){
			vformat='GET'+document.main.eformat.value+' '
			}
		if (vformat=='list'){
			vformat=''
			}
		vto=' to '+document.main.tomail.value
		if (document.main.tomail.value==''){
			vto=' '
			}
		if (!document.main.tomail.value==''){				
			}
		m='http://mail.google.com/mail/?view=cm&fs=1&tf=1&to="""+vebookonmail_email+"""&su='+vformat+vcode+vto+'&body='+encodeURIComponent('Enviar ebook '+vcode)
		w=window.open(m,'addwindow','status=no,toolbar=no,width=575,height=545,resizable=yes');
		w.focus();
	}
		
	function showcodessel()
	{
	var sList = "";
	$('input[type=checkbox]').each(function () {
		if (this.checked) {
			sList += "GET"+document.main.eformat.value+ " "+ $(this).val() + ", ";
			document.formresult.result.value=sList
			}			
	}).ready( alert(sList) );		
	}

	</script>		
	</head>
	<body>

	<form name='main'>
	Format:
	<select name='eformat' id='eformat' >
	  <option value='RTF' selected>RTF (Word)</option>
	  <option value='MOBI'>MOBI (Kindle)</option>
	  <option value='EPUB'>EPUB (Sony/Nook)</option>
	  <option value='FB2'>FB2 (Papyre/Coolreader)</option>
	  <option value='AZW3'>AZW3 (Kindle)</option>
	  <option value='PDF'>PDF (Acrobat Reader)</option>
	  <option value='HTMLZ'>HTMLZ</option>
	</select>
	toEmail: <input name='tomail' value=''/>	
	[<a href='javascript:document.main.tomail.value="@gmail.com";void(0);'>gmail</a>|<a href='javascript:document.main.tomail.value="@free.kindle.com";void(0);'>kindle</a>]
	Detalles en ventana emergente:<input type="checkbox" name="widthdetails" value=""  checked="checked" />
	<br/>Selecciones: <input type='button' value='Mostrar' onclick='javascript:showcodessel()' />
	</form>
	<form name='fsearch' action='esearch.php' method='get'>
	<hr />
	<input name='s' value=''/>
	<input type='submit' value='Buscar eBook'/>
	</form>
	"""	

	vheadrich=u'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<table cellspacing="0" cellpadding="0" border=1 ><tr bgcolor="#E63B3B"><td align=center ><b>Autor</b></td><td align=center><b>Título</b></td><td align=center ><b>Año</b></td><td align=center ><b>Tamaño</b></td><td align=center ><b>Notas/Imágenes</b></td><td align=center ><b>Referencia</b></td><td align=center >Notas/Premios</td></tr>'
	
	fwrite.write(vheaddetail+"<br />Generado: "+str(now)+""+" [Ver <a href='"+vnovedades+"'>Novedades del mes</a>]")	
	fwrite.write( utf8_str(vheadrich))   #.encode('ascii', 'xmlcharrefreplace')
	
	fnovedades.write(vheaddetail+"<br />Generado: "+str(now)+""+" [Ver <a href='"+vtodolist+"'>Todo</a>]")
	fnovedades.write( utf8_str(vheadrich))   #.encode('ascii', 'xmlcharrefreplace')
	
	flist.write( utf8_str(vheadtable) )
	
	vdb = sqlite3.connect(vresumDB)
	
	vsqlresume="""
		select codes, author, title, year, size, lang, codesrich, notes, new, orderauth, serie, comments, notasimages
		from booksresum 
		order by orderauth asc, year desc, serie desc, title asc"""		
		
	print "SQL: ",vsqlresume
	cur = vdb.execute(vsqlresume)
	vdb.text_factory = lambda x: utf8_str(x, "utf-8", "ignore")
	vdb.text_factory = str	
	
	c = vdb.cursor()
	rows = cur.fetchall()
	vcantebooks=len(rows)	
	vlastauthor=""
	vlastorderauthor=""
	vlastauthor1=""
	ebno=0
	vnewauthor=True
	vNumMailSent=0
	vcodepending=''
	fscp = open('recomendaciones-notes.txt','w')
	fscp.close()
		
	if vcantebooks>0:	
		for ebook in rows:			 
			ebno=ebno+1
			listpos=listpos+1
			vcodes=ebook[0]
			vauthor=ebook[1]
			vtitle=ebook[2]
			vyear=ebook[3]			
			vsize=ebook[4]
			vlang=ebook[5]
			vcodesrich=ebook[6]
			vnotes=ebook[7]
			vnewupdatelastmonth=ebook[8]
			vorderauth=ebook[9]
			vserie=("") if ebook[10].strip()=="" else ebook[10].strip()+' '
			vcomments=("") if ebook[11].strip()=="" else ebook[11].strip()+' '
			vnotesimages=("") if ebook[12].strip()=="" else ebook[12].strip()+' '
			
			if not (vlastorderauthor)==(vorderauth) and not (vlastauthor)==(vauthor):
				#and not soundexstr(vlastorderauthor.encode('ascii', 'ignore')) in soundexstr(vorderauth.encode('ascii', 'ignore')) and not soundexstr(vorderauth.encode('ascii', 'ignore')) in soundexstr(vlastorderauthor.encode('ascii', 'ignore')):
				vbgcolor= ' bgcolor="#A2B0F9" '
				vlastorderauthor=vorderauth
				vlastauthor=vauthor
				vauthor='<td align=center >'+vlastauthor+'</td>'
				vnewauthor=True
			else:
				vauthor="<td></td>"
				vbgcolor= ''	
				vnewauthor=False
			print listno,"/",listpos, vauthor, " - ", vtitle," - ", vcodes
			vcodehtml=(vcodesrich) if vHTMLDetails else vcodes
			
			vSendEmailCode=""
			vfirstcode=""
			vSendEmailHTMLCode=""
			vcodesplit=vcodes.split(",")
			vnewbook=True
			vhuckmark=""
			vmarkbook=" "
			vcheckboxbook=""
			vnotecodeinrecomend=True

			for src in vnotnewbooks:
				if src in vcodes:
					vnewbook=False	

			for vvv in vcodesplit:
				vhuckmark=vhuckmark+"<a name='"+vvv+"'/>"
				vfirstcode= (vvv) if vfirstcode=="" else vfirstcode
				if vvv in open('emaillist.txt').read():
					vnotecodeinrecomend=False
				vSendEmailCode= ('<a href="mailto:'+vebookonmail_email+'?subject=GETRTF '+vvv+'">Pedir</a>') if vSendEmailCode=="" else vSendEmailCode
				if (vcheckboxbook==""):
					vcheckboxbook='<input type="checkbox" name="'+vvv+'" value="'+vvv+'" />'
				logtexts = file('ebookonmail.log')						

								
				logtexts = file('ebookonmail.log')						
				for logtext in logtexts:					
					if "kindle.com" in logtext:				
						if 	(vvv+"|" in logtext)  or (vvv+" to" in logtext):
							vmarkbook=(vmarkbook+"<span style='background-color: green;'><b>$</b></span>") if (not "$" in vmarkbook) else vmarkbook
				if not vmarkbook==" ":
					if not ">X<" in vmarkbook:
						vmarkbook='-'+vmarkbook.strip() 
					if not ">$<" in vmarkbook:
						vmarkbook=vmarkbook.strip()+'-'
						
				logtexts = file('recomendaciones.txt')						
				for logtext in logtexts:
					logtext=logtext.replace(" ",",")
					try:
						if ","+vvv+"," in ","+logtext+",":						
							vmarkbook=vmarkbook.strip()+"<span style='background-color: blue;'><b>*</b></span>"

					except:
						pass
								
					
			bgcolnote = ' ' 
			if "red" in vnotes:
				bgcolnote = ' bgcolor="red" '				
			if "green" in vnotes:
				bgcolnote = ' bgcolor="green" '
			if "yellow" in vnotes:	
				bgcolnote = ' bgcolor="yellow" ' 

			divcodes=""
			if "," in vcodes:
				vttt=vcodes.split(",")
				for vt in vttt:
					divcodes=divcodes+"<div id='"+vt+"' ></div>"
			else:
				divcodes="<div id='"+vcodes+"' ></div>"
				
			if vnewbook and vnewupdatelastmonth=="1":	
				vauthor1="<td></td>"
				vbgcolor1= ''
				if not (vlastauthor1)==(vlastauthor):
					vlastauthor1=vlastauthor
					vbgcolor1= ' bgcolor="#A2B0F9" '
					vauthor1='<td align=center >'+vlastauthor+'</td>'
				# try:
					# fnovedades.write('\n<tr'+vbgcolor1+'>'+vauthor1+'<td align=left >'+vserie+vtitle+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vcodes+'</td><td align=center >'+vSendEmailCode+'</td><td align=center '+bgcolnote+' >'+vnotes+'</td></tr>')	
				# except:
					# fnovedades.write('\n<tr'+vbgcolor1+'>'+vauthor1.encode("ascii","ignore")+'<td align=left >'+vserie.encode("ascii","ignore")+vtitle.encode("ascii","ignore")+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vcodes+'</td><td align=center >'+vSendEmailCode+'</td><td align=center '+bgcolnote+' >'+vnotes.encode("ascii","ignore")+'</td></tr>')
					
				try:
					fnovedades.write('\n<tr'+vbgcolor1+'>'+vauthor1+'<td align=left >'+vhuckmark+vcheckboxbook+vmarkbook+'<i>'+vserie+vtitle+divcodes+'</i></td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vnotesimages+'</td><td align=center >'+vcodehtml+'</td><td align=center >'+vnotes+'</td></tr>')	
				except:
					fnovedades.write('\n<tr'+vbgcolor1+'>'+vauthor1.encode("ascii","ignore")+'<td align=left >'+vhuckmark+vcheckboxbook+vmarkbook+'<i>'+vserie.encode("ascii","ignore")+vtitle.encode("ascii","ignore")+divcodes+'</i></td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vnotesimages+'</td><td align=center >'+vcodehtml+'</td><td align=center >'+vnotes.encode("ascii","ignore")+'</td></tr>')					
					
				if vnewupdatelastmonth=="1":
					vnotes=("<span style='background-color: red;'><i>New</i></span>") if vnotes=="" else vnotes+", <span style='background-color: red;'><i>New</i></span>"
				if bgcolnote.strip() == "":
					# bgcolnote = ' bgcolor="red" '	
					bgcolnote = ' '

			if listpos>vcantbookinlistexcel and vnewauthor:
				listno=listno+1
				flist.write("</table>")
				flist.close()
				flist = open(vebookonmaillist+str(listno)+'.html','w')
				flist.write( utf8_str(vheadtable) )
				listpos=0
			
			try:
				flist.write('\n<tr'+vbgcolor+'>'+utf8_str(vauthor)+'<td align=left >'+utf8_str(vserie)+" "+utf8_str(vtitle)+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vcodes+'</td><td align=center >'+vSendEmailCode+'</td><td align=center '+bgcolnote+' >'+vnotes+'</td></tr>')	
			except:
				flist.write('\n<tr'+vbgcolor+'>'+vauthor.encode("ascii","ignore")+'<td align=left >'+vserie.encode("ascii","ignore")+" "+vtitle.encode("ascii","ignore")+'</td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vcodes+'</td><td align=center >'+vSendEmailCode+'</td><td align=center '+bgcolnote+' >'+vnotes.encode("ascii","ignore")+'</td></tr>')	
			
			divcodes=""
			if "," in vcodes:
				vttt=vcodes.split(",")
				for vt in vttt:
					divcodes=divcodes+"<div id='"+vt+"' ></div>"
			else:
				divcodes="<div id='"+vcodes+"' ></div>"
							
			if vnotes<>"" and vnotecodeinrecomend and ("green" in vnotes or "yellow" in vnotes ) and vfirstcode.strip()<>"":
				fscp = open('recomendaciones-notes.txt','a')
				fscp.write("\n"+vfirstcode.strip())
				fscp.close()
			else:
				if "SEL" in vcodesplit:
					fscp = open('recomendaciones-notes.txt','a')
					fscp.write("\n"+vfirstcode.strip())
					fscp.close()				
			
			try:
				fwrite.write('\n<tr'+vbgcolor+'>'+vauthor+'<td align=left >'+vhuckmark+vcheckboxbook+vmarkbook+'<i>'+vserie+vtitle+divcodes+'</i></td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vnotesimages+'</td><td align=center >'+vcodehtml+'</td><td align=center >'+vnotes+'</td></tr>')	
			except:
				fwrite.write('\n<tr'+vbgcolor+'>'+vauthor.encode("ascii","ignore")+'<td align=left >'+vhuckmark+vcheckboxbook+vmarkbook+'<i>'+vserie.encode("ascii","ignore")+vtitle.encode("ascii","ignore")+divcodes+'</i></td><td align=center >'+vyear+'</td><td align=center >'+vsize+'k</td><td align=center >'+vnotesimages+'</td><td align=center >'+vcodehtml+'</td><td align=center >'+vnotes.encode("ascii","ignore")+'</td></tr>')

	
	fnovedades.write("</table>")
	fnovedades.write("\n<form name='formresult'><textarea name='result' rows='4' cols='50'></textarea><input type='button' value='Pedir' onclick='javascript:smail(document.formresult.result.value,"+'"list"'+")' /></form>")
	fnovedades.write("\n</body></html>") 	
	fnovedades.close()		
	
	flist.write("</table>")
	flist.close()		
	
	fwrite.write("\n</table>") 
	fwrite.write("\n<form name='formresult'><textarea name='result' rows='4' cols='50'></textarea><input type='button' value='Pedir' onclick='javascript:smail(document.formresult.result.value,"+'"list"'+")' /></form>")
	fwrite.write("\n</body></html>") 
	fwrite.close()	
	
	#Generar las tablas excel resultantes...
	print "Generando las tablas excel..."
	#for htmlfile in glob.glob("*.html"):
		#os.system('soffice --headless --convert-to xls '+htmlfile)

	print "Cantidad de libros: ",vnumbooks

	#c.execute("VACUUM;")
	vdb.commit()
	vdb.close()

	#wb.save('todo-list.xls')
	
	if os.path.isfile(vscriptpostgenlist):
		os.system('bash '+vscriptpostgenlist)
	

#sys.exit(6)

if os.path.isfile("wwwupdate.sh"):
	os.system('bash wwwupdate.sh')
	
vfound=False
vNumMailSent=0
ebooknotfound=''
vcodepending=''
vcalibredest='/media/users/guess/Calibre-libraries/toshare/'
vscriptpath = os.path.dirname(os.path.abspath(__file__))
os.system('mkdir -p "temp"')

if vgencalibrelist:
	vdb = sqlite3.connect(vresumDB)

	os.system('mkdir -p bashtoshare')

	fscp = open('cp-toshare.sh','w')
	fscp.write("\n"+'unset DISPLAY')
	fscp.write("\n"+'cd bashtoshare')
	fscp.write("\n"+'for f in *.* ; do bash $f; done')   
	fscp.close()
	
	fsss = open('cp-toshare-error.log','w')
	fsss.close()		

	recomends = file('recomendaciones.txt')		
	fscp = open('recomendaciones-notes.txt','a')
	for recomend in recomends:
		if recomend.strip() <>"":
			aaa=recomend.split(",")
			for vvv in aaa: 
				fscp.write("\n"+vvv.strip())
	fscp.close()
	os.system('sort -u recomendaciones-notes.txt -o recomendaciones-notes.txt')

	lastvvv=""	
	recomends = file('recomendaciones-notes.txt')	
	fscp = open('recomendaciones-finales.txt','w')
	for recomend in recomends:
		if recomend.strip() <>"":
			aaa=recomend.split(",")
			for vvv in aaa: 
				vvv = vvv.replace("\n","").replace("\r","").replace(" ","")
				if lastvvv<>vvv.strip() and vvv<>"":
					lastvvv=vvv.strip()
					fscp.write("\n"+vvv.strip())
	fscp.close()
	os.system('sort -u recomendaciones-finales.txt -o recomendaciones-finales.txt')	

	recomends = file('recomendaciones-finales.txt')
	vtpos=0
	lastvvv=""
	for recomend in recomends:
		recomend=","+recomend.replace(" ",",")+","
		aaa=recomend.split(",")
		vlastebook=""
		
		for vvv in aaa:
			vvv = vvv.replace("\n","").replace("\r","")
			if vvv.strip()<>"" and lastvvv.strip()<>vvv.strip():
				try:		
					lastvvv=vvv.strip()
					#Buscar ruta de libro en biblioteca calibre...	
					for src in vsrc:
						vtpos=vtpos+1
						vdblocalroot=vcalibresrc[src+'path']
						vdblocalroot=vdblocalroot.replace(vcalibreabssrc,'')
						ebookpath = ''
						ebookauth = ''
						ebooktitle = ''
						ebookyear = ''						
						
						vcalibresrc[src+'path']
						if vcalibresrc[src+'code'].upper() in vvv.upper():
							vebooknum=vvv.replace(vcalibresrc[src+'code'],"")
							vebooknum=vebooknum
					
							if vcalibresrc[src+'type']=='identifiers':						
								ebookpath, ebookauth, ebooktitle, ebookyear=getebookpath_fromidentifiers(vcalibresrc[vbiblio+'preidval']+vebooknum+vcalibresrc[src+'postidval'],vcalibresrc[src+'id'],vdblocalroot,vcalibresrc[src+'path'])
							if vcalibresrc[src+'type']=='custom' or vcalibresrc[src+'type']=='customfield':
								ebookpath, ebookauth, ebooktitle, ebookyear=getebookpath_fromcustom(vcalibresrc[vbiblio+'preidval']+vebooknum+vcalibresrc[src+'postidval'],vcalibresrc[src+'id'],vdblocalroot,vcalibresrc[src+'path'])
							
							vabsbookpath=ebookpath.replace(vcalibresrc[src+'path'],"")

							print "  ",vtpos,"/",vvv," - ",vabsbookpath," : ",vcalibresrc[src+'code']+vebooknum
							if (ebookpath==""):
								ebooknotfound=ebooknotfound+","+vvv
							else:
								if vlastebook<>vcalibresrc[src+'code']+vebooknum:
									vlastebook=vcalibresrc[src+'code']+vebooknum
									#if not os.path.isdir(vcalibredest+vabsbookpath) or True:
									if not os.path.isdir(vcalibredest+vabsbookpath):
										#os.system('mkdir -p "'+vcalibredest+vabsbookpath+'"')
										#os.system('cp "'+ebookpath+'/cover.jpg" "'+vcalibredest+vabsbookpath+'"')
										#os.system('cp "'+ebookpath+'/metadata.opf" "'+vcalibredest+vabsbookpath+'"')

										#Copiar todo
										#os.system('cp -R -u "'+ebookpath+'/" "'+vcalibredest+vabsbookpath+'/.."')
										vbashname=str(vtpos)
										vbashname=vbashname.zfill(5)
										fscp = open('bashtoshare/'+vbashname+'.sh','w')
										fscp.write("\n"+"\n echo '$(date)' \n echo '---------------'"+"\n"+'echo "'+str(vtpos)+'. Copiando libros de '+vabsbookpath+'..."')
										fscp.write('\nmkdir -p "'+vcalibredest+vabsbookpath+'"')
										fscp.write('\ncp -R -u "'+ebookpath+'/.." "'+vcalibredest+vabsbookpath+'/.."')
										
										# ebook-meta -t "El contador de historias" -a "Alameddine, Rabih" --category="" -l "es"  "/media/users/guess/Calibre-libraries/toshare/Alameddine, Rabih/El contador de historias (3465)/El contador de historias - Alameddine, Rabih.prc"

										vcodes=""
										#vdb = sqlite3.connect(vresumDB)	
										vsqlttt="select codes, author, title, year from booksresum where codes='"+vvv.strip()+"'"		
										cur = vdb.execute(vsqlttt)
										c = vdb.cursor()
										rows = cur.fetchall()
										vcantebooks=len(rows)		
										if vcantebooks>0:	
											for ebook in rows:	
												vcodes=ebook[0]
												vauthor=parser.unescape(ebook[1])
												vtitle=parser.unescape(ebook[2])
												vyear=ebook[3]											
										else:
												vsqlttt="select code, author, title, year from books where code='"+vvv.strip()+"'"		
												cur = vdb.execute(vsqlttt)
												c = vdb.cursor()
												rows = cur.fetchall()
												vcantebooks=len(rows)		
												if vcantebooks>0:
													for ebook in rows:	
														vcodes=ebook[0]
														vauthor=parser.unescape(ebook[1])
														vtitle=parser.unescape(ebook[2])
														vyear=ebook[3]
										c.close()
										if not vcodes=="":
											vcodes=vvv.strip()
											ebookauth=vauthor  
											ebooktitle=vtitle
											ebookyear=vyear
											fsss = open('cp-toshare-error.log','a')
											fsss.write("\n"+vcodes)
											fsss.close()										
										
										if not vcodes=="":
											print "  ",'Meta: '+vtitle+' - '+vauthor+' ('+vyear+')'
											fscp.write("\n"+"\n"+'cd "'+vcalibredest+vabsbookpath+'/"')
											fscp.write("\n"+' if ! [ -f "passed" ]; then')
											fscp.write("\n"+'    echo "" > passed')
											try:
												fscp.write("\n"+'    for f in *.* ; do ebook-meta -t "'+vtitle+'" -a "'+vauthor+'" --author-sort="'+vauthor+'" -d "'+vyear+'" -l "es" "$f"; done')
											except:
												# vtitle=vtitle.encode('utf-8')
												vtitle=utf8_str(vtitle)
												# vauthor=vauthor.encode('utf-8')
												vauthor=utf8_str(vauthor)
												fscp.write("\n"+'    for f in *.* ; do ebook-meta -t "')
												fscp.write(vtitle)
												fscp.write('" -a "')
												fscp.write(vauthor)
												fscp.write('" --author-sort="')
												fscp.write(vauthor)
												fscp.write('" -d "'+vyear+'" -l "es" "$f"; done')
											
											fscp.write("\n"+'    rm *.opf')
											fscp.write("\n"+'    for f in *.fb2 ; do if [ -f "$f" ]; then ebook-meta --to-opf=metadata.opf "$f"; fi; done')
											fscp.write("\n"+'    for f in *.epub; do if ! [ -f "${f%.epub}.fb2" ] && [ -f "$f" ]; then ebook-meta --to-opf=metadata.opf "$f"; fi; done')  
											fscp.write("\n"+' fi; ')
											fscp.write("\n"+'cd "'+vcalibredest+vabsbookpath+'/.."')
											fscp.write("\n"+'for d in *; do ')
											fscp.write("\n"+' if [ -d "$d" ] && ! [ -f "$d/passed" ]; then')
											fscp.write("\n"+'    cd "$d"')
											fscp.write("\n"+'    echo "" > passed')		
											fscp.write("\n"+'    echo ""')										
											fscp.write("\n"+'    echo "'+str(vtpos)+'***** $d ****** $(date)"')

											fscp.write("\n"+'    for f in *.* ; do ebook-meta -a "'+vauthor+'" --author-sort="'+vauthor+'" -l "es" "$f"; done')
											fscp.write("\n"+'    rm *.opf')
											fscp.write("\n"+'    for f in *.fb2 ; do if [ -f "$f" ]; then ebook-meta --to-opf=metadata.opf "$f"; fi; done')
											fscp.write("\n"+'    for f in *.epub; do if ! [ -f "${f%.epub}.fb2" ] && [ -f "$f" ]; then ebook-meta --to-opf=metadata.opf "$f"; fi; done')  

											fscp.write("\n"+'    for f in *.fb2 ; do if ! [ -f "${f%.fb2}.epub" ] && [ -f "$f" ]; then /opt/calibre/ebook-convert  --flow-size=3000 --no-inline-fb2-toc --enable-heuristics --prefer-metadata-cover "$f" "${f%.fb2}.epub"; fi; done')		
											

											fscp.write("\n"+'    for f in *.epub ; do if ! [ -f "${f%.epub}.mobi" ] && [ -f "$f" ]; then ebook-meta -l "es" "$f"; fi; done')
											fscp.write("\n"+'    for f in *.epub ; do if ! [ -f "${f%.epub}.mobi" ] && [ -f "$f" ]; then /opt/lampp/htdocs/ebookonmail/kindlegen/kindlegen -c1 -locale es "$f"; fi; done')										
											fscp.write("\n"+'    for f in *.mobi ; do  if [ -f "$f" ]; then /opt/calibre/calibre-debug -e /opt/lampp/htdocs/ebookonmail/kindlestrip.py "$f" "$f"; fi; done')
											fscp.write("\n"+'    for f in *.epub ; do if ! [ -f "${f%.epub}.mobi" ] && [ -f "$f" ]; then /opt/calibre/ebook-convert  --flow-size=3000 --no-inline-fb2-toc --enable-heuristics --prefer-metadata-cover "$f" "${f%.epub}.mobi"; fi; done')
											fscp.write("\n"+'    for f in *.fb2 ; do if ! [ -f "${f%.fb2}.mobi" ] && [ -f "$f" ]; then /opt/calibre/ebook-convert  --flow-size=3000 --no-inline-fb2-toc --enable-heuristics --prefer-metadata-cover "$f" "${f%.fb2}.mobi"; fi; done')

											fscp.write("\n"+'    cd "'+vcalibredest+vabsbookpath+'/.."')
											fscp.write("\n"+' fi; ')
											fscp.write("\n"+'done')
										
											fscp.close()
										else:
											fsss = open('cp-toshare-error.log','a')
											fsss.write("\n"+vvv.strip()+" no encontrado...")
											fsss.close()
										

										

				except:
					pass		

	print "Ebooks no encontrados en selección: "+ebooknotfound				
				
