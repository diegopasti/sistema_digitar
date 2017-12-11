from dulwich import porcelain
from dulwich.repo import Repo
import os

LOCAL_REPO = os.getcwd()
REMOTE_REPO = 'https://github.com/diegopasti/sistema_digitar'
HEADS = '.git\\refs\\heads\\master'


def check_update():
    data = {}
    ref = Repo('.')
    local_ref = ref.head().decode('utf-8')
    print('Versão local: ', local_ref)
    remote_commit = porcelain.ls_remote(REMOTE_REPO)[b"HEAD"].decode('utf-8')
    print('\nVersão remota: ', remote_commit)
    data['local'] = local_ref
    data['remote'] = remote_commit
    print(data)
    #log = porcelain.log(LOCAL_REPO)
    #print(log)
    #changes = porcelain.get_tree_changes(LOCAL_REPO)
    #print(changes)
    #status = porcelain.status(LOCAL_REPO)
    #print(status)
    #r = porcelain.fetch(LOCAL_REPO,REMOTE_REPO)
    #print(r)
    if local_ref != remote_commit:
        print('\nNOVA VERSÃO DISPONÍVEL,INSTALANDO...\n')
        #update()
    else:
        pass
        print('\nVC JÁ ESTÁ COM A ÚLTIMA VERSÃO INSTALADA.')


    return data
        
def update():

    try:
        porcelain.pull(LOCAL_REPO, REMOTE_REPO)
        print('\nOPERAÇÃO REALIZADA COM SUCESSO...')
    except:
        pass
        try:
            os.remove(HEADS)
            porcelain.pull(LOCAL_REPO, REMOTE_REPO)
            print('\nOPERAÇÃO REALIZADA COM SUCESSO...')
        except:
            pass
        

if __name__ == '__main__':
    import sys
    arguments = sys.argv
    if "update" in arguments:
        check_update()
