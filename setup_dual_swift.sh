#!/bin/bash

#*************************************************************************************************
#   THIS IS A DRAFT OF THE SETUP SCRIPT FOR DUAL SAIO INSTALLATIONS SHARING THE SAME HARDWARE
# This script may not be fully functional yet. I will be updating it regularly. This script requires
# you to run ass users script first.
#*************************************************************************************************
SWIFT1_USER="swift1"
SWIFT2_USER="swift2"
SWIFT_GROUP="swift"

SWIFT_DISK_SIZE_GB="1"
SWIFT_DISK_BASE_DIR="/srv"
SWIFT_MOUNT_BASE_DIR="/mnt"

SWIFT1_CONFIG_DIR="/etc/swift1"
SWIFT1_RUN_DIR="/var/run/swift1"
SWIFT1_CACHE_BASE_DIR="/var/cache/swift1"

SWIFT2_CONFIG_DIR="/etc/swift2"
SWIFT2_RUN_DIR="/var/run/swift2"
SWIFT2_CACHE_BASE_DIR="/var/cache/swift2"

sudo mkdir -p "${SWIFT1_CONFIG_DIR}"
sudo chown $SWIFT1_USER:$SWIFT_GROUP ${SWIFT1_CONFIG_DIR}
sudo mkdir -p "${SWIFT1_RUN_DIR}"
sudo chown $SWIFT1_USER:$SWIFT_GROUP ${SWIFT1_RUN_DIR}

sudo mkdir -p "${SWIFT2_CONFIG_DIR}"
sudo chown $SWIFT2_USER:$SWIFT_GROUP ${SWIFT2_CONFIG_DIR}
sudo mkdir -p "${SWIFT2_RUN_DIR}"
sudo chown $SWIFT2_USER:$SWIFT_GROUP ${SWIFT2_RUN_DIR}

sudo mkdir -p "${SWIFT_DISK_BASE_DIR}"
sudo mkdir -p "${SWIFT_MOUNT_BASE_DIR}"

for x in {1..8}; do
   SWIFT1_DISK="${SWIFT_DISK_BASE_DIR}/swift1-disk${x}"
   SWIFT2_DISK="${SWIFT_DISK_BASE_DIR}/swift2-disk${x}"  
   sudo truncate -s "${SWIFT_DISK_SIZE_GB}GB" "${SWIFT1_DISK}"
   sudo truncate -s "${SWIFT_DISK_SIZE_GB}GB" "${SWIFT2_DISK}"
   sudo mkfs.xfs -f "${SWIFT1_DISK}"
   sudo mkfs.xfs -f "${SWIFT2_DISK}"
done

# good idea to have backup of fstab before we modify it
cp /etc/fstab /etc/fstab.insert.bak

cat >> /etc/fstab << EOF
/srv/swift1-disk1 /mnt/sdb1 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift1-disk2 /mnt/sdb2 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift1-disk3 /mnt/sdb3 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift1-disk4 /mnt/sdb4 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift1-disk5 /mnt/sdb5 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift1-disk6 /mnt/sdb6 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift1-disk7 /mnt/sdb7 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift1-disk8 /mnt/sdb8 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0

/srv/swift2-disk1 /mnt/sdc1 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift2-disk2 /mnt/sdc2 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift2-disk3 /mnt/sdc3 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift2-disk4 /mnt/sdc4 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift2-disk5 /mnt/sdc5 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift2-disk6 /mnt/sdc6 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift2-disk7 /mnt/sdc7 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
/srv/swift2-disk8 /mnt/sdc8 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
EOF

for x in {1..8}; do
   SWIFT1_DISK_DIR="${SWIFT_DISK_BASE_DIR}/swift1_${x}"
   SWIFT2_DISK_DIR="${SWIFT_DISK_BASE_DIR}/swift2_${x}"
   SWIFT1_MOUNT_DIR="${SWIFT_MOUNT_BASE_DIR}/sdb${x}/swift1_${x}"
   SWIFT2_MOUNT_DIR="${SWIFT_MOUNT_BASE_DIR}/sdc${x}/swift2_${x}"
   sudo mkdir ${SWIFT1_MOUNT_DIR}
   sudo mkdir ${SWIFT2_MOUNT_DIR}
   sudo chown ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT1_MOUNT_DIR}
   sudo chown ${SWIFT2_USER}:${SWIFT_GROUP} ${SWIFT2_MOUNT_DIR}

   sudo ln -s ${SWIFT1_MOUNT_DIR} ${SWIFT1_DISK_DIR}
   sudo ln -s ${SWIFT2_MOUNT_DIR} ${SWIFT2_DISK_DIR}
   sudo chown -h ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT1_DISK_DIR}
   sudo chown -h ${SWIFT2_USER}:${SWIFT_GROUP} ${SWIFT2_DISK_DIR}

done

sudo mkdir -p "${SWIFT1_CACHE_BASE_DIR}"
sudo mkdir -p "${SWIFT2_CACHE_BASE_DIR}"

sudo mount -a

for x in {1..8}; do
   sudo mkdir -p ${SWIFT_DISK_BASE_DIR}/swift1_${x}/node/sdb${x}
   sudo mkdir -p ${SWIFT_DISK_BASE_DIR}/swift2_${x}/node/sdc${x}
done

sudo chown -R ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT1_DISK_DIR}
sudo chown -R ${SWIFT2_USER}:${SWIFT_GROUP} ${SWIFT2_DISK_DIR}

#***********************************************************************************************

SWIFT1_USER_HOME="/home/${SWIFT1_USER}"
SWIFT1_USER_LOCAL_BIN="${SWIFT1_USER_HOME}/.local/bin"
mkdir -p ${SWIFT1_USER_LOCAL_BIN}
SWIFT1_LOGIN_CONFIG="${SWIFT1_USER_HOME}/.bashrc"

SWIFT2_USER_HOME="/home/${SWIFT2_USER}"
SWIFT2_USER_LOCAL_BIN="${SWIFT2_USER_HOME}/.local/bin"
mkdir -p ${SWIFT2_USER_LOCAL_BIN}
SWIFT2_LOGIN_CONFIG="${SWIFT2_USER_HOME}/.bashrc"

SWIFT1_REPO_DIR="${SWIFT1_USER_HOME}/swift"
SWIFT2_REPO_DIR="${SWIFT2_USER_HOME}/swift"

#************************************************************************************************
# CLONING AND MODIFYING REPOSITORIES FOR DUAL SWIFT
#************************************************************************************************

if [ -d ${SWIFT1_USER_HOME}]; then
   su - ${SWIFT1_USER} -c 'cd swift && git pull'
else
   su - ${SWIFT1_USER} -c 'git clone https://github.com/openstack/swift'
fi

if [ -d ${SWIFT2_USER_HOME}]; then
   su - ${SWIFT2_USER} -c 'cd swift && git pull'
else
   su - ${SWIFT2_USER} -c 'git clone https://github.com/openstack/swift'
fi


#adding env variables to bashrc
echo "export SAIO_BLOCK_DEVICE=/srv/swift-disk1" >> ${SWIFT1_LOGIN_CONFIG}
echo "export SWIFT_TEST_CONFIG_FILE=/etc/swift1/test.conf" >> ${SWIFT1_LOGIN_CONFIG}
echo "export PATH=${PATH}:$HOME/.local/bin" >> ${SWIFT1_LOGIN_CONFIG}
echo "export PYTHON_EGG_CACHE=/home/swift/tmp" >> ${SWIFT1_LOGIN_CONFIG}
	
echo "export SAIO_BLOCK_DEVICE=/srv/swift-disk2" >> ${SWIFT2_LOGIN_CONFIG}
echo "export SWIFT_TEST_CONFIG_FILE=/etc/swift2/test.conf" >> ${SWIFT2_LOGIN_CONFIG}
echo "export PATH=${PATH}:$HOME/.local/bin" >> ${SWIFT2_LOGIN_CONFIG}
echo "export PYTHON_EGG_CACHE=/home/swift/tmp" >> ${SWIFT2_LOGIN_CONFIG}

#Copying Configs to Config Directory

sudo cp ${SWIFT1_REPO_DIR}/test/sample.conf ${SWIFT1_CONFIG_DIR}/test.conf
sudo cp ${SWIFT2_REPO_DIR}/test/sample.conf ${SWIFT2_CONFIG_DIR}/test.conf

cd ${SWIFT1_REPO_DIR}/doc/saio/swift; cp -r * ${SWIFT1_CONFIG_DIR}; cd -
cd ${SWIFT2_REPO_DIR}/doc/saio/swift; cp -r * ${SWIFT2_CONFIG_DIR}; cd -

chown -R ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT1_CONFIG_DIR}
chown -R ${SWIFT2_USER}:${SWIFT_GROUP} ${SWIFT2_CONFIG_DIR}

find ${SWIFT1_CONFIG_DIR}/ -name \*.conf | xargs sed -i "s/<your-user-name>/${SWIFT1_USER}/"
find ${SWIFT2_CONFIG_DIR}/ -name \*.conf | xargs sed -i "s/<your-user-name>/${SWIFT2_USER}/"

cd ${SWIFT1_CONFIG_DIR};
sudo find . -type f -exec sed -i 's/\/srv\/1\/node/\/srv\/swift1_1\/node/g' {} \;
sudo find . -type f -exec sed -i 's/\/srv\/2\/node/\/srv\/swift1_2\/node/g' {} \;
sudo find . -type f -exec sed -i 's/\/srv\/3\/node/\/srv\/swift1_3\/node/g' {} \;
sudo find . -type f -exec sed -i 's/\/srv\/4\/node/\/srv\/swift1_4\/node/g' {} \;
sudo find . -type f -exec sed -i 's/swift12/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/swift13/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/swift14/swift1/g' {} \;
	
cd ${SWIFT1_CONFIG_DIR};
sudo find . -type f -exec sed -i 's/\/srv\/1\/node/\/srv\/swift2_1\/node/g' {} \;
sudo find . -type f -exec sed -i 's/\/srv\/2\/node/\/srv\/swift2_2\/node/g' {} \;
sudo find . -type f -exec sed -i 's/\/srv\/3\/node/\/srv\/swift2_3\/node/g' {} \;
sudo find . -type f -exec sed -i 's/\/srv\/4\/node/\/srv\/swift2_4\/node/g' {} \;
sudo find . -type f -exec sed -i 's/swift22/swift2/g' {} \;
sudo find . -type f -exec sed -i 's/swift23/swift2/g' {} \;
sudo find . -type f -exec sed -i 's/swift24/swift2/g' {} \;


EXPORT_SWIFT1_PATH="export PATH=${PATH}:${SWIFT1_USER_LOCAL_BIN}:${SWIFT1_USER_HOME}/swift/bin"
EXPORT_SWIFT2_PATH="export PATH=${PATH}:${SWIFT2_USER_LOCAL_BIN}:${SWIFT2_USER_HOME}/swift/bin"

su - ${SWIFT1_USER} -c 'cd ${SWIFT1_USER_HOME}/swift;'

sudo python setup.py develop --user
cd ${SWIFT1_USER_HOME}; sudo chown -R ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT2_USER_LOCAL_BIN}
cd ${SWIFT1_REPO_DIR}/doc/saio/bin; cp * ${SWIFT1_USER_LOCAL_BIN}; cd -

su - ${SWIFT2_USER} -c 'cd ${SWIFT2_USER_HOME}/swift;'
sudo python setup.py develop --user
cd ${SWIFT2_USER_HOME}; sudo chown -R ${SWIFT2_USER}:${SWIFT_GROUP} ${SWIFT2_USER_LOCAL_BIN}
cd ${SWIFT2_REPO_DIR}/doc/saio/bin; cp * ${SWIFT2_USER_LOCAL_BIN}; cd -

cd ${SWIFT1_REPO_DIR}/doc/saio/bin; sudo cp * ${SWIFT1_USER_LOCAL_BIN}; cd -
cd ${SWIFT2_REPO_DIR}/doc/saio/bin; sudo cp * ${SWIFT2_USER_LOCAL_BIN}; cd -

cd ${SWIFT1_USER_LOCAL_BIN}; 
sudo rm resetswift;
cat >> resetswift << EOF

swift-init all stop
# Remove the following line if you did not set up rsyslog for individual logging:
sudo umount /mnt/sdb*
# If you are using a loopback device set SAIO_BLOCK_DEVICE to "/srv/swift-disk"
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk1}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk2}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk3}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk4}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk5}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk6}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk7}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk8}
sudo mount /mnt/sdb*
sudo mkdir -p /mnt/sdb1/swift1_1 /mnt/sdb1/swift1_2 /mnt/sdb1/swift1_3 /mnt/sdb1/swift1_4
sudo mkdir -p /mnt/sdb5/swift1_5 /mnt/sdb6/swift1_6 /mnt/sdb7/swift1_7 /mnt/sdb8/swift1_8

sudo chown -R swift1:swift /mnt/sdb*
mkdir -p /srv/swift1_1/node/sdb1 /srv/swift1_5/node/sdb5 \
         /srv/swift1_2/node/sdb2 /srv/swift1_6/node/sdb6 \
         /srv/swift1_3/node/sdb3 /srv/swift1_7/node/sdb7 \
         /srv/swift1_4/node/sdb4 /srv/swift1_8/node/sdb8
sudo rm -f /var/log/debug /var/log/messages /var/log/rsyncd.log /var/log/syslog
find /var/cache/swift1* -type f -name *.recon -exec rm -f {} \;
if [ "`type -t systemctl`" == "file" ]; then
    sudo systemctl restart rsyslog
    sudo systemctl restart memcached
else
    sudo service rsyslog restart
    sudo /etc/init.d/memcached restart swift1
fi
EOF


cd ${SWIFT2_USER_LOCAL_BIN};
sudo rm resetswift;
cat >> resetswift << EOF

swift-init all stop
# Remove the following line if you did not set up rsyslog for individual logging:
sudo umount /mnt/sdc*
# If you are using a loopback device set SAIO_BLOCK_DEVICE to "/srv/swift-disk"
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk1}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk2}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk3}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk4}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk5}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk6}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk7}
sudo mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift2-disk8}
sudo mount /mnt/sdc*
sudo mkdir /mnt/sdc1/swift2_1 /mnt/sdc1/swift2_2 /mnt/sdc1/swift2_3 /mnt/sdc1/swift2_4
sudo mkdir /mnt/sdc1/swift2_5 /mnt/sdc1/swift2_6 /mnt/sdc1/swift2_7 /mnt/sdc1/swift2_8
sudo chown swift2:swift /mnt/sdc*
mkdir -p /srv/swift2_1/node/sdc1 /srv/swift2_5/node/sdc5 \
         /srv/swift2_2/node/sdc2 /srv/swift2_6/node/sdc6 \
         /srv/swift2_3/node/sdc3 /srv/swift2_7/node/sdc7 \
         /srv/swift2_4/node/sdc4 /srv/swift2_8/node/sdc8
sudo rm -f /var/log/debug /var/log/messages /var/log/rsyncd.log /var/log/syslog
find /var/cache/swift2* -type f -name *.recon -exec rm -f {} \;
if [ "`type -t systemctl`" == "file" ]; then
    sudo systemctl restart rsyslog
    sudo systemctl restart memcached
else
    sudo service rsyslog restart
    sudo /etc/init.d/memcached restart swift2
fi

EOF

sudo chmod +x ${SWIFT1_USER_LOCAL_BIN}/*
sudo chmod +x ${SWIFT2_USER_LOCAL_BIN}/*



#**********************************************************************************************
#MODIFICATIONS TO THE SECOND REPOSITORY
#**********************************************************************************************

cd ${SWIFT1_REPO_DIR}; su - swift1;
sudo find . -type f -exec sed -i 's/\/etc\/swift/\/etc\/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/\/var\/run\/swift/\/var\/run\/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/\/var\/cache\/swift/\/var\/cache\/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/\/tmp\/log\/swift/\/tmp\/swift1_log\/swift/g' {} \;
sudo find . -type f -exec sed -i 's/swift11/swift1/g' {} \;

cd ${SWIFT2_REPO_DIR};su - swift2;
sudo find . -type f -exec sed -i 's/\/etc\/swift/\/etc\/swift2/g' {} \;
sudo find . -type f -exec sed -i 's/\/var\/run\/swift/\/var\/run\/swift2/g' {} \;
sudo find . -type f -exec sed -i 's/\/var\/cache\/swift/\/var\/cache\/swift2/g' {} \;
sudo find . -type f -exec sed -i 's/\/tmp/\/tmp\/swift2_tmp/g' {} \;

sudo find . -type f -exec sed -i 's/8080/8008/g' {} \;
sudo find . -type f -exec sed -i 's/6010/6710/g' {} \;
sudo find . -type f -exec sed -i 's/6020/6720/g' {} \;
sudo find . -type f -exec sed -i 's/6030/6730/g' {} \;
sudo find . -type f -exec sed -i 's/6040/6740/g' {} \;
sudo find . -type f -exec sed -i 's/6011/6711/g' {} \;
sudo find . -type f -exec sed -i 's/6021/6721/g' {} \;
sudo find . -type f -exec sed -i 's/6031/6731/g' {} \;
sudo find . -type f -exec sed -i 's/6041/6741/g' {} \;
sudo find . -type f -exec sed -i 's/6012/6712/g' {} \;
sudo find . -type f -exec sed -i 's/6022/6722/g' {} \;
sudo find . -type f -exec sed -i 's/6032/6732/g' {} \;
sudo find . -type f -exec sed -i 's/6042/6742/g' {} \;
sudo find . -type f -exec sed -i 's/swift22/swift2/g' {} \;
sudo find . -type f -exec sed -i 's/swift1_cache/swift2_cache/g' {} \;

"""	
##Rsyslog setup
sudo cp /home/swift1/swift/doc/saio/rsyslog.d/10-swift.conf /etc/rsyslog.d/
Edit /etc/rsyslog.conf and make the following change (usually in the “GLOBAL DIRECTIVES” section):
$PrivDropToGroup adm
sudo mkdir -p /var/log/swift
sudo chown -R syslog.adm /var/log/swift
sudo chmod -R g+w /var/log/swift
sudo service rsyslog restart
"""

	


