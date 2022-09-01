'''
Created on 20200123
based on the oc3 version
@author: Gerben Rienk
'''
import json
import datetime
from utils.dictfile import readDictFile
from utils.odkc_api import OdkCentralApi
from utils.reporter import Reporter
from utils.logmailer import Mailer
from _operator import itemgetter
import xml.etree.ElementTree as ET
        
if __name__ == '__main__':
	# read the configuration
	config=readDictFile('tb043.config')
	# setup a report
	this_date = datetime.datetime.now()
	date_stamp = this_date.strftime("%Y%m%d")
	report_name = 'logs/list_duplicates_%s.log' % date_stamp 
	my_report = Reporter(report_name)
	start_time = datetime.datetime.now()
	my_report.append_to_report('start checking for duplicates at %s' % str(start_time))
	# set up the mailer
	my_mailer = Mailer(config)
	# create a list of PID's
	all_pids=[]

	# start with requesting an authentication token, which we can use for some time
	api = OdkCentralApi(config['odkc_url'])
	aut_token = api.sessions.get_authentication_token(config['odkc_user'], config['odkc_password'],verbose=False)
	
	project_list = api.projects.list_projects(aut_token=aut_token, verbose=False)
	
	for project in project_list:
		if (project['id'] == int(config['project_id'])):
			my_report.append_to_report('Project: %s: %s' % (project['id'],  project['name']))
	my_report.append_to_report('Form: %s' % (config['form_id']))
    
	submission_list = api.submissions.list_submissions(aut_token=aut_token, project_id=config['project_id'], form_id=config['form_id'], verbose=False)
	total_duplicates = 0
	for submission in submission_list:
		print(submission)
		instance_data = api.submissions.submission_data(aut_token=aut_token, project_id=config['project_id'], form_id=config['form_id'], instance_id=submission['instanceId'], verbose=False)
		#read the xml data
		root = ET.fromstring(instance_data)
		#find the PID
		for info in root.findall('page-welcome'):
			new_pid = info.find('PID').text          
		
		#check if the new pid is already in all pids
		if new_pid in all_pids:
			total_duplicates = total_duplicates + 1
			my_report.append_to_report('PID %s is more than once in the list of randomized PID\'s' %new_pid)
		else:
			all_pids.append(new_pid)
	my_report.append_to_report('Number of duplicates found: %s' % total_duplicates)
    # send the report
	my_mailer.send_file(report_name)
	print('finished checking')