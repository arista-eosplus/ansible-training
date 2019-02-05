# Exercise 1.0 - Exploring the lab environment

## Step 1

Navigate to the `ansible-training` directory.


```
[arista@ansible ~]$ cd ansible-training/
[arista@ansible ansible-training]$
[arista@ansible ansible-training]$

```

## Step 2

Run the `ansible` command with the `--version` command to look at what is configured:


```
[arista@ansible ansible-training]$ ansible --version
ansible 2.7.1
  config file = /home/arista/ansible-training/ansible.cfg
  configured module search path = [u'/home/arista/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python2.7/dist-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 2.7.12 (default, Dec  4 2017, 14:50:18) [GCC 5.4.0 20160609]
[arista@ansible ansible-training]$


```

> Note: The Ansible version you see might differ from the above output


This command gives you information about the version of Ansible, location of the executable, version of Python, search path for the modules and location of the `Ansible configuration file`.

## Step 3

Use the `cat` command to view the contents of the `ansible.cfg` file.

```
[arista@ansible ansible-training]$ cat ansible.cfg
[defaults]
host_key_checking = False
deprecation_warnings = False
timeout = 60
connect_timeout = 60
command_timeout = 60
inventory = /home/arista/ansible-training/inventory/hosts
private_key_file = /home/arista/.ssh/id_rsa.pub
[arista@ansible ansible-training]$

```

Note the following parameters within the `ansible.cfg` file:

 - `inventory`: shows the location of the Ansible inventory being used
 - `private_key_file`: this shows the location of the private key used to login to devices



## Step 4

The scope of a `play` within a `playbook` is limited to the groups of hosts declared within an Ansible **inventory**. Ansible supports multiple [inventory](http://docs.ansible.com/ansible/latest/intro_inventory.html) types. An inventory could be a simple flat file with a collection of hosts defined within it or it could be a dynamic script (potentially querying a CMDB backend) that generates a list of devices to run the playbook against.

In this lab you will work with a file based inventory written in the **ini** format. Use the `cat` command to view the contents of your inventory:


```

[arista@ansible ~]$ cat ~/ansible-training/inventory/hosts
[all:vars]
ansible_port=22

[arista:children]
spines
leafs
hosts

[spines]
spine1 ansible_host=192.168.0.10
spine2 ansible_host=192.168.0.11

[leafs]
leaf1 ansible_host=192.168.0.14
leaf2 ansible_host=192.168.0.15
leaf3 ansible_host=192.168.0.16
leaf4 ansible_host=192.168.0.17

[hosts]
host1 ansible_host=192.168.0.31
host2 ansible_host=192.168.0.32
[arista@ansible ~]$

```

## Step 5

In the above output every `[ ]` defines a group. For example `[spines]` is a group that contains the hosts `spine1` and `spine2`. Groups can also be _nested_. The group `[arista]` is a parent group to the groups `[spines]`, `[leafs]` and `[hosts]`

> Parent groups are declared using the `children` directive. Having nested groups allows the flexibility of assigning more specific values to variables.


> Note: A group called **all** always exists and contains all groups and hosts defined within an inventory.


We can associate variables to groups and hosts. Host variables are declared/defined on the same line as the host themselves. For example for the host `spine1`:

```
spine1 ansible_host=52.90.196.252 ansible_ssh_user=arista extra_variable=172.16.165.205 ansible_network_os=eos

```

 - `spine1` - The name that Ansible will use.  This can but does not have to rely on DNS
 - `ansible_host` - The IP address that Ansible will use, if not configured it will default to DNS
 - `ansible_ssh_user` - The user Ansible will use to login to this host, if not configured it will default to the user the playbook is run from
 - `private_ip` - This value is not reserved by Ansible so it will default to a [host variable](http://docs.ansible.com/ansible/latest/intro_inventory.html#host-variables).  This variable can be used by playbooks or ignored completely.
- `ansible_network_os` - This variable is necessary while using the `network_cli` connection type within a play definition, as we will see shortly.

# Complete

You have completed lab exercise 1.0

---
