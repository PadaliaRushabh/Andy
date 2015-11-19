'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
############################---------------ANDY-signer : Android Certificate Automation.-------------#######################
############################---------------The script's name is Andy. -------------------------------#######################
############################---------------Its only purpose is to automate the keystore generation and signing the apk. ####
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@author: Shivang and Rushabh Padalia
'''

import subprocess, os
import sys, pexpect, getopt
import config

class SignApp:
	def __init__(self):
		self.alias = config.alias
		self.pwd = config.pwd # Password can be changed here.
		self.name = config.name
		self.org_unit = config.org_unit
		self.org = config.org
		self.city = config.city
		self.state = config.state
		self.country_code = config.country_code
		self.version = 0.2
		self.apk_path = None
		self.keystore_name = None


	def generateKeystore(self):
		#keytool -genkey -v -keystore <keystore_name> -alias <alias_name> -keyalg RSA -keysize 2048 -validity 10000		
		keytool_cmd = 'keytool -genkey -v -keystore '+ self.keystore_name +' -alias '+self.alias +' -keyalg RSA -keysize 2048 -validity 10000'
		try:
			if os.path.isfile(self.keystore_name):
				print "Keystore file named '" + self.keystore_name +"' already exists."
				sys.exit(0)
			child = pexpect.spawn(keytool_cmd, timeout=None)
			child.expect('Enter keystore password: ')
			child.sendline(self.pwd) 			
			child.expect('Re-enter new password: ')			
			child.sendline(self.pwd)			
			child.expect('What is your first and last name?') #names
			child.sendline(self.name)			
			child.expect('What is the name of your organizational unit?') #Organizational_unit
			child.sendline(self.org_unit)			
			child.expect('What is the name of your organization?') #Organization
			child.sendline(self.org)			
			child.expect('What is the name of your City or Locality?') #City
			child.sendline(self.city)
			child.expect('What is the name of your State or Province?') #State
			child.sendline(self.state)
			child.expect('What is the two-letter country code for this unit?') #Two-letter Country Code
			child.sendline(self.country_code)			
			child.expect('Is CN=')
			child.sendline('yes')						
			child.expect('Generating 2,048 bit RSA key pair')			
			child.sendline(self.pwd)						
			child.expect('Re-enter new password:')
			child.sendline(self.pwd)			
			i = child.expect(['$','#'])
			if i==0 or i==1:
				child.sendline('pwd')			
			child.close()
			print "Done"

		except Exception as e:
			print "Sorry. There seem to be some problem with Andy-Signer"
			print e

	def signIt(self, apk_path):
		#jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore my_application.apk alias_name
		signer_cmd = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore " + self.keystore_name +" "+ apk_path +" " + self.alias
		print signer_cmd
		try:
			child = pexpect.spawn(signer_cmd)
			child.expect('Enter Passphrase for keystore:')
			child.sendline(self.pwd)

			child.delaybeforesend = 2 
			i = child.expect(['$', '#'])
			if i==0 or i==1:
				child.sendline('pwd')		
			child.close()

			print "Apk signed successfully."

		except Exception as e:
			print "Something went wrong during Signing the apk"
			print "Description: ", e
		pass
	
	def decompile(self, apk_path):
		apktool_cmd = "java -jar apktool.jar if" + " " + apk_path 
		print apktool_cmd
		try:
			child = pexpect.spawn(apktool_cmd)
			print child.read()
			child.delaybeforesend = 2 
			i = child.expect(['$', '#'])
			if i==0 or i==1:
				child.sendline('pwd')		
			child.close()

		except Exception as e:
			print "Something went wrong during framework installation"
			print "Description: ", e
		pass
	
		apktool_cmd = "java -jar apktool.jar d" + " " + apk_path
		print apktool_cmd
		try:
			child = pexpect.spawn(apktool_cmd)
			print child.read()
			child.delaybeforesend = 2 
			i = child.expect(['$', '#'])
			if i==0 or i==1:
				child.sendline('pwd')		
			child.close()

		except Exception as e:
			print "Something went wrong during decompiling"
			print "Description: ", e
		pass
	
	def recompile(self, apk_path):
		apktool_cmd = "java -jar apktool.jar b" + " " + apk_path
		print apktool_cmd
		try:
			child = pexpect.spawn(apktool_cmd)
			print child.read()
			child.delaybeforesend = 2 
			i = child.expect(['$', '#'])
			if i==0 or i==1:
				child.sendline('pwd')		
			child.close()

		except Exception as e:
			print "Something went wrong during framework installation"
			print "Description: ", e
		pass
	def analyze(self):
		#Check for jarsigner and keystore present or not.
		pass
	

if __name__ == "__main__":
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "g:n:s:d:r:" , ['generate-keystore=' , "keystore-name=", "sign-apk=" , 'decompile=' , 'recompile=',  'version'])
        
    except getopt.GetoptError:
        print "python andy.py -g <Keystore_name>"
        print "python andy.py -n <keystore_name> -s <path_to_apk>"
        print "python andy.py -d <path_to_apk_decompile>"
        print "python andy.py -r <path_to_folder_to_recompile>"
        sys.exit(2)
    #print opts
    obj = SignApp()
    for opt, arg in opts:
		print "opt" + opt
		if opt == "-d":
			obj.decompile(arg)
			sys.exit(2)
		if opt == "-r":
			obj.recompile(arg)
			sys.exit(2)		
		if opt == "-n":
			if len(opts) is not 2:
				print "python andy.py -n <keystore_name> -s <path_to_apk>"
				sys.exit(2)
			elif obj.apk_path == None:
				obj.keystore_name = arg
			else:
				obj.keystore_name = arg
				obj.signIt(obj.apk_path)
				sys.exit(2)
		if opt == "-s":
			if len(opts) is not 2:
				print "python andy.py -n <keystore_name> -s <path_to_apk>"
			elif obj.keystore_name == None:
				obj.apk_path = arg
			else:
				obj.apk_path = arg
				obj.signIt(obj.apk_path)
				sys.exit(2)
		if opt == '-g':
		    obj.keystore_name = arg
		    obj.generateKeystore()
		    sys.exit(2)


        
    
    

    

