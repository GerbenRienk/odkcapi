'''
Created on 20200123
based on the oc3 version
@author: Gerben Rienk
'''
import json

from utils.dictfile import readDictFile
from utils.odkc_api import OdkCentralApi
import xml.etree.ElementTree as ET

from _operator import itemgetter
        
if __name__ == '__main__':

	config=readDictFile('tb043.config')

	# create a list of PID's
	all_pids=[]

	# start with requesting an authentication token, which we can use for some time
	api = OdkCentralApi(config['odkc_url'])
	aut_token = api.sessions.get_authentication_token(config['odkc_user'], config['odkc_password'],verbose=False)
	# print(aut_token)
	submission_list = api.submissions.list_submissions(aut_token=aut_token, project_id=config['project_id'], form_id=config['form_id'], verbose=False)
	print('checking duplicates:')
	for submission in submission_list:
		instance_data = api.submissions.submission_data(aut_token=aut_token, project_id=config['project_id'], form_id=config['form_id'], instance_id=submission['instanceId'], verbose=False)
		#read the xml data
		root = ET.fromstring(instance_data)
		#find the PID
		print(instance_data)
		for info in root.findall('page-welcome'):
			new_pid = info.find('PID').text          
		
		#check if the new pid is already in all pids
		if new_pid in all_pids:
			print('PID %s is more than once in the list of randomized PID\'s' %new_pid)
		else:
			all_pids.append(new_pid)
	
	
