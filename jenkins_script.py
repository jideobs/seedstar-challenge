#!/usr/bin/env python

import sys
import json
import requests
import optparse
import sqlite3
from datetime import datetime

DB_NAME = 'jenkins_job_status.db'
USAGE = 'usage: jenkins_script.py [OPTIONS]... [URL]...'
JOBS_PATH = '{instance_url}/api/json?tree=jobs[name]'
STATUS_PATH = '{instance_url}/job/{job_name}/lastBuild/api/json?tree=result,building'

OPTIONS = None


def get_data(url):
    if OPTIONS:
        user = OPTIONS.user.split(':')
        r = requests.get(url, auth=tuple(user))
    else:
        r = requests.get(url)

    return json.loads(r.content)


def get_jobs(url):
    resp = get_data(url)
    return resp.get('jobs')


def get_job_status(url):
    resp = get_data(url)
    result = resp.get('result')
    building = resp.get('building')
    if building:
        result = 'RUNNING'
    return result


def save_job_status(instance_url, job_name, job_status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("CREATE TABLE jobs (instance, job, status, date_checked)")
    except sqlite3.OperationalError:
        # table already created
        pass

    query = ("INSERT INTO jobs VALUES ('{instance}', '{job}', '{status}', '{date_checked}')"
             .format(instance=instance_url, job=job_name, status=job_status, date_checked=datetime.utcnow()))
    c.execute(query)
    conn.commit()
    conn.close()


def main(instance_url):
    job_url = JOBS_PATH.format(instance_url=instance_url)
    jobs = get_jobs(job_url)

    for job in jobs:
        job_name = job['name']
        status_url = STATUS_PATH.format(instance_url=instance_url, job_name=job_name)
        job_status = get_job_status(status_url)
        save_job_status(instance_url, job_name, job_status)
        print 'Just saved status for %s' % job_name


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    parser.add_option('-u', '--user', dest='user', metavar='USER',
                      help='Enter authentication details for instance USER:PASSWD')
    OPTIONS, args = parser.parse_args()
    if len(args) < 1:
        print 'jenkins_script: missing instance url'
        parser.print_help()
        sys.exit()
    instance = args[0]
    main(instance)
