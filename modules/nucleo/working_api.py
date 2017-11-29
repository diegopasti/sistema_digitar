import project_properties
from django.conf import settings
from django.http import HttpResponse
import requests
import json


class WorkingApi:
    setup_file = settings.WORKING_CONFIGURATION
    server_api = settings.WORKING_SERVER+"/api/work/register"
    user_key = None
    project_key = None
    working_key = None
    task_id = None

    def get_working_key(self):
        config = project_properties.working_paramters#json.loads(open(settings.WORKING_CONFIGURATION).read())
        self.user_key = config['user_key']
        self.project_key = config['project_key']
        self.task_id = config['task']

        if config:
            self.working_key = config['project_key'] + "&" + config['user_key'] + "&" + config['task']
        else:
            self.working_key = None
        return self.working_key

    def save(self, tipo, request_page=None):
        headers = {'content-type': 'application/json'}
        data = {"tipo":tipo, "request_page": request_page, "working_key": self.get_working_key()}
        response = requests.get(self.server_api, data, headers=headers).json()
        data = json.dumps(response)
        return HttpResponse(data, content_type='application/json')


class WorkingManager():

    def register(self,tag,request_page=None):
        workin_api = WorkingApi()
        response = workin_api.save(tag,request_page)
        if response.status_code == 200:
            response_data = json.loads(response.content.decode())
            if response_data['success'] == True:
                data = response_data['data']['date']
                user = response_data['data']['user_name']
                project = response_data['data']['project_name']
                print(data + " > WorkingApi was updated -", user, "working on", project, )
            else:
                print("WorkingApi not update!")
        else:
            print("WorkingApi not Running at moment.")

        return response


    def register_programming_backend(self):
        return self.register(tag="PROG-BACK")

    def register_programming_frontend(self, page):
        return self.register(tag="PROG-FRONT",request_page=page)

    def register_test_backend(self):
        return self.register(tag="TEST-BACK")

