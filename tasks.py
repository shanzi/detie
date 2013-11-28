#!/usr/bin/env python
# encoding: utf-8


from invoke import task

@task
def test_ci():
    print "Test Success"
