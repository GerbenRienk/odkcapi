import requests
import json
from collections import OrderedDict


class OdkCentralApi(object):

    def __init__(self, url):
        self.url = url
        self.headers = {"Content-Type": "application/json"}        
        self.utils = _Utils(self)
        self.sessions = _Sessions(self)
        self.participants = _Participants(self)
        self.events = _Events(self)
        self.projects = _Projects(self)
        self.forms = _Forms(self)
        self.submissions =_Submissions(self)

class _Utils(object):

    def __init__(self, odk_central_api):
        self.api = odk_central_api

    def request(self, data=None, request_type=None, url=None, headers=None, params=None, files=None, verbose=False):
        """
        Return the result of an API call, or None.

        Exceptions are logged rather than raised.

        Parameters
        :param data: Method name and parameters to send to the API.
        :type data: String
        :param url: Location of the endpoint.
        :type url: String
        :param headers: HTTP headers to add to the request.
        :type headers: Dict
        :param request_type: either post or get
        Return
        :return: Dictionary containing result of API call, or None.
        """
        if url is None:
            url = self.api.url
        if headers is None:
            headers = self.api.headers
        return_value = None
        try:
            if verbose == True:
                print("p url=     %s   " % url)
                print("p params=  %s   " % params)
                print("p headers= %s   " % headers)
                print("p data=    %s   " % data)
                print("p type=    %s \n" % request_type)
            
            if request_type == 'post':
                response = requests.post(url, params=params, headers=headers, data=data, files=files)
                
            if request_type == 'get':
                response = requests.get(url, params=params, headers=headers, data=data)
            
            if request_type == 'put':
                response = requests.put(url, params=params, headers=headers, data=data)
            
            if request_type == 'delete':
                response = requests.delete(url, params=params, headers=headers, data=data)
            
            if verbose == True:
                print("req url         = %s   " % response.request.url)
                print("req headers     = %s   " % response.request.headers)
                print("req body        = %s   " % response.request.body)
                print("resp status code= %s   " % response.status_code)
                print("resp text       = %s \n" % response.text)
            
            return_value = response 
                       
        except requests.ConnectionError as pe:
            # TODO: some handling here, for now just print pe
            print('when a request to the odk-central api was made, the following error was raised %s' % (pe))
            return_value = None
        
        return return_value
    
    def is_jsonable(self, x):
        try:
            json.dumps(x)
            return True
        except:
            return False
        
    @staticmethod
    def prepare_params(method, params):
        """
        Prepare remote procedure call parameter dictionary.

        Important! Despite being provided as key-value, the API treats all
        parameters as positional. OrderedDict should be used to ensure this,
        otherwise some calls may randomly fail.

        Parameters
        :param method: Name of API method to call.
        :type method: String
        :param params: Parameters to the specified API call.
        :type params: OrderedDict

        Return
        :return: JSON encoded string with method and parameters.
        """
        data = OrderedDict([
            ('method', method),
            ('params', params),
            ('id', 1)
        ])
        data_json = json.dumps(data)
        return data_json

class _Sessions(object):

    def __init__(self, odk_central_api):
        self.api = odk_central_api

    def get_authentication_token(self, username, password, verbose=False):
        """
        Get an access token for all subsequent API calls.
        
        """
        token_data = '{"email":"%s" , "password":"%s"}' % (username, password)
        aut_url = self.api.url + "/v1/sessions"
        headers = self.api.headers
        
        response = self.api.utils.request(data=token_data, request_type='post', url=aut_url, headers=headers, verbose=verbose)
        if response.status_code == 200:
            # we got a json-response
            token_info = json.loads(response.text)
            return_value = token_info['token']
        else:
            print('authentication request to %s returned status code %i' % (url, response.status_code))
            return_value = None
        
        return return_value

class _Projects(object):

    def __init__(self, odk_central_api):
        self.api = odk_central_api

    def list_projects(self, aut_token, verbose=False):
        projects_url = self.api.url + "/v1/projects"
        bearer = "Bearer " + aut_token
        headers = {"Authorization": bearer}
        
        response = self.api.utils.request(request_type='get', url=projects_url, headers=headers, verbose=verbose)
        if response.status_code == 200:
            # we got a json-response
            project_info = json.loads(response.text)
            
            return_value = project_info
        else:
            print('projects request to %s returned status code %i' % (projects_url, response.status_code))
            return_value = None
        
        return return_value
        
        return None
class _Forms(object):

    def __init__(self, odk_central_api):
        self.api = odk_central_api

    def list_forms(self, aut_token, project_id, verbose=False):
        forms_url = self.api.url + "/v1/projects/" + project_id + "/forms"
        bearer = "Bearer " + aut_token
        headers = {"Authorization": bearer}
        
        response = self.api.utils.request(request_type='get', url=forms_url, headers=headers, verbose=verbose)
        if response.status_code == 200:
            # we got a json-response
            forms_info = json.loads(response.text)
            return_value = forms_info
        else:
            print('forms request to %s returned status code %i' % (url, response.status_code))
            return_value = None
        
        return return_value
        
        return None

class _Submissions(object):

    def __init__(self, odk_central_api):
        self.api = odk_central_api

    def list_submissions(self, aut_token, project_id, form_id, verbose=False):
        submissions_url = self.api.url + "/v1/projects/" + project_id + "/forms/" + form_id + "/submissions"
        bearer = "Bearer " + aut_token
        headers = {"Authorization": bearer}
        
        response = self.api.utils.request(request_type='get', url=submissions_url, headers=headers, verbose=verbose)
        if response.status_code == 200:
            # we got a json-response
            project_info = json.loads(response.text)
            #project_info = response.text
            return_value = project_info
        else:
            print('submissions request to %s returned status code %i' % (submissions_url, response.status_code))
            return_value = None
        
        return return_value
        
        return None

class _Participants(object):

    def __init__(self, odk_central_api):
        self.api = odk_central_api

    def list_participants(self, study_oid, aut_token, verbose=False):
        """
        List participants per study and/or per site
        /pages/auth/api/clinicaldata/studies/{studyOID}/participants
        Parameters
        :param study_oid: study_oid
        :type session_key: String
        :param aut_token: aut_token
        :type username: String
        """
        url = self.api.url + "/pages/auth/api/clinicaldata/studies/" + study_oid + "/participants"
        bearer = "bearer " + aut_token
        headers = {"Authorization": bearer}
        complete_response = self.api.utils.request_2(url=url, headers=headers, request_type='get', verbose=verbose)
        # pass only the main part: 
        response=json.loads(complete_response)
        return response['studyParticipants']

    def add_participant(self, study_oid, site_oid, study_subject_id, aut_token, verbose=False):
        """
        Add a participants to a study / site
        POST {serverName}/pages/auth/api/clinicaldata/studies/{studyOID}/sites/{siteOID}/participants
        Parameters
        :param study_oid: study_oid
        :type study_oid: String
        """
        url = self.api.url + "/pages/auth/api/clinicaldata/studies/" + study_oid + "/sites/" + site_oid + "/participants"
        params = {"register":"n"}
        bearer = "bearer " + aut_token
        headers = {"accept":"*/*","Content-Type": "application/json", "Authorization": bearer}
        
        data = json.dumps({"subjectKey" : study_subject_id})
        #submit request
        response = self.api.utils.request_2(url=url, params=params, headers=headers, request_type='post', data=data, verbose=verbose)
           
        return response

    def bulk_add_participants(self, study_oid, site_oid, files, aut_token):
        """
        Add participants to a study using a csv-file
        POST {serverName}/pages/auth/api/clinicaldata/studies/{studyOID}/sites/{siteOID}/participants/bulk
        Parameters
        :param study_oid: study_oid
        :type study_oid: String
        :param files: the csv-file-location 
        :type username: files = {'file': ('report.xls', open('report.xls', 'rb')}
        Header should contain: content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
        """
        url = self.api.url + "/pages/auth/api/clinicaldata/studies/" + study_oid + "/sites/" + site_oid + "/participants/bulk?register=n"
        bearer = "bearer " + aut_token
        headers = {"content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW", "Authorization": bearer}
        response = self.api.utils.request_2(url=url, headers=headers, request_type='post', verbose=True, files=files)
                
        return response

class _Events(object):

    def __init__(self, odk_central_api):
        self.api = odk_central_api

    def schedule_event(self, study_oid, site_oid, event_info, aut_token, verbose=False):
        """
        Schedule one events
        """
        url = self.api.url + "/pages/auth/api/clinicaldata/studies/" + study_oid + "/sites/" + site_oid + "/events"
        
        bearer = "bearer " + aut_token
        headers = {"accept":"*/*","Content-Type": "application/json", "Authorization": bearer}
        
        data = json.dumps(event_info)
        #submit the request
        result = self.api.utils.request(url=url, headers=headers, request_type='post', data=data, verbose=verbose)
        # hopefully the request resulted in status code 200, which is fine for us, but also 400 is good
        if(result.status_code == 200 or result.status_code == 400):
            result = None
        # if this is not the case something went wrong, so we just return whatever the response was
         
        return result

    def update_event(self, study_oid, site_oid, event_info, aut_token, verbose=False):
        """
        Change an event
        """
        url = self.api.url + "/pages/auth/api/clinicaldata/studies/" + study_oid + "/sites/" + site_oid + "/events"
        
        bearer = "bearer " + aut_token
        headers = {"accept":"*/*","Content-Type": "application/json", "Authorization": bearer}
        
        data = json.dumps(event_info)
        #submit the request
        result = self.api.utils.request(url=url, headers=headers, request_type='put', data=data, verbose=verbose)
        # hopefully the request resulted in status code 200, which is fine for us, but also 400 is good
        #if(result.status_code == 200 or result.status_code == 200):
            #result = None
        # if this is not the case something went wrong, so we just return whatever the response was
         
        return result

    def check_events(self, study_oid, aut_token, verbose=False):
        """
        It's a mystery what this end-point does, but it's in the swagger, so we leave it for now
        """
        url = self.api.url + "/pages/auth/api/%s/events/check" % study_oid 
        bearer = "bearer " + aut_token
        headers = {"accept":"*/*","Content-Type": "application/json", "Authorization": bearer}
        #submit the request
        result = self.api.utils.request(url=url, headers=headers, request_type='get', verbose=verbose)
        return result






