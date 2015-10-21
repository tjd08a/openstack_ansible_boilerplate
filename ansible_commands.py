__author__ = 'james'
#!/usr/bin/python
import ansible.runner
import ansible.playbook
import ansible.inventory
import json
import os.path
from ansible import callbacks
from ansible import utils

def setup_host(host_ip, private_key):
    key_path = os.path.expanduser('~/.ssh')
    key_path += "/" + private_key
    print host_ip
    ansible_host = ansible.inventory.host.Host(
        name = host_ip,
        port = 22
    )
    ansible_host.set_variable('ansible_ssh_user','ubuntu')
    ansible_host.set_variable('ansible_ssh_private_key_file', key_path)
    print key_path

    group = ansible.inventory.group.Group(
        name = 'openstack'
    )

    print ansible_host.groups
    group.add_host(ansible_host)

    sample_inventory = ansible.inventory.Inventory()
    sample_inventory.add_group(group)
    print sample_inventory.groups_list()
    return sample_inventory

def run_playbook(inventory, playbook):
    utils.VERBOSITY = 4
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
    pb = ansible.playbook.PlayBook(
        playbook = playbook,
        stats = stats,
        callbacks = playbook_cb,
        runner_callbacks = runner_cb,
        inventory = inventory,
        check=True
    )

    pr = pb.run()
    print json.dumps(pr, sort_keys=True, indent=4)

    return