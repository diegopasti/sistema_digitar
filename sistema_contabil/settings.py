"""
Django settings for sistema_contabil project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import sys

import project_properties

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a33ryhl1tch=ql&a32o!+92%akmtem5%s7bhs_tj0#s3q$e4$%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
HTML_MINIFY = False
COMPRESS_ENABLED = True
COMPRESS_ROOT = os.path.join(BASE_DIR,"static/compress")

ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'sistema_contabil.urls'
WSGI_APPLICATION = 'sistema_contabil.wsgi.application'

'''LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}
'''

# Application definition
#AUTH_USER_MODEL = 'modules.user.User'
#AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles','session_security',
    'djangobower','compressor','dropbox','dbbackup',
    'sistema_contabil','modules','modules.nucleo','modules.user','modules.entidade','modules.protocolo','modules.honorary','modules.servico','modules.preferencias'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',


    #'django.middleware.cache.UpdateCacheMiddleware',
    #'htmlmin.middleware.HtmlMinifyMiddleware',
    # other middleware classes
    #'django.middleware.cache.FetchFromCacheMiddleware',
    #'htmlmin.middleware.MarkRequestMiddleware',
)

SESSION_SECURITY_EXPIRE_AFTER= 600
SESSION_SECURITY_WARN_AFTER= 540
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_INSECURE = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates/")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data/db.sqlite3'),
    }
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'data/backup')}
#DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
#DBBACKUP_STORAGE_OPTIONS = {'oauth2_access_token': '','root_path': '//data/'}
DBBACKUP_DATE_FORMAT = 'temp'#'%Y%m%d%H%M%S'
DBBACKUP_FILENAME_TEMPLATE = '{datetime}.{extension}' #'{datetime}.{extension}'
DBBACKUP_GPG_RECIPIENT = 'cleiton.leonel@gmail.com'
#DBBACKUP_GPG_ALWAYS_TRUST = 'True'
DROPBOX_OAUTH2_TOKEN = 'r2VjuxIaDQAAAAAAAAAAD7YKqJlAJSdXsRz3IWYGHs2Q_BEnim1nOc3-LA1PspKi'
#DROPBOX_OAUTH2_TOKEN = '4dM4LNuAHKAAAAAAAAAACCB_3-K_tIVlAFYwTBatxMlTd_e6Y5dyiEbR7uX1dKTJ'
DROPBOX_ROOT_PATH = '/backup'
ADM_DROPBOX = 'cleiton.creton@gmail.com'
KEY_DROPBOX = '98651597'

LANGUAGE_CODE = 'pt-br'
# NA MAQUINA DE DESENVOLVIMEMTO WINDWOS O HORARIO CORRETO DEVE UTILIZAR:
#TIME_ZONE = 'UTC'

# NO SERVIDOR LINUX DE PRODUCAO O HORARIO CORRETO DEVE UTILIZAR:
TIME_ZONE='America/Sao_Paulo'

#
# DEPOIS DA REFATORAcaO 2.0 PEDIU PRA COLOCAR ISSO
#
USE_TZ = True
USE_I18N = True
USE_L10N = True
#USE_TZ = True - Quando eu coloco isso a hora esta vindo com 3 horas a mais.

TIME_INPUT_FORMATS = [ '%H:%M', ]
USE_THOUSAND_SEPARATOR = True
# Static files (CSS, JavaScript, Images)


# https://docs.djangoproject.com/en/1.8/howto/static-files/
#LANGUAGE_CODE = 'pt-br'
#TIME_ZONE = 'America/Sao_Paulo'





"""
    STATIC_ROOT        
        
        O caminho absoluto para o diretorio onde ./manage.py collectstatic ira coletar os
        arquivos para implantacao. Exemplo: STATIC_ROOT = "/var/www/example.com/static/"
    
        agora o comando ./manage.py collectstatic ira copiar todos os arquivos estaticos (ou seja, na pasta de arquivos estaticos
        da aplicacao, arquivos estaticos em todos os caminhos) para a /var/www/example.com/static/ diretorio.
        agora voce so precisa servir este diretorio no Apache ou nginx..etc.
        

        
        
    STATIC_URL (Obrigatorio)
    
        O URL do qual os arquivos estaticos no diretorio STATIC_ROOT sao servidos (por Apache ou nginx..etc).
        Exemplo: /static/ ou http://static.example.com/

        Se voce definir STATIC_URL = 'http://static.example.com/', entao voce deve servir a pasta
        STATIC_ROOT (ou seja, "/var/www/example.com/static/") pela Apache ou nginx 
        na url 'http: //static.example.com/'(so que voce pode consultar o arquivo 
        estatico '/var/www/example.com/static/jquery.js' com 'http://static.example.com/jquery.js' )
        
        Agora em seus django-templates, voce pode submete-la por:
        {Load% staticfiles%}
        <Script src = "{% static" jquery.js "%}"> </ script>
        
        o que tornara:
        <Script src = "http://static.example.com/jquery.js"> </ script>.

"""


""" 
    Essa configuracao permite que os arquivos estaticos da pasta sejam carregadas, inclusive imagens.
    O pisa consegue carregar tanto os arquivos estaticos mas nao com desse jeito. Por algum motivo,
    ainda desconhecido, se estiver assim o pisa nao consegue ou encontrar ou renderizar o conteudo
    estatico de outros arquivos mas do outro jeito sim.
    
    - Tentei usar STATIC_URL mas parece nao ter funcionado.
    - Tentei retirar a formatacao da tag BODY tambem nao parece ter funcionado.
    
    Algumas ideias para manter essa configuracao:
    - Embutir o css na pagina que vai ser convertida. (Testado - Funciona!)
    - Utilizar o caminho absoluto das imagens ao inves de tentar carregar pelo static tag. (Funciona!)
      Nao consegui um meio de carregar o base_dir diretamente no template, entao eu pego ele na view 
      e passo pro template. 
    
"""
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = "/"
STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'sistemadigitar@gmail.com>'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sistemadigitar@gmail.com'
EMAIL_HOST_PASSWORD = 'd1g1t@r@dm1n'
EMAIL_PORT = 587

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    ("imagens", os.path.join(BASE_DIR, "/static/imagens")),
    
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
]

if sys.platform == 'linux':
    BOWER_PATH = '/usr/local/bin/bower'
else:
    if "lucas" in BASE_DIR:
        BOWER_PATH = 'C:/Users/lucas/AppData/Roaming/npm/bower.cmd'
    elif "helde" in BASE_DIR:
        BOWER_PATH = 'C:/Users/helde/AppData/Roaming/npm/bower.cmd'
    else:
        BOWER_PATH = 'C:/Users/diego/AppData/Roaming/npm/bower.cmd'

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')
BOWER_INSTALLED_APPS = (
    'jquery#2.2.0',
    'angular#1.6.4',
    'bootstrap',     #3.3.7',#3.3.2
    'jquery-ui',
    'font-awesome',  #4.7.0',#4.2
    'nprogress',
    'pnotify',
    'datatables.net-dt',
    'datatables.net-bs',
    'jquery-editable-select',
    'jquery-maskmoney',
    'angular-utils-pagination',
    'angular-locale-pt-br',
    'select2',
    'labelauty',
    'multiple-select',
    'jquery.maskedinput'


    #'bootstrap#3.3.7',#3.3.2
    #'font-awesome#4.7.0',#4.2
    #'angular#1.6.4',
    #'animate.css',
    #'gauge.js',
    #'chart.js',
    #'bootstrap-progressbar#0.9.0',
    #'jquery.nicescroll',
    #'moment',
    #"bootstrap-daterangepicker",
    #'fastclick',

    #'qunit',
    #'blanket',
    #'https://github.com/yairEO/validator.git',
    #'smartwizard',
    #'multiple-select', # PODE SER QUE NAO IREMOS USAR MAIS
    #'jQuery-Smart-Wizard#3.3.1',
    #'angular-utils-pagination',
    #'bootstrap-select',
    #'ng-filters-br'
)

"""
#FUNCIONAVA ANTIGAMENTE
STATIC_URL = '/arquivos_estaticos/'
STATIC_ROOT = os.path.join(BASE_DIR, 'arquivos_estaticos')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "arquivos_estaticos"),
    )
"""


"""
#FIZ ISSO PRA FUNCIONAR O PDF

STATIC_URL = '/arquivos_estaticos/'
STATIC_ROOT = os.path.join(BASE_DIR, 'arquivos_estaticos')

#STATIC_ROOT = os.path.join(BASE_DIR, '/arquivos_estaticos') - Quando ta assim tudo funciona, menos o pdf
#STATIC_ROOT = os.path.join(BASE_DIR, 'arquivos_estaticos') - Quando ta assim funciona o pdf.. o resto nao

MEDIA_URL = '/static/media/'   # isso faz diferenca
#MEDIA_ROOT = os.path.join(BASE_DIR, '/arquivos_estaticos/media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "/arquivos_estaticos"),
)
"""


FILER_DEBUG = True
FILER_ENABLE_LOGGING = True
FILER_CANONICAL_URL = 'sharing/'
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

SELENIUM_GECKODRIVER_MOZILLA = project_properties.geckodriver_path
MOZILLA_FIREFOX_TEST_PATH = project_properties.mozilla_firefox_path
#SELENIUM_CHROMEDRIVER = project_properties.chromedriver_path

SERVER_ADDRESS = "0.0.0.0:8020"
SERVER_DIGITAR = True
if SERVER_DIGITAR :
    WORKING_CONFIGURATION = os.path.join(BASE_DIR, 'conf/working.json')
    WORKING_SERVER = "http://127.0.0.1:8010"

    from modules.nucleo.working_api import WorkingManager


    try:
        if "runserver" in sys.argv:
            WorkingManager().register_programming_backend()

        elif "test" in sys.argv:
            WorkingManager().register_test_backend()

        else:
            pass

    except:
        pass