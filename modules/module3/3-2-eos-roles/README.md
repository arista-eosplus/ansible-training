# Exercise 3.2 - Generating Spine/Leaf Switch Config using EOS Roles

In this lab we will use the Arista created Roles on Ansible Galaxy to build out a Spine - Leaf site configuration.


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
```

The `provider` variables added will be used by Ansible for connection to the switches. The `provider` is the old method of connecting to network devices before Ansible 2.5. The current EOS roles still require the old connection method so we will provide the necessary variables here.

We've also added variables for a new user. These variables will be used by the `arista.eos-system` role to add a new user `newexampleuser` to all devices.

Next let's add two new files in group_vars/ one for the `leafs` group and one for the `spines` group as shown below.

``` shell
[arista@ansible ansible-training]$ cat inventory/group_vars/leafs
---
eos_purge_vlans: no
eos_ip_routing_enabled: yes
```

``` shell
[arista@ansible ansible-training]$ cat inventory/group_vars/spines
---
eos_purge_vlans: no
eos_ip_routing_enabled: yes
```

These two files are currently the same. Both containing the `eos_ip_routing_enabled` variable that is set to enabling IP routing on the switch and `eos_purge_vlans` that is set for preventing the new configurations done by the `arista.eos-bridging` role from removing extra vlans found in the configuration not associated with variables. If we later need to add additional configuration variables for all `leafs` or all `spines`, we have these group_vars/ files to add them too.

Next we will add or update four of our host_vars/ files.

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine1
---
hostname: dc1-spine1
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine2
---
hostname: dc1-spine2
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf1
---
hostname: dc1-leaf1
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf2
---
hostname: dc1-leaf2
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
... <output omitted for brevity> ...
username newexampleuser privilege 0 role network-operator nopassword
dc1-spine1#
[arista@ansible ansible-training]$
```
 You should see the new hostname `dc1-spine` and the `newexampleuser` configured.

 Now let's try running this same playbook again. Remember that Ansible modules/roles should be idempotent when they can, meaning that they only make changes when necessary.

 ``` shell
 [arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts_for_eos_roles site.yml

PLAY [spines] *************************************************************************************************************************

... <output omitted for brevity> ...

PLAY [leafs] **************************************************************************************************************************

... <output omitted for brevity> ...

PLAY RECAP ****************************************************************************************************************************
leaf1                      : ok=6    changed=0    unreachable=0    failed=0
leaf2                      : ok=6    changed=0    unreachable=0    failed=0
spine1                     : ok=6    changed=0    unreachable=0    failed=0
spine2                     : ok=6    changed=0    unreachable=0    failed=0

 [arista@ansible ansible-training]$
 ```

 Notice that the roles are idempotent because the devices are already in the state expected by the configured variables.


#### Step 4


Now let's add some more substantial configurations to the switches in our site and use more of the `arista.eos` roles.

Update each of the host_vars/ files as shown below:

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine1
---
hostname: dc1-spine1

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: production

interfaces:
  - name: Loopback0
    enable: true
  - name: Loopback1
    enable: true
  - name: Ethernet2
    description: '[BGP]Connection to Leaf1'
    enable: true
  - name: Ethernet3
    description: '[BGP]Connection to Leaf2'
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.1/32
  - name: Loopback1
    address: 2.2.2.1/32
  - name: Ethernet2
    address: 10.1.1.0/31
  - name: Ethernet3
    address: 10.1.1.2/31
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine2
---
hostname: dc1-spine2

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: production

interfaces:
  - name: Loopback0
    enable: true
  - name: Loopback1
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to Leaf1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to Leaf2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.2/32
  - name: Loopback1
    address: 2.2.2.2/32
  - name: Ethernet2
    address: 10.1.2.0/31
  - name: Ethernet3
    address: 10.1.2.2/31
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf1
---
hostname: dc1-leaf1

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: app2

interfaces:
  - name: Loopback0
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to spine1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to spine2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.10/32
  - name: Ethernet2
    address: 10.1.1.1/31
  - name: Ethernet3
    address: 10.1.2.1/31
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf2
---
hostname: dc1-leaf2

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: production

interfaces:
  - name: Loopback0
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to spine1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to spine2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.11/32
  - name: Ethernet2
    address: 10.1.1.3/31
  - name: Ethernet3
    address: 10.1.2.3/31
```

With these additional variables added for each device we can see that there will be a couple of vlans configured per switch and several interfaces configured for IPv4 connections. To speed up this lab I am including a mapping of what configuration variables apply to what role here.

vlans - `arista.eos-bridging`
interfaces - `arista.eos-interfaces`
ip_interfaces - `arista.eos-ipv4`

Since these there variable sections have been added to all of our host_vars/ lets add these roles to our `spine.yml` and `leaf.yml` playbooks.

``` yaml
---
- hosts: spines
  gather_facts: no
  connection: local

  roles:
    - arista.eos-system
    - arista.eos-bridging
    - arista.eos-interfaces
    - arista.eos-ipv4
```

``` yaml
---
- hosts: leafs
  gather_facts: no
  connection: local

  roles:
    - arista.eos-system
    - arista.eos-bridging
    - arista.eos-interfaces
    - arista.eos-ipv4
```

At this point our playbooks are still almost the same. Let's run the updated playbook.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts_for_eos_roles site.yml

PLAY [spines] *************************************************************************************************************************

... <output omitted for brevity> ...

PLAY [leafs] **************************************************************************************************************************

... <output omitted for brevity> ...

TASK [arista.eos-interfaces : Arista EOS interface resources (Ansible >= 2.2)] ********************************************************
changed: [leaf2] => (item={u'enable': True, u'name': u'Loopback0'})
changed: [leaf1] => (item={u'enable': True, u'name': u'Loopback0'})
changed: [leaf2] => (item={u'enable': True, u'name': u'Ethernet2', u'description': u'[BGP]Connection to spine1'})
changed: [leaf1] => (item={u'enable': True, u'name': u'Ethernet2', u'description': u'[BGP]Connection to spine1'})
changed: [leaf2] => (item={u'enable': True, u'name': u'Ethernet3', u'description': u'[BGP]Connection to spine2'})
changed: [leaf1] => (item={u'enable': True, u'name': u'Ethernet3', u'description': u'[BGP]Connection to spine2'})

TASK [arista.eos-ipv4 : set_fact] *****************************************************************************************************
skipping: [leaf1]
skipping: [leaf2]

TASK [arista.eos-ipv4 : Gather EOS configuration] *************************************************************************************
skipping: [leaf1]
skipping: [leaf2]

TASK [arista.eos-ipv4 : Save EOS configuration] ***************************************************************************************
skipping: [leaf1]
skipping: [leaf2]

TASK [arista.eos-ipv4 : Include the Arista EOS IPv4 resources] ************************************************************************
included: /home/arista/.ansible/roles/arista.eos-ipv4/tasks/resources2.2.yml for leaf1, leaf2

TASK [arista.eos-ipv4 : Arista EOS IPv4 resources (Ansible >= 2.1)] *******************************************************************
changed: [leaf2] => (item={u'name': u'Loopback0', u'address': u'1.1.1.11/32'})
changed: [leaf1] => (item={u'name': u'Loopback0', u'address': u'1.1.1.10/32'})
changed: [leaf2] => (item={u'name': u'Ethernet2', u'address': u'10.1.1.3/31'})
changed: [leaf1] => (item={u'name': u'Ethernet2', u'address': u'10.1.1.1/31'})
changed: [leaf2] => (item={u'name': u'Ethernet3', u'address': u'10.1.2.3/31'})
changed: [leaf1] => (item={u'name': u'Ethernet3', u'address': u'10.1.2.1/31'})

RUNNING HANDLER [arista.eos-system : save running config] *****************************************************************************
ok: [leaf2]
ok: [leaf1]

PLAY RECAP ****************************************************************************************************************************
leaf1                      : ok=13   changed=3    unreachable=0    failed=0
leaf2                      : ok=13   changed=3    unreachable=0    failed=0
spine1                     : ok=13   changed=3    unreachable=0    failed=0
spine2                     : ok=13   changed=3    unreachable=0    failed=0

[arista@ansible ansible-training]$
```

With all of these roles and configs there is a lot of output. You can filter through this to see all the expected changes and log into the switches to view them.

Once again running the playbook a second time does not make any changes because of the roles are idempotent.


#### Step 5


Our next step will be to add some variables to configure a static route and BGP on each switch. Update each devices host_vars/ file as shown below:

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine1
---
hostname: dc1-spine1

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: production

interfaces:
  - name: Loopback0
    enable: true
  - name: Loopback1
    enable: true
  - name: Ethernet2
    description: '[BGP]Connection to Leaf1'
    enable: true
  - name: Ethernet3
    description: '[BGP]Connection to Leaf2'
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.1/32
  - name: Loopback1
    address: 2.2.2.1/32
  - name: Ethernet2
    address: 10.1.1.0/31
  - name: Ethernet3
    address: 10.1.1.2/31

ipv4_static_routes:
  - ip_dest: 0.0.0.0/0
    next_hop: Management1
    next_hop_ip: 172.16.130.2
    route_name: Default
    tag: 100

bgp:
  enable: true
  bgp_as: 65001
  redistribute:
    - connected
  log_neighbor_changes: yes
  timers:
    keep_alive: 1
    hold: 3
  neighbors:
    - name: 10.1.1.1
      remote_as: 65002
      peer_group: demoleaf
      enable: true
    - name: 10.1.1.3
      remote_as: 65002
      peer_group: demoleaf
      enable: true
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/spine2
---
hostname: dc1-spine2

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: production

interfaces:
  - name: Loopback0
    enable: true
  - name: Loopback1
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to Leaf1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to Leaf2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.2/32
  - name: Loopback1
    address: 2.2.2.2/32
  - name: Ethernet2
    address: 10.1.2.0/31
  - name: Ethernet3
    address: 10.1.2.2/31

ipv4_static_routes:
  - ip_dest: 0.0.0.0/0
    next_hop: Management1
    next_hop_ip: 172.16.130.2
    route_name: Default
    tag: 100

bgp:
  enable: true
  bgp_as: 65001
  redistribute:
    - connected
  log_neighbor_changes: yes
  timers:
    keep_alive: 1
    hold: 3
  neighbors:
    - name: 10.1.2.1
      remote_as: 65002
      peer_group: demoleaf
      enable: true
    - name: 10.1.2.3
      remote_as: 65002
      peer_group: demoleaf
      enable: true
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf1
---
hostname: dc1-leaf1

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: app2

interfaces:
  - name: Loopback0
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to spine1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to spine2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.10/32
  - name: Ethernet2
    address: 10.1.1.1/31
  - name: Ethernet3
    address: 10.1.2.1/31

ipv4_static_routes:
  - ip_dest: 0.0.0.0/0
    next_hop: Management1
    next_hop_ip: 172.16.130.2
    route_name: Default
    tag: 100

bgp:
  enable: true
  bgp_as: 65002
  redistribute:
    - connected
  log_neighbor_changes: yes
  timers:
    keep_alive: 1
    hold: 3
  listeners:
    - name: 10.1.0.0/16
      peer_group: demoleaf
      remote_as: 65001
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf2
---
hostname: dc1-leaf2

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: production

interfaces:
  - name: Loopback0
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to spine1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to spine2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.11/32
  - name: Ethernet2
    address: 10.1.1.3/31
  - name: Ethernet3
    address: 10.1.2.3/31

ipv4_static_routes:
  - ip_dest: 0.0.0.0/0
    next_hop: Management1
    next_hop_ip: 172.16.130.2
    route_name: Default
    tag: 100

bgp:
  enable: true
  bgp_as: 65002
  redistribute:
    - connected
  log_neighbor_changes: yes
  timers:
    keep_alive: 1
    hold: 3
  listeners:
    - name: 10.1.0.0/16
      peer_group: demoleaf
      remote_as: 65001
```

The new sections variable to role mappings are shown below:

ipv4_static_route - `arista.eos-route-control`
bgp - `arista.eos-bgp`

Since these there variable sections have been added to all of our host_vars/ lets add these roles to our `spine.yml` and `leaf.yml` playbooks.

``` yaml
---
- hosts: spines
  gather_facts: no
  connection: local

  roles:
    - arista.eos-system
    - arista.eos-bridging
    - arista.eos-interfaces
    - arista.eos-ipv4
    - arista.eos-route-control
    - arista.eos-bgp
```

``` yaml
---
- hosts: leafs
  gather_facts: no
  connection: local

  roles:
    - arista.eos-system
    - arista.eos-bridging
    - arista.eos-interfaces
    - arista.eos-ipv4
    - arista.eos-route-control
    - arista.eos-bgp
```

Let's run the updated playbook.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts_for_eos_roles site.yml

PLAY [spines] *************************************************************************************************************************

... <output omitted for brevity> ...

PLAY [leafs] **************************************************************************************************************************

... <output omitted for brevity> ...

PLAY RECAP ****************************************************************************************************************************
leaf1                      : ok=20   changed=3    unreachable=0    failed=0
leaf2                      : ok=20   changed=3    unreachable=0    failed=0
spine1                     : ok=23   changed=4    unreachable=0    failed=0
spine2                     : ok=23   changed=4    unreachable=0    failed=0

[arista@ansible ansible-training]$
```

With all of these roles and configs there is a lot of output. You can filter through this to see all the expected changes and log into the switches to view them.

Once again running the playbook a second time does not make any changes because of the roles are idempotent.


#### Step 6


For our final step we will add some additional configurations that will only apply to our leaf switches. Update the leaf switches host_vars files as shown below:

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf1
---
hostname: dc1-leaf1

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: app2

interfaces:
  - name: Loopback0
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to spine1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to spine2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.10/32
  - name: Ethernet2
    address: 10.1.1.1/31
  - name: Ethernet3
    address: 10.1.2.1/31

ipv4_static_routes:
  - ip_dest: 0.0.0.0/0
    next_hop: Management1
    next_hop_ip: 172.16.130.2
    route_name: Default
    tag: 100

bgp:
  enable: true
  bgp_as: 65002
  redistribute:
    - connected
  log_neighbor_changes: yes
  timers:
    keep_alive: 1
    hold: 3
  listeners:
    - name: 10.1.0.0/16
      peer_group: demoleaf
      remote_as: 65001

mlag:
    mlag_domain_id: mlag1
    mlag_trunk_group: mlagpeer
    mlag_shutdown: false
    local_if_vlan: Vlan1024
    local_if_ip_address: 10.0.0.1/30
    local_if_disable_spanning_tree: true
    peer_address: 10.0.0.2
    peer_link_if: Port-Channel10
    peer_link_mode: trunk
    peer_link_lacp_mode: active
    peer_link_enable: true
    peer_link_members:
      - Ethernet1

virtual_mac_addr: "00:1c:73:00:00:99"

varp_interfaces:
  - vlanid: 1001
    name: Varp_Vlan1001
    description: My Vlan1001
    enable: true
    interface_addr: 192.168.1.3/24
    virtual_addrs:
      - 192.168.1.1
  - vlanid: 1002
    name: Varp_Vlan1002
    description: My Vlan1001
    enable: true
    interface_addr: 192.168.2.3/24
    virtual_addrs:
      - 192.168.2.1
```

``` shell
[arista@ansible ansible-training]$ cat inventory/host_vars/leaf2
---
hostname: dc1-leaf2

vlans:
  - vlanid: 1
    name: default
  - vlanid: 2
    name: production

interfaces:
  - name: Loopback0
    enable: true
  - name: Ethernet2
    description: "[BGP]Connection to spine1"
    enable: true
  - name: Ethernet3
    description: "[BGP]Connection to spine2"
    enable: true

ip_interfaces:
  - name: Loopback0
    address: 1.1.1.11/32
  - name: Ethernet2
    address: 10.1.1.3/31
  - name: Ethernet3
    address: 10.1.2.3/31

ipv4_static_routes:
  - ip_dest: 0.0.0.0/0
    next_hop: Management1
    next_hop_ip: 172.16.130.2
    route_name: Default
    tag: 100

bgp:
  enable: true
  bgp_as: 65002
  redistribute:
    - connected
  log_neighbor_changes: yes
  timers:
    keep_alive: 1
    hold: 3
  listeners:
    - name: 10.1.0.0/16
      peer_group: demoleaf
      remote_as: 65001

mlag:
    mlag_domain_id: mlag1
    mlag_trunk_group: mlagpeer
    mlag_shutdown: false
    local_if_vlan: Vlan1024
    local_if_ip_address: 10.0.0.2/30
    local_if_disable_spanning_tree: true
    peer_address: 10.0.0.1
    peer_link_if: Port-Channel10
    peer_link_mode: trunk
    peer_link_lacp_mode: active
    peer_link_enable: true
    peer_link_members:
      - Ethernet1

virtual_mac_addr: "00:1c:73:00:00:99"

varp_interfaces:
  - vlanid: 1001
    name: Varp_Vlan1001
    description: My Vlan1001
    enable: true
    interface_addr: 192.168.1.4/24
    virtual_addrs:
      - 192.168.1.1
  - vlanid: 1002
    name: Varp_Vlan1002
    description: My Vlan1001
    enable: true
    interface_addr: 192.168.2.4/24
    virtual_addrs:
      - 192.168.2.1
```

The new sections variable to role mappings are shown below:

mlag - `arista.eos-mlag`
virtual_mac_addr - `arista.eos-virtual-router`
varp_interfaces - `arista.eos-virtual-router`

Since these variable sections have only been added to the leaf switches host_vars/ lets add these roles to the `leaf.yml` playbook.

``` yaml
---
- hosts: leafs
  gather_facts: no
  connection: local

  roles:
    - arista.eos-system
    - arista.eos-bridging
    - arista.eos-interfaces
    - arista.eos-ipv4
    - arista.eos-route-control
    - arista.eos-bgp
    - arista.eos-mlag
    - arista.eos-virtual-router
```

Let's run our playbook one more time to complete our full site configuration.

``` shell
[arista@ansible ansible-training]$ ansible-playbook -i inventory/hosts_for_eos_roles site.yml

PLAY [spines] *************************************************************************************************************************

... <output omitted for brevity> ...

PLAY [leafs] **************************************************************************************************************************

... <output omitted for brevity> ...

PLAY RECAP ****************************************************************************************************************************
leaf1                      : ok=26   changed=6    unreachable=0    failed=0
leaf2                      : ok=26   changed=6    unreachable=0    failed=0
spine1                     : ok=18   changed=0    unreachable=0    failed=0
spine2                     : ok=18   changed=0    unreachable=0    failed=0

[arista@ansible ansible-training]$
```

After this most recent run only the leaf switches have changes. Connect to one of the leaf switches and execute a `show mlag` to verify the feature is operational.

We have just used Ansible to configure multiple features across a full site. With our variables set and simple playbooks that leverage pre-built roles we can configure or verify the configuration of a full site of devices.


# Complete

You have completed lab exercise 3.2

---
