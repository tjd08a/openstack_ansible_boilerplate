__author__ = 'james'
# Last modified: 10/14/2015
# Description: Creates a sample OpenStack instance then configures it using Ansible
import time
from novaclient import client
from credentials import get_nova_creds


# Wait for an OpenStack instance to change from an inputted status
# instance_reference is the reference to the instance obtained by using the nova.servers.find method
# status_name is the status from which the instance should change from e.g. BUILD
def wait_for_status_change(instance_reference, status_name):
    instance = nova.servers.get(instance_reference)
    status = instance.status
    while status == status_name:
        time.sleep(5)
        instance = nova.servers.get(instance_reference)
        status = instance.status
    return

# Waits until an instance with the given name is deleted.
# instance_name is the name of the OpenStack instance to be deleted.
def wait_for_deletion(instance_name):
    # If the server exists, delete so a new one can be created
    server_found = nova.servers.findall(name=instance_name)
    while len(server_found) != 0:
        current_instance = nova.servers.find(name=instance_name)
        current_instance.delete()
        time.sleep(5)
        server_found = nova.servers.findall(name=instance_name)
    return

# Configuration variables for the instance, they may be changed.
instance_name = "My First Instance"
keypair_name = "My First Keypair"
image_name = "CloudVM"
flavor_name = "m1.small"

# ID of NIC to use for instance
# Obtain from Horizon API, needed if multiple networks present
net_id='2e69f0be-6b14-44d4-b3ea-705114e0d4e7'

# Get credentials for OpenStack, these are obtained by going to the Horizon Console
# See credentials.py for more about this.
creds = get_nova_creds()
# Passes the credentials along with a version of the client to use
nova = client.Client('2',**creds)

wait_for_deletion(instance_name)

key = nova.keypairs.get(keypair_name)
image = nova.images.find(name=image_name)
print nova.images.list()
flavor = nova.flavors.find(name=flavor_name)
print nova.flavors.list()
print nova.networks.list()

nics = [{"net-id": net_id, "v4-fixed-ip":""}]
nova.servers.create(name=instance_name,
                    flavor=flavor,
                    key_name=keypair_name,
                    image=image,
                    nics=nics)

instance_reference = nova.servers.find(name=instance_name)
wait_for_status_change(instance_reference, "BUILD")
ip_addresses = nova.servers.ips(instance_reference)
ip_addr = None
for interface in ip_addresses:
   ip_list = ip_addresses[interface]
   ip_addr = ip_list[0]['addr']
   break



