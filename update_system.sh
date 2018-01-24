echo 'INICIALIZANDO ATUALIZAÇÃO'
#service redis-server stop                 --> Encerra o serviço se houver esse comando.
#sudo fuser -k 8000/tcp                    --> Encerra o serviço associado a uma porta especifica.
#ps aux | grep -i manage                   --> Encerra o serviço que tem o label manage.
#pkill -f "python manage.py runserver"     --> Encerra o serviço pelo comando que o criou.
#python manage.py

source /home/django/PythonEnvs/sistema_digitar/bin/activate
python manage.py install_packages

#service redis-server start                --> Inicializa o serviço pelo nome
#python manage.py runserver 0.0.0.0:8000   --> Inicializa pelo comando
echo 'ATUALIZAÇÃO REALIZADA COM SUCESSO'

