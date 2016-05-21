#**************************************************************************
#  	SCRIPT TO ADD SWIFT LINUX USERS 
#**************************************************************************
#!/bin/sh
swift_group=swift
sudo groupadd $swift_group
echo $swift_group 'group has been created'
for i in `more userlist`
do
   echo 'adding user' $i
   sudo useradd -g $swift_group -m -s /bin/bash $i
   #sudo echo "$swift_group ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
   #sudo adduser $i sudo
done
