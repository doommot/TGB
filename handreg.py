from account import account
import config
from datetime import datetime

def log(line):
	log_stream = open(config.logfile, "a", encoding = 'utf8')
	mem = 'HREG:' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + line+'\n'
	log_stream.write(mem)
	log_stream.close()

accounts = []
for x in range (int(input("How many accs to reg?\n"))):
	accounts.append(account())
	log("account reg"+str(x))
	accounts[x].reg(input("Enter phone:\n"))


def save_accounts_list(accounts):#!this will rewrite current list
	log("saving account list")
	f=open(config.accountfile,'a')#filename must be in class fields
	for ele in l1:
		f.write(ele+'\n')
	f.close()