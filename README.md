# Dual-Swift 
Multi-swift is the idea of running multiple swift clusters on shared hardware.
The current implementation shows two swift all in one clusters - swift1 & swift2 running on shared OS and Hardware

## Why? ##
Why would anyone want to do this? Why not just buy more hardware? Or use multi-tenant capabilities
of swift?

## Enterprise Use Case ##

Say we have an enterprise with two lines of businesses(LOBs) wanting to deploy their application using OpenStack Swift.
The Enterprise has alredy invested on a beast like infrastructure and want to ensure it is utilized to the fullest. Also, 
each LOB is charged by the Data Center Group for maintenance cost per Operating System image.

Having the first LOB explored the Swift path, they got to own the complete hardware and successfuly deploy their application
in production. However, they are using just a fraction of available resources. When the second LOB decides to explore Swift,
the Enterprise is now against making an additional investment in hardware. When they see that the first LOB is bareky making use
of any hardware, they suggest the second LOB to share the infrastructure with the other LOB.

Now what? Swift is multi tenant by default! Why can't you have both the LOBs use separate accounts on the same Swift Cluster?
Sure, Swift is multi tenant supportive. But, what if both the LOBs want to have different sets of middleware?

A single swift cluster can have multiple proxy servers. So why not configure different proxy servers and have different middlewares
in it's pipeline?
Sure, we can do that. But, we cannot a single human administator managing the swift clusters for both the LOBs. In this attempt, we not
only eliminate the dependency of one human operator being shared between the departments, but also be able to have separate maintenance 
windows for both the clusters, separate network lines and also allign to the enterprise's goal of optimum resource utilization and minimize
costs by sharing hardware

## Required Changes ##
In order to have two swift clusters running parallely on the same hardware and OS, we need to ensure they both have clear separate paths, 
ports and services dedicated to each of them

* paths
  - Various paths listed that will conflict are as follows: 
    - Configuration paths: /etc/swift --> this is where all the required configuration files are stored
    - Run Directories: /var/run/swift --> this directory is used to spin off the swift process and store run time infomation
    - Cache Directories: /var/cache/swift --> this directory is used by swift-recon daemon process to dump stats from various storage nodes connected
    - Temp Directories: /tmp/log/swift --> temp folder where profiler dumps that stats of a test run

* ports
  - Swift has multiple processes running and listening on different ports. All of these ports have to be separated. Below are the list of ports for 
    swift1 and swift2 clusters.
  - All the ports for the second swift cluster have been modified to start with a series if 67**
    - proxy-server: 8080 --> 8008
    - account-server: 60x2 --> 67x2
    - container-server: 60x1 --> 67x2
    - object-server: 60x0 --> 67x0

* devices
  - Both the swift clusters have separate disks that are mounted on separate mount points. We've got to modify the remakerings script to add the devices to
    the ring builder commands. 

* memcached
  - Both the swift instances need  separate memcached instances. memcache stores the Swift's auth token, swift user credentials etc. Clearly this needs to be 
   separated for both the clusters. The port is hardcoded in the Swift code, and we can change the swift2 cluster to listen on separate port
    - swift1 memcached port: 11211
    - swift2 memcached port: 11212

* rsyslog
  - rsyslog daemon also needs to be separated for both the clusters in order to enable logging separately for both the clustres. This can be achieved using "facility"
    feature in rsyslog

