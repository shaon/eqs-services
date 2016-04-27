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
    print state
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
