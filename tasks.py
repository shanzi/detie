#!/usr/bin/env python
# encoding: utf-8
import os, sys

from invoke import Collection, task, ctask, run as _run
import detie
from detie import logger
import requests

try:
    import private_keys as pk
except Exception, e:
    pk = {}


def run(cmd, hide=None ,*args, **kwargs):
        
    if not hide:
        sys.stdout.write("\x1b[2;38;5;230m")
        print cmd
        sys.stdout.write("\x1b[2;38;5;236m")
        sys.stdout.flush()
        r = _run(cmd, hide=hide, *args, **kwargs)
        sys.stdout.write("\x1b[0m")
        sys.stdout.flush()
    else:
        r = _run(cmd, hide=hide, *args, **kwargs)
    return r


@task
def update_repo():
    logger.info("Checking repo status")
    status = run('git status --porcelain')
    if status.ok:
        if status.stdout.strip() == '':
            r = run('git push')
            if r.ok: return
            else: logger.error("Failed to push repo")
        else:
            logger.error("Please commit or stash your changes before deploy")
    else:
        logger.error("Failed to get git repo status")
    exit(1)

@task
def sync_data():
    local_data_dir = os.path.abspath(pk.LOCAL_DATA_DIR)
    password_file = os.path.abspath(pk.RSYNC_PWD_FILE)
    rsync_cmd = "rsync -avzP %s %s --password-file %s" % (local_data_dir, pk.RSYNC_PATH, password_file)
    logger.info("Syncing data files")
    result = run(rsync_cmd, hide=None)
    if not result.ok:
        logger.error('Failed to sync data files')

@task(pre=['update_repo', 'sync_data'])
def deploy():
    logger.info("Trigger building")
    r = requests.get(pk.BUILD_TRIGGER_URL)
    if r.status_code < 200 or r.status_code >= 300:
        logger.error('Trigger building failed')

@task
def score():
    detie.score()
    

@task
def train_bayes(force=False):
    detie.train_bayes(force)

@task(default=True)
def build():
    detie.run()
