#cd desktop\grisha\progproj\tgb\v0.3
#C:\users\user\appdata\local\programs\python\python36-32\python.exe account.py
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
import config
from datetime import datetime, timedelta
import random
import data.names

class account:
	#data of account
	phone = None
	client = None #объект сетевого интерфейса данного аккаунта, через методы которого происходят все действия.

	def __init__(self, phone=None): #constructor, phone if registered, empty if not
		if(phone):
			self.phone=phone
			self.__client_connect()
		elif(not phone):
			pass
		else:
			__log('internal __init__ error')
			raise internalError ('phone and !phone can not exist both')

	def subscribe(self, channel):
		entity  = self.client.get_entity(channel)
		self.client(JoinChannelRequest(entity))
		self.__log('join '+channel)

	def unsubscribe(self, channel):
		self.client.LeaveChannelRequest(channel)
		self.__log('join '+channel)

	def send(self, entity, text=None, file=None, force_document=False): #params: username, text(optional), /path/to/the/file.jpg (optional)
		if(text):
			if(file):
				self.__log('sending text with file to '+entity+' ')
				self.client.send_message(entity, text)
				self.client.send_file(entity, file, force_document=force_document)
			else:
				self.__log('sending text to '+entity+' ')
				self.client.send_message(entity, text)
		else:
			if(file):
				self.__log('sending file to '+entity+' ')
				self.client.send_file(entity, file, force_document=force_document)
			else:
				self.__log('ValueError while sending nothing to '+entity+' ')
				raise ValueError('text or file needed')

	def login(self, password=None):
		self.__client_connect()
		self.client.send_code_request(self.phone) #sending code, client stores hash.
		self.__log('logging in. Code is sent')
		if(password):
			self.client.sign_in(phone=self.phone, code=input("Enter Code:"), password=password)
			self.__log(password + ' password for ')
		else:
			self.client.sign_in(phone=self.phone, code=input("Enter Code:")) #verifying code with hash that has been recieved by account

	def reg(self, phone):
		self.phone=phone
		self.__log('initialization of account ')
		self.__client_connect()
		firstname = random.choice(names.firstnames)
		self.__log('firstname is chosen ' + firstname)
		lastname = random.choice(config.lastnames)
		self.__log('lastname is chosen ' + lastname)
		self.client.send_code_request(self.phone)
		self.__log('code is sent')
		self.client.sign_up(input("\nEnter Code:"), firstname, lastname)

	def __client_connect(self):
		session_file_name = self.phone #we will have a +71234567890.session file with all data. It will be needed to connect
		self.client = TelegramClient(session_file_name, config.api_id, config.api_hash, timeout=timedelta(seconds=30))
		for i in range (0,5):
			self.__log('connecting... ')
			if (i==4):
				self.__log('unable to connect ')
				raise ConnectionError ("Unable to connect")
			if(self.client.connect()):
				self.__log('connected ')
				break

	def terminate(self):
		if(self.client.log_out):
			self.__log('terminated session ')
		else:
			self.__log('unable to terminate, RPC error ')
		'''self.user = None'''
		self.phone = None
		self.client = None
		self.__log('account already forgotten, Dominouse')

	def __log(self, line):
		log_stream = open(config.logfile, "a", encoding = 'utf8')
		mem = 'ACCN:' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + line +' '+self.phone+'\n'
		log_stream.write(mem)
		log_stream.close()