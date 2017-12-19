from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.porcelain import tag_list
from datetime import datetime,timedelta
import time
import os

LOCAL_REPO = os.getcwd()
REMOTE_REPO = 'https://github.com/diegopasti/sistema_digitar'
HEADS = '.git\\refs\\heads\\master'
MASTER = '.git\\refs\\remotes\\HEAD'


def check_update():
    data = {}
    repo = Repo('.')
    local_ref = repo.head().decode('utf-8')
    print('Versão local: ', local_ref)
    remote_commit = porcelain.ls_remote(REMOTE_REPO)[b"HEAD"].decode('utf-8')
    print('\nVersão remota: ', remote_commit)

    with porcelain.open_repo_closing(repo) as r:
        walker = r.get_walker(max_entries=1)
        for entry in walker:
            message = str(entry.commit.message)[2:-3]
            author = str(entry.commit.author)
            if message.startswith('Merge'):
                continue

    stamp = datetime.utcfromtimestamp(entry.commit.commit_time)
    delta = timedelta(hours=2)
    last_update = (stamp - delta).strftime('%d/%m/%Y'+' ás '+'%H:%M:%S')
    data['local'] = local_ref
    data['remote'] = remote_commit
    data['last_update'] = last_update
    print(data)

    #tag_labels = tag_list(repo)
    #print(tag_labels)
    #for i in ref.get_walker(include=[local_ref]):
        #print(i)
    #import git
    #repo = git.Repo(".")
    #tree = repo.tree()
    #for blob in tree:
        #commit = next(repo.iter_commits(paths=blob.path, max_count=1))
        #print(blob.path, commit.author, commit.committed_date)

    #path = sys.argv[0].encode('utf-8')

    #w = ref.get_walker(paths=[path], c = next(iter(w)).commit)
    #try:
        #c = next(iter(w)).commit
    #except StopIteration:
        #print("No file %s anywhere in history." % sys.argv[0])
    #else:
        #print("%s was last changed by %s at %s (commit %s)" % (
            #sys.argv[1], c.author, time.ctime(c.author_time), c.id))

    #log = porcelain.log('.', max_entries=1)
    #print(log)
    #log = porcelain.log(LOCAL_REPO)
    #print(log)
    #changes = porcelain.get_tree_changes(LOCAL_REPO)
    #print(changes)
    #status = porcelain.status(LOCAL_REPO)
    #print(status)
    #r = porcelain.fetch(LOCAL_REPO,REMOTE_REPO)
    #print(r)
    #for i in r:
        #print(i)
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