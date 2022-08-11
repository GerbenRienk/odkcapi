import requests
import json

class OdkApi(object):

    def __init__(self, config):
        self.url = config['odk_api_url']
        self.user = config['odk_api_username']
        self.password = config['odk_api_password']
        self.headers = {"content-type": "application/json"}        
        self.utils = _Utils(self)
        self.submissions = _Submissions(self)
        

class _Utils(object):

    def __init__(self, odk_api):
        self.api = odk_api

    def request(self, data=None, request_type=None, url=None, headers=None, params=None, files=None, verbose=False):
        """
        Return the result of an api call, or None.
        """
        auth = requests.auth.HTTPDigestAuth(self.api.user, self.api.password)
        if url is None:
            url = self.api.url
        if headers is None:
            headers = self.api.headers
        return_value = None
        try:
            if verbose == True:
                print("p url=     %s   " % url)
                #print("p params=  %s   " % params)
                #print("p headers= %s   " % headers)
                #print("p data=    %s   " % data)
                print("p user=    %s   " % self.api.user)
                print("p type=    %s \n" % request_type)
            
            if request_type == 'post':
                response = requests.post(url, params=params, headers=headers, data=data, files=files, auth=auth)
                
            if request_type == 'get':
                response = requests.get(url, params=params, headers=headers, data=data, auth=auth)
            
            if request_type == 'put':
                response = requests.put(url, params=params, headers=headers, data=data)
            
            if request_type == 'delete':
                response = requests.delete(url, params=params, headers=headers, data=data)
            
            if verbose == True:
                #print("req url         = %s   " % response.request.url)
                #print("req headers     = %s   " % response.request.headers)
                #print("req body        = %s   " % response.request.body)
                print("resp status code= %s   " % response.status_code)
                print("resp text       = %s \n" % response.text)
            
            return_value = response 
                       
        except requests.ConnectionError as pe:
            # TODO: some handling here, for now just print pe
            print('when a request to the odk api was made, the following error was raised %s' % (pe))
            return_value = None
        
        return return_value
    
class _Submissions(object):

    def __init__(self, odk_api):
        self.api = odk_api

    def list(self, form_id, verbose=False):
        """
        list submissions per form-id
        """
        url = self.api.url + "/view/submissionList?formId=%s" % form_id
        response = self.api.utils.request(url=url, request_type='get', verbose=verbose)
        
        return response

    def get_data(self, form_id, group_name, uuid, verbose=False):
        """
        retrieve data of a particular submission per form-id
        reply = requests.get((base_format % {'form_id': form_id,
                                                 'api': 'downloadSubmission',
                                                 'host': host} +
                                  submission_format % {'group_name': 'CRF99-ImageTest',
                                                       'uuid': uuid}), auth=auth)
        base_format = 'https://%(host)s/view/%(api)s?formId=%(form_id)s'
        submission_format = '[@version=null and @uiVersion=null]/%(group_name)s[@key=%(uuid)s]'
        """
        url = self.api.url + "/view/downloadSubmission?formId=%s[@version=null and @uiVersion=null]/%s[@key=%s]" % (form_id, group_name, uuid)
        response = self.api.utils.request(url=url, request_type='get', verbose=verbose)
        
        return response

    