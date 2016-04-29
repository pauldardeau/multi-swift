# multi-swift
Multi-swift is the idea of running multiple swift clusters on shared hardware.
The current implementation shows two swift all in one clusters running on shared OS and Hardware

## Why? ##
Why would anyone want to do this? Why not just buy more hardware? Or use multi-tenant capabilities
of swift?

## Enterprise Use Case ##
* 2 or more unrelated departments or business units
* a need to isolate the swift clusters that service these needs
* a desire to minimize costs (perhaps datacenter chargeback costs) by sharing hardware infrastructure

## Required Changes ##
* paths
    Various paths such as
        * Configuration paths: /etc/swift
        * Run Directories: /var/run/swift
        * Cache Directories: /var/cache/swift
        * Temp Directories: /tmp/log/swift
* ports
    All the ports for the second swift cluster have been modified to start with a series if 67**
* devices
    Both the swift clusters have separate disks that are mounted on separate mount points. We've got to modify the ringbuilder commands accordingly
* memcached
    Both the swift instances need to separate memcached instance configured to listen on separate ports (11211 & 11212)

