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

The ```site.yml``` playbook is divided into to two child playbooks ```spine.yml``` and ```leaf.yml```.  As their name implies ```spine.yml``` will run against hosts in the spine group and ```leaf.yml``` will run against hosts in the leaf group.

To feed the correct IP addresses/username into the play change the requisite host_var or group_var file to meet your needs.

For example if my host file looks like this:

```
[spine]
dc1-spine1
dc1-spine2

[leaf]
dc1-tora
dc1-torb
```

If I needed to change the IP address that will be configured on dc1-spine1 I would edit the ```host_vars/dc1-spine1``` file.
