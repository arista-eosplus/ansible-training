# Exercise 3.2 - Generating Spine/Leaf Switch Config using EOS Roles

In this lab we will use the Arista created Roles on Ansible Galaxy to build out a Spine - Leaf configuration.


#### Step 1

First we will need to install the needed roles. Let's do this by creating a new file `newroles.yml` to install them all in one command. Add the following lines to `newroles.yml` so that it looks like the output below.

``` shell
[arista@ansible ansible-training]$ cat newroles.yml
- src: arista.eos-bgp
- src: arista.eos-bridging
- src: arista.eos-interfaces
- src: arista.eos-ipv4
- src: arista.eos-mlag
- src: arista.eos-route-control
- src: arista.eos-system
- src: arista.eos-virtual-router
- src: arista.eos-vxlan
[arista@ansible ansible-training]$
```

The following command will install the roles referenced in `newroles.yml` required to configure our site switches.

```
ansible-galaxy install -r newroles.yml
```

Run the command:

``` shell
[arista@ansible ansible-training]$ ansible-galaxy install -r newroles.yml
- downloading role 'eos-bgp', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-bgp/archive/v2.1.8.tar.gz
- extracting arista.eos-bgp to /home/arista/.ansible/roles/arista.eos-bgp
- arista.eos-bgp (v2.1.8) was installed successfully
- downloading role 'eos-bridging', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-bridging/archive/v2.1.8.tar.gz
- extracting arista.eos-bridging to /home/arista/.ansible/roles/arista.eos-bridging
- arista.eos-bridging (v2.1.8) was installed successfully
- downloading role 'eos-interfaces', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-interfaces/archive/v2.1.8.tar.gz
- extracting arista.eos-interfaces to /home/arista/.ansible/roles/arista.eos-interfaces
- arista.eos-interfaces (v2.1.8) was installed successfully
- downloading role 'eos-ipv4', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-ipv4/archive/v2.1.8.tar.gz
- extracting arista.eos-ipv4 to /home/arista/.ansible/roles/arista.eos-ipv4
- arista.eos-ipv4 (v2.1.8) was installed successfully
- downloading role 'eos-mlag', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-mlag/archive/v2.1.8.tar.gz
- extracting arista.eos-mlag to /home/arista/.ansible/roles/arista.eos-mlag
- arista.eos-mlag (v2.1.8) was installed successfully
- downloading role 'eos-route-control', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-route-control/archive/v2.1.8.tar.gz
- extracting arista.eos-route-control to /home/arista/.ansible/roles/arista.eos-route-control
- arista.eos-route-control (v2.1.8) was installed successfully
- downloading role 'eos-system', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-system/archive/v2.1.8.tar.gz
- extracting arista.eos-system to /home/arista/.ansible/roles/arista.eos-system
- arista.eos-system (v2.1.8) was installed successfully
- downloading role 'eos-virtual-router', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-virtual-router/archive/v2.1.8.tar.gz
- extracting arista.eos-virtual-router to /home/arista/.ansible/roles/arista.eos-virtual-router
- arista.eos-virtual-router (v2.1.8) was installed successfully
- downloading role 'eos-vxlan', owned by arista
- downloading role from https://github.com/arista-eosplus/ansible-eos-vxlan/archive/v2.1.8.tar.gz
- extracting arista.eos-vxlan to /home/arista/.ansible/roles/arista.eos-vxlan
- arista.eos-vxlan (v2.1.8) was installed successfully
[arista@ansible ansible-training]$
```

Let's run another ansible-galaxy command to view our installed roles.

``` shell
[arista@ansible ansible-training]$ ansible-galaxy list
- arista.eos-vxlan, v2.1.8
- arista.eos-bridging, v2.1.8
- arista.eos-mlag, v2.1.8
- arista.eos-interfaces, v2.1.8
- arista.eos-system, v2.1.8
- ansible-network.network-engine, v2.7.3
- arista.eos-ipv4, v2.1.8
- arista.eos-route-control, v2.1.8
- arista.eos-virtual-router, v2.1.8
- arista.eos-bgp, v2.1.8
[arista@ansible ansible-training]$
```

All roles from our `newroles.yml` file are listed in addition to the `ansible-network.network-engine` role we installed in the previous lab.


#### Step 2


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
