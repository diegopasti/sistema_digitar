:: Desativa o eco de comando
@echo off

:: Limpa a tela
cls

:: Linha em branco
@echo.

:: Escreve na tela
@echo INICIALIZANDO ATUALIZACAO

:: Encerra serviço em uma porta especifica
FOR /F "tokens=5 delims= " %%P IN ('netstat -a -n -o ^| findstr :8000.*LISTENING') DO taskkill /F /PID %%P

:: linha em branco
::@echo.

::Ativar ambiente virtual (Diego)
::c:\users\diego\PythonVirtualEnvs\sistema_digitar\Scripts\activate.bat & cd C:\Users\diego\OneDrive\Projetos\sistema_digitar & python manage.py install_packages & python manage.py runserver 0.0.0.0:8000

::Ativar ambiente virtual (Lucas)
::c:\users\diego\PythonVirtualEnvs\sistema_digitar\Scripts\activate.bat & cd C:\Users\diego\OneDrive\Projetos\sistema_digitar & python manage.py install_packages & python manage.py runserver 0.0.0.0:8000
::Ativar ambiente virtual (Cleiton)
c:\users\helde\PythonVirtualEnvs\sistema_digitar\Scripts\activate.bat & cd C:\Users\helde\OneDrive\Projetos\sistema_digitar & python manage.py install_packages & python manage.py runserver 0.0.0.0:8000


:: aguarda uma tecla ser pressionada
::pause​
::@echo ATUALIZACAO REALIZADA COM SUCESSO



