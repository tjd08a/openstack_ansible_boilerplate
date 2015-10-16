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
    host = ansible.inventory.host.Host(
        name = host_ip,
        port = 22
    )
    host.set_variable('ansible_ssh_user','ubuntu')
    host.set_variable('ansible_ssh_private_key_file', key_path)

    group = ansible.inventory.group.Group(
        name = 'openstack'
    )

    sample_inventory = ansible.inventory.Inventory()
    sample_inventory.add_group(group)
    return sample_inventory

def run_playbook(inventory, playbook):
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
    pb = ansible.playbook.PlayBook(
        playbook = playbook,
        stats = stats,
        callbacks = playbook_cb,
        runner_callbacks = runner_cb,
        inventory = inventory,
        check = True

    )

    pr = pb.run()
    print json.dumps(pr, sort_keys=True, indent=4)

    return

    return