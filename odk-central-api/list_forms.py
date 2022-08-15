'''
Created on 20200123
based on the oc3 version
@author: Gerben Rienk
'''
import json

from utils.dictfile import readDictFile
from utils.odkc_api import OdkCentralApi

from _operator import itemgetter
        
if __name__ == '__main__':
    
    config=readDictFile('tb043.config')
    
    # start with requesting an authentication token, which we can use for some time
    api = OdkCentralApi(config['odkc_url'])
    aut_token = api.sessions.get_authentication_token(config['odkc_user'], config['odkc_password'],verbose=False)
    # print(aut_token)
    forms_list = api.forms.list_forms(aut_token=aut_token, project_id=config['project_id'], verbose=False)
    print('your forms:')
    for form in forms_list:
        print(form['xmlFormId'])
        
    print('---')
