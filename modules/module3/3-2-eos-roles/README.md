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


For this lab we will separate configurations of different device types into different playbooks. We will also need to provide a large number of parameters to our group_vars/ and host_vars/ that will be used by the newly installed roles to configure the switches.

First lets set up a new hosts file that will work with a limited number of our devices. Let's create this new hosts file as `hosts_for_eos_roles`.

``` shell
[arista@ansible ansible-training]$ cat inventory/hosts_for_eos_roles
[spines]
spine1 ansible_host=192.168.0.10
spine2 ansible_host=192.168.0.11

[leafs]
leaf1 ansible_host=192.168.0.14
leaf2 ansible_host=192.168.0.15
[arista@ansible ansible-training]$
```

Using this new hosts file we will only be working with two spines and two leafs.

Next let's some new group_vars/ needed for configuring our site.

Within group_vars/ create a new file named `all` and add the following:

``` shell
[arista@ansible ansible-training]$ cat inventory/group_vars/all
---
# Connection to the devices
provider:
  host: '{{ ansible_host }}'
  username: arista
  password: arista
  use_ssl: false
  transport: eapi
  validate_certs: false

eos_users:
  - name: newexampleuser
    nopassword: true
    privilege: 0
    role: network-operator
[arista@ansible ansible-training]$
```

The `provider` variables added will be used by Ansible for connection to the switches. The `provider` is the old method of connecting to network devices before Ansible 2.5. The current EOS roles still require the old connection method so we will provide the necessary variables here.

We've also added variables for a new user. These variables will be used by the `arista.eos-system` role to add a new user `newexampleuser` to all devices.

Next let's add two new files in group_vars/ one for the `leafs` group and one for the `spines` group as shown below.

``` shell
[arista@ansible ansible-training]$ cat inventory/group_vars/leafs
---
eos_purge_vlans: no
eos_ip_routing_enabled: yes
[arista@ansible ansible-training]$
```

``` shell
[arista@ansible ansible-training]$ cat inventory/group_vars/spines
---
eos_purge_vlans: no
eos_ip_routing_enabled: yes
[arista@ansible ansible-training]$
```

These two files are currently the same. Both containing the `eos_ip_routing_enabled` variable that is set to enabling IP routing on the switch and `eos_purge_vlans` that is set for preventing the new configurations done by the `arista.eos-bridging` role from removing extra vlans found in the configuration not associated with variables. If we later need to add additional configuration variables for all `leafs` or all `spines`, we have these group_vars/ files to add them too.

Next we will add or update four of our host_vars/ files.

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine1
---
hostname: dc1-spine1
[arista@ansible ansible-training]$
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine2
---
hostname: dc1-spine2
[arista@ansible ansible-training]$
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf1
---
hostname: dc1-leaf1
[arista@ansible ansible-training]$
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf2
---
hostname: dc1-leaf2
[arista@ansible ansible-training]$
```

In these host_vars/ files we have provided a unique hostname variable that the `arista.eos-system` role will use to configure the hostname on the respective device.


#### Step 3


Now that we have our initial set of connection, group and host variables set, let's create our playbooks.

First create a playbook for the `spines` group called `spine.yml` and add the following:

``` yaml
---
- hosts: spines
  gather_facts: no
  connection: local

  roles:
    - arista.eos-system

```

Next lets create a playbook for the `leafs` group called `leaf.yml` and add the following:

``` yaml
---
- hosts: leafs
  gather_facts: no
  connection: local

  roles:
    - arista.eos-system

```

So far both of these playbooks look almost the same, both executing the `arista.eos-system` role. The only difference is the `hosts` statement which specifies the group of devices the playbook will work on. As we continue building out the configurations these two playbooks will differ more.

Instead of having to execute these two playbook separately, let's create one more playbook name `site.yml` and add the following:

``` yaml
---
- include: spine.yml
- include: leaf.yml

```

This playbook is using the Ansible `include` statement to execute both our `spine.yml` and `leaf.yml` playbooks in one shot.

Now with all our initial variables set and playbooks created, let's run the playbook `site.yml`.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts_for_eos_roles site.yml

PLAY [spines] *************************************************************************************************************************

TASK [arista.eos-system : set_fact] ***************************************************************************************************
skipping: [spine1]
skipping: [spine2]

TASK [arista.eos-system : Gather EOS configuration] ***********************************************************************************
ok: [spine1]
ok: [spine2]

TASK [arista.eos-system : Save EOS configuration] *************************************************************************************
ok: [spine1]
ok: [spine2]

TASK [arista.eos-system : Include the Arista EOS System resources] ********************************************************************
included: /home/arista/.ansible/roles/arista.eos-system/tasks/resources2.2.yml for spine1, spine2

TASK [arista.eos-system : Arista EOS Hostname resources (Ansible >= 2.2)] *************************************************************
changed: [spine1]
changed: [spine2]

TASK [arista.eos-system : Arista EOS IP Routing resources (Ansible >= 2.2)] ***********************************************************
ok: [spine1]
ok: [spine2]

TASK [arista.eos-system : Arista EOS CLI User resources (Ansible >= 2.2)] *************************************************************
changed: [spine1] => (item=None)
changed: [spine1]
changed: [spine2] => (item=None)
changed: [spine2]

TASK [arista.eos-system : Gather EOS configuration] ***********************************************************************************
ok: [spine1]
ok: [spine2]

TASK [arista.eos-system : Save EOS configuration] *************************************************************************************
ok: [spine1]
ok: [spine2]

RUNNING HANDLER [arista.eos-system : save running config] *****************************************************************************
ok: [spine1]
ok: [spine2]

PLAY [leafs] **************************************************************************************************************************

TASK [arista.eos-system : set_fact] ***************************************************************************************************
skipping: [leaf1]
skipping: [leaf2]

TASK [arista.eos-system : Gather EOS configuration] ***********************************************************************************
ok: [leaf1]
ok: [leaf2]

TASK [arista.eos-system : Save EOS configuration] *************************************************************************************
ok: [leaf1]
ok: [leaf2]

TASK [arista.eos-system : Include the Arista EOS System resources] ********************************************************************
included: /home/arista/.ansible/roles/arista.eos-system/tasks/resources2.2.yml for leaf1, leaf2

TASK [arista.eos-system : Arista EOS Hostname resources (Ansible >= 2.2)] *************************************************************
changed: [leaf2]
changed: [leaf1]

TASK [arista.eos-system : Arista EOS IP Routing resources (Ansible >= 2.2)] ***********************************************************
ok: [leaf1]
ok: [leaf2]

TASK [arista.eos-system : Arista EOS CLI User resources (Ansible >= 2.2)] *************************************************************
changed: [leaf1] => (item=None)
changed: [leaf1]
changed: [leaf2] => (item=None)
changed: [leaf2]

TASK [arista.eos-system : Gather EOS configuration] ***********************************************************************************
ok: [leaf1]
ok: [leaf2]

TASK [arista.eos-system : Save EOS configuration] *************************************************************************************
ok: [leaf1]
ok: [leaf2]

RUNNING HANDLER [arista.eos-system : save running config] *****************************************************************************
ok: [leaf2]
ok: [leaf1]

PLAY RECAP ****************************************************************************************************************************
leaf1                      : ok=9    changed=2    unreachable=0    failed=0
leaf2                      : ok=9    changed=2    unreachable=0    failed=0
spine1                     : ok=9    changed=2    unreachable=0    failed=0
spine2                     : ok=9    changed=2    unreachable=0    failed=0

[arista@ansible ansible-training]$

```

The `arista.eos-system` role made a couple changes for all of our devices. This is what we would expect being that we added a new user into our group_vars/all variables file and gave each device a custom hostname in their unique host_vars/ file.

Let's connect to spine1 to see the changes on the switch.

``` shell
[arista@ansible ansible-training]$ ssh arista@192.168.0.10
dc1-spine1#show run | include username
... <some output omitted> ...
username newexampleuser privilege 0 role network-operator nopassword
dc1-spine1#
[arista@ansible ansible-training]$
```
 You should see the new hostname `dc1-spine` and the `newexampleuser` configured.

 Now let's try running this same playbook again. Remember that Ansible modules/roles should be idempotent when they can, meaning that they only make changes when necessary.

 ``` shell
 [arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts_for_eos_roles site.yml

PLAY [spines] *************************************************************************************************************************

... <some output omitted> ...

PLAY [leafs] **************************************************************************************************************************

... <some output omitted> ...

PLAY RECAP ****************************************************************************************************************************
leaf1                      : ok=6    changed=0    unreachable=0    failed=0
leaf2                      : ok=6    changed=0    unreachable=0    failed=0
spine1                     : ok=6    changed=0    unreachable=0    failed=0
spine2                     : ok=6    changed=0    unreachable=0    failed=0

 [arista@ansible ansible-training]$

 ```

 Notice that the roles are idempotent because the devices are already in the state expected by the configured variables.


#### Step 4



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
