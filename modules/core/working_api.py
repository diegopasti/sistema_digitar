from django.http import HttpResponse
import project_properties
import requests
import json

from sistema_contabil.settings import WORKING_SERVER


class WorkingApi:

    #print(dir(settings))
    setup_file = project_properties.working_paramters
    server_api = WORKING_SERVER + "/api/work/register"
    user_key = None
    project_key = None
    working_key = None
    task_id = None

    def get_working_key(self):
        config = self.setup_file
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
        try:
            response = requests.get(self.server_api, data, headers=headers).json()
        except:

            response = {'success':False,'message':'Server not enable.'}
        data = json.dumps(response)
        return HttpResponse(data, content_type='application/json')


class WorkingManager:

    def register(self,tag,request_page=None):
        working_api = WorkingApi()
        response = working_api.save(tag, request_page)
        if response.status_code == 200:
            response_data = json.loads(response.content.decode())
            if response_data['success'] == True:
                data = response_data['data']['date']
                user = response_data['data']['user_name']
                project = response_data['data']['project_name']
                print(data + " > WorkingApi was updated -", user, "working on", project, )
            else:
                print("WorkingApi not update! "+response_data['message'])
        return response

    def register_programming_backend(self):
        return self.register(tag="PROG-BACK")

    def register_programming_frontend(self, page):
        return self.register(tag="PROG-FRONT",request_page=page)

    def register_test_front(self):
        #print("TEM QUE REGISTRAR QUE VOU RODAR O TEST DE FRONT")
        return self.register(tag="TEST-FRONT")

    def register_test_backend(self):
        return self.register(tag="TEST-BACK")

