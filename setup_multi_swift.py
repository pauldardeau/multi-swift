#
#
#

import os
import os.path


SWIFT_USER_NAME = 'swift_user'
SWIFT_GROUP_NAME = 'swift_group'
SWIFT_HOME_BASE_DIR = 'swift_home_base_dir'
SWIFT_UID = 'swift_uid'
SWIFT_GID = 'swift_gid'
SWIFT_FS_TYPE = 'swift_fs_type'
SWIFT_DISK_SIZE_GB = 'swift_disk_size_gb'
SWIFT_DISK_BASE_DIR = 'swift_disk_base_dir'
SWIFT_DISK_COUNT = 'swift_disk_count'
SWIFT_MOUNT_BASE_DIR = 'swift_mount_base_dir'
SWIFT_CONFIG_BASE_DIR = 'swift_config_base_dir'
SWIFT_RUN_BASE_DIR = 'swift_run_base_dir'
SWIFT_CACHE_BASE_DIR = 'swift_cache_base_dir'
SWIFT_PULL_REPO = 'swift_pull_repo'
SWIFT_MOUNT_OPTIONS = 'swift_mount_options'


def change_owner(file_path, user_name, group_name, recurse=False):
    #TODO: get uid for user_name
    #TODO: get gid for group_name
    return os.chown(file_path, uid, gid)


def disk_base_dir(opts):
    return opts[SWIFT_DISK_BASE_DIR]


def mount_base_dir(opts):
    return opts[SWIFT_MOUNT_BASE_DIR]


def swift_pull_repo(opts):
    return opts[SWIFT_PULL_REPO]


def swift_local_repo(opts):
    return os.path.join(home_dir(opts), 'swift')


def dir_exists(dir_path):
    return os.path.isdir(dir_path)


def create_dir(dir_path):
    os.makedirs(dir_path)


def dir_replace_all(dir_path, replacements):
    """Replace all occurrences for all files in specified directory"""
    #TODO: enumerate all files in dir_path
    #TODO: if file is a text file (if this can be easily determined)
    #TODO: read file contents
    #TODO: call replace_all
    #TODO: if file contents are changed, re-write file
    pass


def replace_all(s, replacements):
    pass


def fs_type(opts):
    return opts[SWIFT_FS_TYPE]


def mount_options(opts):
    return opts[SWIFT_MOUNT_OPTIONS]


def fstab_entry(opts, disk_number, device):
    device_spec = '/srv/%s-disk%d' % (swift_user(opts), disk_number)
    mount_point = '%s/sdb2' % mount_base_dir(opts)  #TODO: fix sdb2
    return '%s %s %s %s' % (device_spec,mount_point,fs_type(opts),mount_options(opts))


def mkfs_command(opts):
    return 'mkfs.' + fs_type(opts)


def swift_user(opts):
    return opts[SWIFT_USER_NAME]


def config_dir(opts):
    return os.path.join(opts[SWIFT_CONFIG_BASE_DIR], swift_user(opts))


def run_dir(opts):
    return os.path.join(opts[SWIFT_RUN_BASE_DIR], swift_user(opts))


def cache_dir(opts):
    return os.path.join(opts[SWIFT_CACHE_BASE_DIR], swift_user(opts))


def home_dir(opts):
    return os.path.join(opts[SWIFT_HOME_BASE_DIR], swift_user(opts))


def repo_dir(opts):
    return os.path.join(home_dir(opts), 'swift')


def egg_cache_dir(opts):
    return os.path.join(home_dir(opts), 'tmp')


def tmp_dir(opts):
    return os.path.join('/tmp', swift_user(opts))


def test_config_file(opts):
    return os.path.join(config_dir(opts), 'test.conf')


def swift_group(opts):
    return opts[SWIFT_GROUP_NAME]


def swift_uid(opts):
    return opts[SWIFT_UID]


def swift_gid(opts):
    return opts[SWIFT_GID]


def create_disks(opts):
    pass


def create_directories(opts):
    swift_config_dir = config_dir(opts)
    swift_run_dir = run_dir(opts)
    user_name = swift_user(opts)
    group_name = swift_group(opts)
    swift_uid = swift_uid(opts)
    swift_gid = swift_gid(opts)

    # set up config dir
    create_dir(swift_config_dir)
    change_owner(swift_config_dir, user_name, group_name)

    # set up run dir
    create_dir(swift_run_dir)
    change_owner(swift_run_dir, user_name, group_name)

    create_dir(disk_base_dir(opts))
    create_dir(mount_base_dir(opts))

    for x in {1..8}; do
        SWIFT1_DISK="${SWIFT_DISK_BASE_DIR}/swift1-disk${x}"
        truncate -s "${SWIFT_DISK_SIZE_GB}GB" "${SWIFT1_DISK}"
        mkfs_command(opts) -f "${SWIFT1_DISK}"

    # good idea to have backup of fstab before we modify it
    cp /etc/fstab /etc/fstab.insert.bak

    #==================   START  ====================
    cat >> /etc/fstab << EOF
    /srv/swift1-disk1 /mnt/sdb1 fs_type(opts) loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    /srv/swift1-disk2 /mnt/sdb2 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    /srv/swift1-disk3 /mnt/sdb3 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    /srv/swift1-disk4 /mnt/sdb4 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    /srv/swift1-disk5 /mnt/sdb5 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    /srv/swift1-disk6 /mnt/sdb6 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    /srv/swift1-disk7 /mnt/sdb7 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    /srv/swift1-disk8 /mnt/sdb8 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0
    EOF
    #==================   STOP  =====================

    for x in {1..8}; do
        disk_dir = "${SWIFT_DISK_BASE_DIR}/swift1_${x}"
        mount_dir = "${SWIFT_MOUNT_BASE_DIR}/sdb${x}/swift1_${x}"
        create_dir(mount_dir) 
        change_owner(mount_dir, swift_user(opts), swift_group(opts))
        sudo ln -s ${SWIFT1_MOUNT_DIR} ${SWIFT1_DISK_DIR}
        sudo chown -h ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT1_DISK_DIR}

    sudo mkdir -p "${SWIFT1_CACHE_BASE_DIR}"
    create_dir(cache_base_dir)

    sudo mount -a

    for x in {1..8}; do
        sudo mkdir -p ${SWIFT_DISK_BASE_DIR}/swift1_${x}/node/sdb${x}
        sudo mkdir -p ${SWIFT_DISK_BASE_DIR}/swift2_${x}/node/sdc${x}

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


def setup_local_swift_repo(opts):
    user_home_dir = home_dir(opts)
    if dir_exists(user_home_dir):
        cmd = 'cd %s && git pull' % user_home_dir
    else:
        cmd = 'git clone %s' % swift_pull_repo(opts)
    exec_as_user(cmd, swift_user(opts))


#adding env variables to bashrc
def setup_bashrc(opts):
    env_var_stmts = '' 
    env_var_stmts += 'export SAIO_BLOCK_DEVICE=%s' % ??? 
    env_var_stmts += 'export SWIFT_TEST_CONFIG_FILE=%s' % test_config_file(opts) 
    env_var_stmts += 'export PATH=${PATH}:$HOME/.local/bin'
    env_var_stmts += 'export PYTHON_EGG_CACHE=%s' % egg_cache_dir(opts)
    append_to_file(env_var_stmts, login_config_file(opts))

    echo "export SAIO_BLOCK_DEVICE=/srv/swift-disk1" >> ${SWIFT1_LOGIN_CONFIG}
    echo "export SWIFT_TEST_CONFIG_FILE=/etc/swift1/test.conf" >> ${SWIFT1_LOGIN_CONFIG}
    echo "export PATH=${PATH}:$HOME/.local/bin" >> ${SWIFT1_LOGIN_CONFIG}
    echo "export PYTHON_EGG_CACHE=/home/swift/tmp" >> ${SWIFT1_LOGIN_CONFIG}

#Copying Configs to Config Directory
def setup_configs(opts):
    copy_file(os.path.join(local_repo_dir(opts),'/test/sample.conf'),
              test_config_file(opts))

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

#============================    START   ======================
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
#=========================    STOP  =======================


cd ${SWIFT2_USER_LOCAL_BIN};
sudo rm resetswift;

#========================   START  =======================
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
#============================  STOP  =======================

sudo chmod +x ${SWIFT1_USER_LOCAL_BIN}/*
sudo chmod +x ${SWIFT2_USER_LOCAL_BIN}/*



#**********************************************************************************************
#MODIFICATIONS TO THE SECOND REPOSITORY
# Changing the ports to 60** to 67** series
# and modifying the paths to suit swift2
#
#TODO: refine sed scripts to work efficiently and avoid the rework of replacing the wrong updates
#**********************************************************************************************

cd ${SWIFT1_REPO_DIR}; su - swift1;
sudo find . -type f -exec sed -i 's/\/etc\/swift/\/etc\/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/\/var\/run\/swift/\/var\/run\/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/\/var\/cache\/swift/\/var\/cache\/swift1/g' {} \;
sudo find . -type f -exec sed -i 's/\/tmp\/log\/swift/\/tmp\/swift1_log\/swift/g' {} \;
sudo find . -type f -exec sed -i 's/swift11/swift1/g' {} \;

cd ${SWIFT2_REPO_DIR};su - swift2;

replacements = []
replacements['8080'] = '8008'
replacements['6010'] = '6710'
replacements['6020'] = ''
replacements['6030'] = ''
replacements['6040'] = ''
replacements['6011'] = ''
replacements['6021'] = ''
replacements['6031'] = ''
replacements['6041'] = ''
replacements['6012'] = ''
replacements['6022'] = ''
replacements['6032'] = ''
replacements['6042'] = ''
replacements['swift22'] = 'swift2'

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


def get_swift_users():
    return ['swift1', 'swift2']


def setup_swift_environment(opts):
    print('setup swift user %s' % swift_user)


def main():
    opts = {}
    opts[SWIFT_GROUP] = 'swift'
    opts[SWIFT_FS_TYPE] = 'xfs'
    opts[SWIFT_DISK_SIZE_GB] = '1'
    opts[SWIFT_DISK_BASE_DIR] = '/srv'
    opts[SWIFT_DISK_COUNT] = '8'
    opts[SWIFT_MOUNT_BASE_DIR] = '/mnt'
    opts[SWIFT_CONFIG_BASE_DIR] = '/etc'
    opts[SWIFT_RUN_BASE_DIR] = '/var/run'
    opts[SWIFT_CACHE_BASE_DIR] = '/var/cache'
    opts[SWIFT_HOME_BASE_DIR] = '/home'
    opts[SWIFT_PULL_REPO] = 'https://github.com/openstack/swift'
    opts[SWIFT_MOUNT_OPTIONS] = 'loop,noatime,nodiratime,nobarrier,logbufs=8 0 0'

    swift_users = get_swift_users()
    group_name = swift_group(opts) 
    #TODO: retrieve gid for group

    for swift_user in swift_users:
        opts[SWIFT_USER] = swift_user
        #TODO: retrieve uid for user
        setup_swift_environment(opts)


if __name__=='__main__':
    main()

