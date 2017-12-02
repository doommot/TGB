#cd desktop\grisha\progproj\tgb\v0.3
#C:\users\user\appdata\local\programs\python\python36-32\python.exe cluster.py
from account import account
import data.clusterAlpha

class cluster:
	accounts_file = 'Empty_cluster'
	account_list = []

	def __init__(self, cluster_name): #recieves name of file with phones list
		self.accounts_file=cluster_name
		self.__log('Creating cluster')
		initcount = 0
		accountcount= len(data.clusterAlpha.phones) - 1
		while initcount <= accountcount:
			self.account_list[initcount] = account(data.clusterAlpha.phone[initcount])

	def __log(self, line):
		log_stream = open(config.logfile, "a", encoding = 'utf8')
		mem = 'CLST:' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + line +' '+self.datafolder+'\n'
		log_stream.write(mem)
		log_stream.close()