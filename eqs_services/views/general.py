import json
import socket
from flask import Blueprint, render_template, request
from resource_manager.client import ResourceManagerClient

from config import RM_ENDPOINT

machine_views = Blueprint('general', __name__)


@machine_views.route('/')
def index():
    client = ResourceManagerClient(endpoint=RM_ENDPOINT)
    machines = client.get_all_resources()

    available_machines = []
    used_machines = []
    pxe_failed = []
    error_state = []

    for machine in machines:
        addr = socket.getaddrinfo(machine['hostname'], 22, socket.AF_INET, socket.IPPROTO_IP, socket.IPPROTO_TCP)[0]
        machine.update({'ip': str(addr[4][0])})

        if machine['state'] == "in_use":
            used_machines.append(machine)
        elif machine['state'] == "idle":
            available_machines.append(machine)
        elif machine['state'] == "pxe_failed":
            pxe_failed.append(machine)
        else:
            error_state.append(machine)
    total_machines = len(machines)

    return render_template('general/index.html',
                           machines=machines,
                           total_machines=total_machines,
                           available_machines=len(available_machines),
                           used_machines=len(used_machines),
                           pxe_failed=len(pxe_failed))


@machine_views.route('/machines')
def machines():
    client = ResourceManagerClient(endpoint=RM_ENDPOINT)
    machines = client.get_all_resources()
    machine_list = []

    state = request.args.get('state')
    if not state:
        state = "all"

    for machine in machines:
        addr = socket.getaddrinfo(machine['hostname'], 22, socket.AF_INET, socket.IPPROTO_IP, socket.IPPROTO_TCP)[0]
        machine.update({'ip': str(addr[4][0])})

        if state == "all":
            machine_list.append(machine)
        elif state == machine['state']:
            machine_list.append(machine)
    return render_template("general/machines.html", machines=machine_list)


def get_current_jobs():
    client = ResourceManagerClient(endpoint=RM_ENDPOINT,
                                     resource_type='machines')
    jobs = []
    machines = client.get_all_resources()
    for machine in machines:
        if machine['job_id'] and machine['job_id'] not in jobs:
            jobs.append(machine['job_id'])
    return jobs


@machine_views.route('/addresses')
def addresses():

    state = request.args.get('state')
    if not state:
        state = "all"

    client = ResourceManagerClient(endpoint=RM_ENDPOINT,
                                   resource_type='public-addresses')
    all_ips = client.get_all_resources()
    available_ips = client.find_resources(field="owner", value="")

    jobs = get_current_jobs()
    zombie_ips = []

    for ip in all_ips:
        if ip['owner'] and ip['owner'] not in jobs:
            ip.update({'temp_state': 'zombie'})
            zombie_ips.append(ip)

    if state == "zombie":
        ips = zombie_ips
    else:
        ips = all_ips

    return render_template("general/ipaddresses.html",
                           total_pub_ips=len(all_ips),
                           available_ips=len(available_ips),
                           zombie_ips=len(zombie_ips),
                           ips=ips)
