#!/usr/bin/env python
# encoding: utf-8
import os

from invoke import Collection, task
from invoke.context import Context

try:
    import private_keys as pk
except Exception, e:
    pk = {}

ctx = Context(run={'hide':'both'})

def abort(text, code=1):
    print "\x1b[31;1mAbort: \x1b[0m%s [%d]" %  (text, code)
    exit(code)

def warning(text):
    print "\x1b[33;1mWarning: \x1b[0m%s" %  text

def info(text):
    print "\x1b[34;1mInfo: \x1b[0m%s" %  text

@task
def update_repo():
    status = ctx.run('git status --porcelain')
    if status.ok:
        if status.stdout.strip() == '':
            ctx.run('git push')
        else:
            abort("Please commit or stash your changes before deploy")
    else:
        abort("Failed to get git repo status")

@task
def sync_data():
    local_data_dir = os.path.abspath(pk.LOCAL_DATA_DIR)
    password_file = os.path.abspath(pk.RSYNC_PWD_FILE)
    rsync_cmd = "rsync -avzP %s %s --password-file %s" % (local_data_dir, pk.RSYNC_PATH, password_file)
    info("Syncing data files")
    result = ctx.run(rsync_cmd, hide=None)
    if not result.ok:
        abort('Failed to sync data files')

@task(pre=['update_repo', 'sync_data'])
def deploy():
    pass
