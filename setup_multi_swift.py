#
#
#

import os
import os.path
import pwd
import shutil


RUN_MODE_EXEC = 'exec'
RUN_MODE_LOGIC = 'logic'
RUN_MODE_PREVIEW = 'preview'

GB_BYTES = 1024 * 1024 * 1024
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
SWIFT_REMOTE_REPO = 'swift_remote_repo'
SWIFT_MOUNT_OPTIONS = 'swift_mount_options'
SWIFT_MKFS_OPTIONS = 'swift_mkfs_options'
SWIFT_HOME_LOCAL_BIN = 'swift_home_local_bin'
SWIFT_PORT_ADJUST = 'swift_port_adjust'
SWIFT_PROXY_PORT_ADJUST = 'swift_proxy_port_adjust'
SWIFT_REPO_NAME = 'swift_repo_name'
SWIFT_RUN_MODE = 'swift_run_mode'


def swift_run_mode(opts):
    return opts[SWIFT_RUN_MODE]


def swift_is_exec_mode(opts):
    return swift_run_mode(opts) == RUN_MODE_EXEC


def swift_is_logic_mode(opts):
    return swift_run_mode(opts) == RUN_MODE_LOGIC


def swift_is_preview_mode(opts):
    return swift_run_mode(opts) == RUN_MODE_PREVIEW


def swift_repo_name(opts):
    return opts[SWIFT_REPO_NAME]


def swift_port_adjust(opts):
    return int(opts[SWIFT_PORT_ADJUST])


def swift_proxy_port_adjust(opts):
    return int(opts[SWIFT_PROXY_PORT_ADJUST])


def swift_disk_count(opts):
    return int(opts[SWIFT_DISK_COUNT])


def swift_disk_size_gb(opts):
    return opts[SWIFT_DISK_SIZE_GB]


def swift_mkfs_options(opts):
    return opts[SWIFT_MKFS_OPTIONS]


def create_file_system(opts, fs_path):
    if swift_is_logic_mode(opts): 
        print('create_file_system: %s' % fs_path)
    else:
        #TODO: implement create_file_system
        pass


def create_file_with_gb_size(opts, file_path, gb_size):
    gb_size_in_bytes = GB_BYTES * gb_size
    if swift_is_logic_mode(opts):
        print('create_file_with_gb_size: %s %s (%s)' % (file_path,
                                                        gb_size,
                                                        str(gb_size_in_bytes)))
    else:
        if swift_is_exec_mode(opts):
            with open(file_path, 'w') as f:
                f.truncate(gb_size_in_bytes)
        elif swift_is_preview_mode(opts):
            print("open('%s','w'); truncate(%d)" % (file_path, gb_size_in_bytes))


def file_exists(opts, file_path):
    if swift_is_logic_mode(opts):
    	print('checking_file_exists: %s' % file_path)
    return os.path.isfile(file_path)


def delete_file(opts, file_to_delete):
    if swift_is_logic_mode(opts):
        print('delete_file: %s' % file_to_delete)
    elif swift_is_preview_mode(opts):
        print("os.remove('%s')" % file_to_delete)
    elif swift_is_exec_mode(opts):
    	os.remove(file_to_delete)


def delete_file_if_exists(opts, file_to_delete):
    if swift_is_logic_mode(opts):
        print('delete_file_if_exists: %s' % file_to_delete)
    if file_exists(opts, file_to_delete):
        delete_file(opts, file_to_delete)


def copy_file(opts, src_file, dest):
    if swift_is_logic_mode(opts):
        print('copy_file: %s %s' % (src_file, dest))
    elif swift_is_preview_mode(opts):
        print("shutil.copy('%s', '%s')" % (src_file, dest))
    elif swift_is_exec_mode(opts):
        shutil.copy(src_file, dest)


def copy_all(opts, src_dir, dest_dir, recurse=False):
    if swift_is_logic_mode(opts):
        print('copy_all: %s %s' % (src_dir, dest_dir))
    #TODO: implement preview mode of copy_all
    #TODO: implement exec mode of copy_all


def append_to_file(opts, text_to_append, file_path):
    if swift_is_logic_mode(opts):
        print('append_to_file: %s' % file_path)
        print('%s...' % text_to_append[0:40])
    elif swift_is_preview_mode(opts):
        print("open('%s', 'a'); print('%s...')" % (file_path, text_to_append[0:40]))
    elif swift_is_exec_mode(opts):
        with open(file_path, "a") as f:
            f.write(text_to_append)


def change_owner(opts, file_path, user_name, group_name, recurse=False):
    if swift_is_logic_mode(opts):
        print('change_owner: %s (%s,%s)' % (file_path,
                                            user_name,
                                            group_name))
    else:
        uid = pwd.getpwnam(user_name).pw_uid
        gid = pwd.getpwnam(user_name).pw_gid
        if swift_is_preview_mode(opts):
            print("os.chown('%s', %s, %s)" % (file_path, str(uid), str(gid)))
        elif swift_is_exec_mode(opts):
            os.chown(file_path, uid, gid)


def swift_disk_base_dir(opts):
    return opts[SWIFT_DISK_BASE_DIR]


def swift_mount_base_dir(opts):
    return opts[SWIFT_MOUNT_BASE_DIR]


def swift_remote_repo(opts):
    return opts[SWIFT_REMOTE_REPO]


def swift_local_repo(opts):
    return os.path.join(swift_home_dir(opts), swift_repo_name(opts))


def dir_exists(opts, dir_path):
    if swift_is_logic_mode(opts):
        print('checking_dir_exists: %s' % dir_path)
    return os.path.isdir(dir_path)


def create_dir(opts, dir_path):
    if swift_is_logic_mode(opts):
        print('create_dir: %s' % dir_path)
    elif swift_is_preview_mode(opts):
        print("os.makedirs('%s')" % dir_path)
    elif swift_is_exec_mode(opts):
        os.makedirs(dir_path)


def create_link(opts, src, dest):
    if swift_is_logic_mode(opts):
        print('create_link %s <-- %s' % (src, dest))
    elif swift_is_preview_mode(opts):
        print("os.symlink('%s', '%s')" % (src, dest))
    elif swift_is_exec_mode(opts):
        os.symlink(src, dest)


def dir_replace_all(opts, dir_path, replacements):
    """Replace all occurrences for all files in specified directory"""
    #TODO: dir_replace_all: enumerate all files in dir_path
    #TODO: dir_replace_all: if file is a text file (if this can be easily determined)
    #TODO: dir_replace_all: read file contents
    #TODO: dir_replace_all: call replace_all
    #TODO: dir_replace_all: if file contents are changed, re-write file
    if swift_is_logic_mode(opts):
        print('dir_replace_all: %s %s' % (dir_path, repr(replacements)))
    #TODO: implement preview mode of dir_replace_all
    #TODO: implement exec mode of dir_replace_all


def dir_replace(opts, dir_path, file_spec, replacements):
    if swift_is_logic_mode(opts):
        print('dir_replace: %s %s %s' % (dir_path, file_spec, repr(replacements)))
    #TODO: implement preview mode of dir_replace
    #TODO: implement exec mode of dir_replace


def replace_all(opts, s, replacements):
    if swift_is_logic_mode(opts):
        print('replace_all: %s %s' % (s, repr(replacements)))
    #TODO: implement preview mode of replace_all
    #TODO: implement exec mode of replace_all


def swift_fs_type(opts):
    return opts[SWIFT_FS_TYPE]


def swift_mount_options(opts):
    return opts[SWIFT_MOUNT_OPTIONS]


def fstab_entry(opts, disk_number, device):
    device_spec = '%s/%s-disk%d' % (swift_disk_base_dir(opts), swift_user(opts), disk_number)
    mount_point = '%s/sdb2' % swift_mount_base_dir(opts)  #TODO: fstab_entry: fix sdb2
    return '%s %s %s %s' % (device_spec,mount_point,swift_fs_type(opts),swift_mount_options(opts))


def mkfs_command(opts):
    return 'mkfs.' + swift_fs_type(opts)


def swift_user(opts):
    return opts[SWIFT_USER_NAME]


def swift_config_dir(opts):
    return os.path.join(opts[SWIFT_CONFIG_BASE_DIR], swift_user(opts))


def swift_run_dir(opts):
    return os.path.join(opts[SWIFT_RUN_BASE_DIR], swift_user(opts))


def swift_cache_base_dir(opts):
    return opts[SWIFT_CACHE_BASE_DIR]


def swfit_cache_dir(opts):
    return os.path.join(swift_cache_base_dir(opts), swift_user(opts))


def swift_home_dir(opts):
    return os.path.join(opts[SWIFT_HOME_BASE_DIR], swift_user(opts))


def swift_home_local_bin_dir(opts):
    return os.path.join(swift_home_dir(opts), opts[SWIFT_HOME_LOCAL_BIN])


def swift_egg_cache_dir(opts):
    return os.path.join(swift_home_dir(opts), 'tmp')


def swift_tmp_dir(opts):
    return os.path.join('/tmp', swift_user(opts))


def swift_test_config_file(opts):
    return os.path.join(swift_config_dir(opts), 'test.conf')


def swift_group(opts):
    return opts[SWIFT_GROUP_NAME]


def swift_uid(opts):
    return opts[SWIFT_UID]


def swift_gid(opts):
    return opts[SWIFT_GID]


def create_disks(opts):
    #TODO: implement create_disks
    pass


def setup_fstab_entries(opts):
    fstab_entries = ''
    fs_type = swift_fs_type(opts) 
    mount_options = swift_mount_options(opts)
    user = swift_user(opts)
    mount_base_dir = swift_mount_base_dir(opts)
    disk_base_dir = swift_disk_base_dir(opts)
    for x in range(swift_disk_count(opts)):
        device_spec = '%s/%s-disk1' % (disk_base_dir, user)
        mount_point = '%s/sdb1' % (mount_base_dir)
        fs_entry = '%s %s %s %s\n' % (device_spec, mount_point, fs_type, mount_options)
        fstab_entries += fs_entry
    append_to_file(opts, fstab_entries, '/etc/fstab')


def swift_create_directories(opts):
    config_dir = swift_config_dir(opts)
    run_dir = swift_run_dir(opts)
    disk_base_dir = swift_disk_base_dir(opts)
    user_name = swift_user(opts)
    group_name = swift_group(opts)

    # set up config dir
    create_dir(opts, config_dir)
    change_owner(opts, config_dir, user_name, group_name)

    # set up run dir
    create_dir(opts, run_dir)
    change_owner(opts, run_dir, user_name, group_name)

    create_dir(opts, disk_base_dir)
    create_dir(opts, swift_mount_base_dir(opts))

    # good idea to have backup of fstab before we modify it
    copy_file(opts, '/etc/fstab', '/etc/fstab_insert_%s' % user_name)

    gb_size_as_int = int(swift_disk_size_gb(opts))

    for x in range(swift_disk_count(opts)):
        disk_num = '%d' % (x+1)
        disk_path = '%s/%s-disk%s' % (disk_base_dir, user_name, disk_num)
        create_file_with_gb_size(opts, disk_path, gb_size_as_int)
        create_file_system(opts, disk_path)

    setup_fstab_entries(opts)

    mount_base_dir = swift_mount_base_dir(opts)

    for x in range(swift_disk_count(opts)):
        disk_num = '%d' % (x+1)
        SWIFT1_DISK_DIR = '%s/%s_%s' % (disk_base_dir, user_name, disk_num)
        disk_dir = '%s/%s_%s' % (disk_base_dir, user_name, disk_num)
        mount_dir = '%s/sdb%s/%s_%s' % (mount_base_dir, disk_num, user_name, disk_num)
        create_dir(opts, mount_dir) 
        change_owner(opts, mount_dir, user_name, group_name)
        create_link(opts, mount_dir, disk_dir)
        change_owner(opts, disk_dir, user_name, group_name)

    cache_base_dir = swift_cache_base_dir(opts)
    create_dir(opts, cache_base_dir)

    #mount -a

    for x in range(swift_disk_count(opts)):
        disk_num = '%d' % (x+1)
        dir_path = '%s/%s_%s/node/sdb%s' % (disk_base_dir, user_name, disk_num, disk_num)
        create_dir(opts, dir_path)

    #PJD: SWIFT1_DISK_DIR doesn't seem correct here
    #chown -R ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT1_DISK_DIR}
    change_owner(opts, SWIFT1_DISK_DIR, user_name, group_name, True)

#******************************************************************************

#SWIFT1_USER_HOME="/home/${SWIFT1_USER}"
#SWIFT1_USER_LOCAL_BIN="${SWIFT1_USER_HOME}/.local/bin"
#mkdir -p ${SWIFT1_USER_LOCAL_BIN}
#SWIFT1_LOGIN_CONFIG="${SWIFT1_USER_HOME}/.bashrc"
#SWIFT1_REPO_DIR="${SWIFT1_USER_HOME}/swift"

#******************************************************************************

def exec_as_user(opts, cmd, exec_user):
    if swift_is_logic_mode(opts):
        print('exec (%s): %s' % (exec_user, cmd))
    #TODO: implement preview mode of exec_as_user
    #TODO: implement exec mode of exec_as_user


def setup_local_swift_repo(opts):
    user_home_dir = swift_home_dir(opts)
    if dir_exists(user_home_dir):
        cmd = 'cd %s && git pull' % user_home_dir
    else:
        cmd = 'git clone %s' % swift_remote_repo(opts)
    exec_as_user(opts, cmd, swift_user(opts))


def setup_bashrc(opts):
    env_var_stmts = '' 
    #env_var_stmts += 'export SAIO_BLOCK_DEVICE=%s' % ??? 
    env_var_stmts += 'export SWIFT_TEST_CONFIG_FILE=%s' % swift_test_config_file(opts) 
    env_var_stmts += 'export PATH=${PATH}:$HOME/.local/bin'
    env_var_stmts += 'export PYTHON_EGG_CACHE=%s' % swift_egg_cache_dir(opts)
    append_to_file(opts, env_var_stmts, login_config_file(opts))
    disk_base_dir = swift_disk_base_dir(opts)
    #echo "export SAIO_BLOCK_DEVICE=/srv/swift-disk1" >> ${SWIFT1_LOGIN_CONFIG}
    #echo "export SWIFT_TEST_CONFIG_FILE=/etc/swift1/test.conf" >> ${SWIFT1_LOGIN_CONFIG}
    #echo "export PATH=${PATH}:$HOME/.local/bin" >> ${SWIFT1_LOGIN_CONFIG}
    #echo "export PYTHON_EGG_CACHE=/home/swift/tmp" >> ${SWIFT1_LOGIN_CONFIG}


def swift_setup_configs(opts):
    repo_dir = swift_local_repo(opts)
    copy_file(opts,
              os.path.join(repo_dir,'test/sample.conf'),
              swift_test_config_file(opts))

    user = swift_user(opts)
    group = swift_group(opts)
    repo_dir = swift_local_repo(opts)
    config_dir = swift_config_dir(opts)

    source_dir = '%s/doc/saio/swift' % repo_dir
    copy_all(opts, source_dir, config_dir, True)

    change_owner(opts, config_dir, user, group, True)

    disk_base_dir = swift_disk_base_dir(opts)

    search_replace = {}
    search_replace['<your-user-name>'] = user
    dir_replace(opts, config_dir, '*.conf', search_replace)

    search_replace = {}
    search_replace['/srv/1/node'] = '%s/%s_1/node' % (disk_base_dir, user)
    search_replace['/srv/2/node'] = '%s/%s_2/node' % (disk_base_dir, user)
    search_replace['/srv/3/node'] = '%s/%s_3/node' % (disk_base_dir, user)
    search_replace['/srv/4/node'] = '%s/%s_4/node' % (disk_base_dir, user)
    dir_replace_all(opts, config_dir, search_replace)

    home_local_bin = swift_home_local_bin_dir(opts)

    """
    EXPORT_SWIFT1_PATH="export PATH=${PATH}:${SWIFT1_USER_LOCAL_BIN}:${SWIFT1_USER_HOME}/swift/bin"

    su - ${SWIFT1_USER} -c 'cd ${SWIFT1_USER_HOME}/swift;'
    python setup.py develop --user
    #PJD: mistake on next line (mixup of SWIFT1 and SWIFT2)
    cd ${SWIFT1_USER_HOME}; chown -R ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT2_USER_LOCAL_BIN}
    cd ${SWIFT1_REPO_DIR}/doc/saio/bin; cp * ${SWIFT1_USER_LOCAL_BIN}; cd -

    cd ${SWIFT1_REPO_DIR}/doc/saio/bin; cp * ${SWIFT1_USER_LOCAL_BIN}; cd -

    cd ${SWIFT1_USER_LOCAL_BIN}; 
    rm resetswift;
    """
    file_to_delete = os.path.join(home_local_bin, 'resetswift')
    delete_file_if_exists(opts, file_to_delete)

    #============================    START   ======================
    mount_base_dir = swift_mount_base_dir(opts)
    """
    swift-init all stop
    # Remove the following line if you did not set up rsyslog for individual logging:
    umount /mnt/sdb*
    # If you are using a loopback device set SAIO_BLOCK_DEVICE to "/srv/swift-disk"
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk1}
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk2}
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk3}
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk4}
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk5}
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk6}
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk7}
    mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-/srv/swift1-disk8}
    mount /mnt/sdb*
    mkdir -p /mnt/sdb1/swift1_1 /mnt/sdb1/swift1_2 /mnt/sdb1/swift1_3 /mnt/sdb1/swift1_4
    mkdir -p /mnt/sdb5/swift1_5 /mnt/sdb6/swift1_6 /mnt/sdb7/swift1_7 /mnt/sdb8/swift1_8

    chown -R swift1:swift /mnt/sdb*
    mkdir -p /srv/swift1_1/node/sdb1 /srv/swift1_5/node/sdb5 \
             /srv/swift1_2/node/sdb2 /srv/swift1_6/node/sdb6 \
             /srv/swift1_3/node/sdb3 /srv/swift1_7/node/sdb7 \
             /srv/swift1_4/node/sdb4 /srv/swift1_8/node/sdb8
    rm -f /var/log/debug /var/log/messages /var/log/rsyncd.log /var/log/syslog
    find /var/cache/swift1* -type f -name *.recon -exec rm -f {} \;
    if [ "`type -t systemctl`" == "file" ]; then
        systemctl restart rsyslog
        systemctl restart memcached
    else
        service rsyslog restart
        /etc/init.d/memcached restart swift1
    fi
    EOF
    """
    #=========================    STOP  =======================

    #chmod +x ${SWIFT1_USER_LOCAL_BIN}/*

    #**********************************************************************************************
    #MODIFICATIONS TO THE SECOND REPOSITORY
    # Changing the ports to 60** to 67** series
    # and modifying the paths to suit swift2
    #
    #TODO: refine sed scripts to work efficiently and avoid the rework of replacing the wrong updates
    #**********************************************************************************************
    #cd ${SWIFT1_REPO_DIR}; su - swift1;

    port_adjust = swift_port_adjust(opts)
    proxy_port_adjust = swift_proxy_port_adjust(opts)

    replacements = {}
    replacements['/etc/swift'] = '/etc/%s' % user
    replacements['/var/run/swift'] = '/var/run/%s' % user
    replacements['/var/cache/swift'] = '/var/cache/%s' % user
    replacements['/tmp/log/swift'] = '/tmp/%s_log/swift' % user
    replacements['/tmp'] = '/tmp/%s_tmp' % user
    replacements['8080'] = str(8080+proxy_port_adjust) 
    replacements['6010'] = str(6010+port_adjust)
    replacements['6020'] = str(6020+port_adjust)
    replacements['6030'] = str(6030+port_adjust)
    replacements['6040'] = str(6040+port_adjust)
    replacements['6011'] = str(6011+port_adjust)
    replacements['6021'] = str(6021+port_adjust)
    replacements['6031'] = str(6031+port_adjust)
    replacements['6041'] = str(6041+port_adjust)
    replacements['6012'] = str(6012+port_adjust)
    replacements['6022'] = str(6022+port_adjust)
    replacements['6032'] = str(6032+port_adjust)
    replacements['6042'] = str(6042+port_adjust)
    #replace_all
    print('replacements: %s' % repr(replacements))


def get_swift_users(opts):
    #TODO: implement get_swift_users
    return ['swift1']  #, 'swift2', 'swift3']


def swift_setup_environment(opts):
    print('setup swift user %s' % swift_user(opts))
    swift_create_directories(opts)
    swift_setup_configs(opts)


def main():
    opts = {}
    opts[SWIFT_GROUP_NAME] = 'swift'
    opts[SWIFT_FS_TYPE] = 'xfs'
    opts[SWIFT_MKFS_OPTIONS] = '-f'
    opts[SWIFT_DISK_SIZE_GB] = '1'
    opts[SWIFT_DISK_BASE_DIR] = '/srv'
    opts[SWIFT_DISK_COUNT] = '8'
    opts[SWIFT_MOUNT_BASE_DIR] = '/mnt'
    opts[SWIFT_CONFIG_BASE_DIR] = '/etc'
    opts[SWIFT_RUN_BASE_DIR] = '/var/run'
    opts[SWIFT_CACHE_BASE_DIR] = '/var/cache'
    opts[SWIFT_HOME_BASE_DIR] = '/home'
    opts[SWIFT_REMOTE_REPO] = 'https://github.com/openstack/swift'
    opts[SWIFT_MOUNT_OPTIONS] = 'loop,noatime,nodiratime,nobarrier,logbufs=8 0 0'
    opts[SWIFT_HOME_LOCAL_BIN] = '.local/bin'
    opts[SWIFT_REPO_NAME] = 'swift'
    opts[SWIFT_RUN_MODE] = RUN_MODE_LOGIC

    port_adjust = 100
    proxy_port_adjust = 10

    for swift_user in get_swift_users(opts):
        opts[SWIFT_USER_NAME] = swift_user
        opts[SWIFT_PORT_ADJUST] = port_adjust
        opts[SWIFT_PROXY_PORT_ADJUST] = proxy_port_adjust
        swift_setup_environment(opts)
        port_adjust += 100
        proxy_port_adjust += 10


if __name__=='__main__':
    main()

