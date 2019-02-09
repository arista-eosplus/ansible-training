# Exercise 3.2 - Generating Spine/Leaf Switch Config using EOS Roles
# Sample BGP/MLAG/Varp Playbook

1) Install the needed roles by creating a text file:
```
sudo ansible-galaxy install -r newroles.yml
```
The above command will install the need roles required to run the play book.

2) The playbook can be executed by running:

```
ansible-playbook -i hosts site.yml
```

The ```site.yml``` playbook is divided into to two child playbooks ```spine.yml``` and ```leaf.yml```.  As their name implies ```spine.yml``` will run against hosts in the `spines` group and ```leaf.yml``` will run against hosts in the `leafs` group.

To feed the correct IP addresses/username into the play change the requisite host_vars/ or group_vars/ file to meet your needs.

For example if my host file looks like this:

```
[spines]
spine1 ansible_host=<ip address>
spine2 ansible_host=<ip address>

[leafs]
leaf1 ansible_host=<ip address>
leaf2 ansible_host=<ip address>
```

If I needed to change the IP address that will be configured on spine1 I would edit the ```host_vars/spine1``` file.
