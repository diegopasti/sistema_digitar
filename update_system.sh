echo 'INICIALIZANDO ATUALIZA��O'
#service redis-server stop                 --> Encerra o servi�o se houver esse comando.
#sudo fuser -k 8000/tcp                    --> Encerra o servi�o associado a uma porta especifica.
#ps aux | grep -i manage                   --> Encerra o servi�o que tem o label manage.
#pkill -f "python manage.py runserver"     --> Encerra o servi�o pelo comando que o criou.
#python manage.py

source /home/django/PythonEnvs/sistema_digitar/bin/activate
python manage.py install_packages

#service redis-server start                --> Inicializa o servi�o pelo nome
#python manage.py runserver 0.0.0.0:8000   --> Inicializa pelo comando
echo 'ATUALIZA��O REALIZADA COM SUCESSO'

