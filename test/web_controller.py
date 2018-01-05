'''
Created on 20 de jan de 2016

@author: Diego
'''
import time
from telnetlib import EC

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.select import Select
#from telnetlib import EC
#from selenium.webdriver import DesiredCapabilities
#from logilab.common import configuration
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#from selenium.webdriver.common.keys import Keys



class DjangoWebTest:

    web_controller = None
    project_url = "http://127.0.0.1:8000/"
    temp = {}

    def __init__(self):
        self.web_controller = WebController()
        #self.load_page(self.project_url)

    def change_password(self, email, password, new_password, confirm_password):
        self.login(email,password)
        while self.get_title() != 'SistemaWeb - Perfil do Usuário':
            time.sleep(1)
            self.web_controller.click('field_user')
            self.web_controller.click('profile')
        self.web_controller.enter_text('old_password', password)
        self.web_controller.enter_text('password', new_password)
        self.web_controller.enter_text('confirm_password', confirm_password)
        self.web_controller.click('button_send')

    def add_entity (self, cpf_cnpj, entity_name, birth_date_foundation,fantasy_name ,observation):
        while self.get_title() != 'SistemaWeb - Base Page':
            time.sleep(1)
        self.web_controller.click('button_menu_entidade')
        self.web_controller.click('button_submenu_entidade')
        while self.get_title() != 'SistemaWeb - Cadastrar Entidade':
            time.sleep(1)
        time.sleep(4)
        self.web_controller.click('bt_identification')
        self.web_controller.enter_text('cpf_cnpj',cpf_cnpj)
        self.web_controller.enter_text('entity_name', entity_name)
        self.web_controller.enter_text('fantasy_name', fantasy_name)
        self.web_controller.enter_text('birth_date_foundation', birth_date_foundation)
        self.web_controller.enter_text('observation', observation)
        time.sleep(4)
        self.web_controller.click('submit_entity')



    def change_password_behave (self, password ,new_password, confirm_password):
        while self.get_title() != 'SistemaWeb - Perfil do Usuário':
            time.sleep(1)
            self.web_controller.click('field_user')
            self.web_controller.click('profile')
        self.web_controller.enter_text('old_password', password)
        self.web_controller.enter_text('password', new_password)
        self.web_controller.enter_text('confirm_password', confirm_password)
        self.web_controller.click('button_send')

    def register(self, email, password, confirm_password):
        self.web_controller.load_page(self.project_url+'register')
        digitar_email = self.web_controller.enter_text('email', email)
        digitar_password = self.web_controller.enter_text('password', password)
        digitar_confirm_password = self.web_controller.enter_text('confirm_password', confirm_password)
        clicar_enviar = self.web_controller.click('button_register')

        preencher_formulario = digitar_email and digitar_password and digitar_confirm_password
        if preencher_formulario and clicar_enviar:
            pass

    def login(self, email, password):
        self.web_controller.enter_text('email', email)
        self.web_controller.enter_text('password', password)
        self.web_controller.click('button_send')

    def logout(self):
        time.sleep(3)
        self.web_controller.click('field_user')
        self.web_controller.click('logout')

    def delete_user (self, email):
        self.load_page('http://127.0.0.1:8000/api/user/register/delete/'+email)

    def check_error_notify(self):
        component = self.web_controller.get_component(By.CLASS_NAME,'alert-danger')
        if component is not None:
            return component.text
        else:
            return None

    def check_error_form(self):
        component = self.web_controller.get_component(By.CLASS_NAME,'alert')
        print(component)
        if component is not None:
            return component.text
        else:
            return None

    def get_title(self):
        return self.web_controller.get_title()

    def load_page(self,url):
        if "http://" not in url:
            url = "http://" + url
        self.web_controller.load_page(url)

    def close(self):
        self.web_controller.close()


class WebController:

    controle_componentes  = None
    link = None
    driver = None
    component = None
    
    def __init__(self,extensoes=[]):
        self.load_controllers(extensoes)

    def get_title(self):
        return self.driver.title

    def load_page(self, url):
        self.driver.get(url)
        try:
            pass
        except:
            print("Falha no carregamento da pagina: ",url)
            self.close()
        
    def maximize_window(self):
        self.driver.maximize_window()
    
    def load_controllers(self, extensoes=[]):
        binary = FirefoxBinary(settings.MOZILLA_FIREFOX_TEST_PATH)
        capabilities = webdriver.DesiredCapabilities().FIREFOX
        """FirefoxOptions
        options = new
        FirefoxOptions();
        options.addPreference("--log", "error");
        """
        capabilities["marionette"] = True

        try:
            self.driver = webdriver.Firefox(firefox_binary=binary,executable_path=settings.SELENIUM_GECKODRIVER_MOZILLA,capabilities=capabilities)
            #self.driver.maximize_window()


            """ Especificando extensoes
            profile = webdriver.FirefoxProfile()
            for item in extensoes:
                profile.add_extension(extension=item)
            self.driver = webdriver.Firefox(firefox_profile=profile) """
            
            """ Carregar Mozilla Simples """

            
        except:
            print("Navegador nao pode ser aberto. Pode ser necessario atualiza-lo antes.")
            exit(0)

    def get_component(self, metodo, valor):
        global EC
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        wait = WebDriverWait(self.driver, 5)
        try:
            element = wait.until(EC.element_to_be_clickable((metodo,valor)))
            return element
        except:
            
            time.sleep(2)
            try:
                self.component = self.driver.find_element(metodo, valor)
                return self.component
            except:
                #print "Busca por elemento excedeu o tempo maximo.",valor
                return None
    
    def select(self, identificador, opcao):
        self.component = self.get_component(By.ID, identificador)
        if self.component != None:
            Select(self.component).select_by_value(opcao)
            return True
        return False
        
    def click(self, identificador):
        self.component = self.get_component(By.ID, identificador)
        if self.component is not None:
            try:
                self.component.click()
                return True
            except:
                #print "Erro! Componente nao pode ser clicado.."
                return False
        return False
    
    def enter_text(self, identificador, texto):
        self.component = self.get_component(By.ID, identificador)
        if self.component != None:
            self.component.send_keys(texto)
            return True
        return False
        
    def clear_field(self, identificador):
        self.component = self.get_component(By.ID, identificador)
        if self.component != None:
            self.component.clear()
            return True
        return False
    
    def print_screen(self,path):
        self.driver.save_screenshot(path)

    def wait(self, time):
        time.sleep(time)

    def iniciar(self, url):
        self.link = url
        self.load_page(url)

    def close(self):
        self.driver.close()
        try:
            alert = self.controlador.driver.switch_to_alert()
            alert.accept()

        except:
            pass

        time.sleep(1)
        try:
            alert = self.controlador.driver.switch_to_alert()
            alert.accept()
        except:
            pass
