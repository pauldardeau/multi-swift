#
#
# TODO: call setup_bashrc
# TODO: look for duplicated code/logic
# TODO: check that all functions are called
# TODO: setup of memcached
#

import glob
import os
import os.path
import pwd
import shutil
import sys


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
SWIFT_DEVICE_LETTER = 'swift_device_letter'


def swift_device_letter(opts):
    return opts[SWIFT_DEVICE_LETTER]


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
        cmd = '%s %s %s' % (mkfs_command(opts),
                            swift_mkfs_options(opts),
                            fs_path)
        if swift_is_preview_mode(opts):
            print(cmd)
        else:
            os.system(cmd)


def create_file_with_gb_size(opts, file_path, gb_size):
    gb_size_in_bytes = GB_BYTES * gb_size
    if swift_is_logic_mode(opts):
        print('create_file_with_gb_size: %s %s (%s)' % (file_path,
                                                        gb_size,
                                                        str(gb_size_in_bytes)))
    elif swift_is_exec_mode(opts):
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


def copy_dir_files(opts, src_dir, dest_dir):
    names = os.listdir(src_dir)
    for name in os.listdir(src_dir):
        srcname = os.path.join(src_dir, name)
        if not os.path.isdir(srcname):
            shutil.copy2(srcname, os.path.join(dest_dir, name))


def copy_all(opts, src_dir, dest_dir, recurse=False):
    if swift_is_logic_mode(opts):
        print('copy_all: %s %s' % (src_dir, dest_dir))
    if swift_is_preview_mode(opts):
        if recurse:
            print('cp -R %s/* %s' % (src_dir, dest_dir))
        else:
            print('cp %s/* %s' % (src_dir, dest_dir))
    elif swift_is_exec_mode(opts):
        if recurse:
            shutil.copytree(src_dir, dest_dir)
        else:
            copy_dir_files(src_dir, dest_dir)


def append_to_file(opts, text_to_append, file_path):
    if swift_is_logic_mode(opts):
        print('append_to_file: %s' % file_path)
        print('%s...' % text_to_append[0:40])
    elif swift_is_preview_mode(opts):
        print("open('%s', 'a'); print('%s...')" % (file_path, text_to_append[0:40]))
    elif swift_is_exec_mode(opts):
        with open(file_path, "a") as f:
            f.write(text_to_append)


def user_exists(opts, user_name):
    try:
        pwd.getpwnam(user_name)
        return True
    except KeyError:
        return False


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


def mount_all_filesystems(opts):
    if swift_is_logic_mode(opts):
        print('mount all filesystems')
    else:
        cmd = 'mount -a'
        if swift_is_preview_mode(opts):
            print(cmd)
        elif swift_is_exec_mode(opts):
            os.system(cmd)


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


def file_replace(opts, file_path, replacements):
    with open(file_path, 'w') as f:
        file_contents = f.read()
        new_file_contents = replace_all(opts,
                                        file_contents,
                                        replacements)
        if new_file_contents != file_contents:
            f.write(new_file_contents)


def dir_replace_all(opts, dir_path, replacements):
    if swift_is_logic_mode(opts):
        print('dir_replace_all: %s %s' % (dir_path, repr(replacements)))
    elif swift_is_preview_mode(opts):
        #TODO: implement preview mode of dir_replace_all
        pass
    elif swift_is_exec_mode(opts):
        dir_listings = os.listdir(dir_path)
        for dir_listing in dir_listings:
            path_dir_listing = os.path.join(dir_path, dir_listing)
            # it would be good to verify that file is a text file
            if os.path.isfile(path_dir_listing): 
                file_replace(opts, path_dir_listing, replacements)


def dir_replace(opts, dir_path, file_spec, replacements):
    if swift_is_logic_mode(opts):
        print('dir_replace: %s %s %s' % (dir_path,
                                         file_spec,
                                         repr(replacements)))
    elif swift_is_preview_mode(opts):
        #TODO: implement preview mode of dir_replace
        pass
    elif swift_is_exec_mode(opts):
        if file_spec == '*':
            dir_replace_all(opts, dir_path, replacements)
        else:
            for listing_entry in glob.glob(file_spec):
                path_listing_entry = os.path.join(dir_path, listing_entry)
                if os.path.isfile(path_listing_entry):
                    file_replace(opts, path_listing_entry, replacements)


def replace_all(opts, s, replacements):
    if swift_is_logic_mode(opts):
        print('replace_all: %s %s' % (s, repr(replacements)))
        return s
    elif swift_is_preview_mode(opts):
        #TODO: implement preview mode of replace_all
        return s
    elif swift_is_exec_mode(opts):
        for k, v in replacements.items():
            s = s.replace(k,v)
        return s


def swift_fs_type(opts):
    return opts[SWIFT_FS_TYPE]


def swift_mount_options(opts):
    return opts[SWIFT_MOUNT_OPTIONS]


def fstab_entry(opts, disk_number):
    device_spec = '%s/%s-disk%d' % (swift_disk_base_dir(opts),
                                    swift_user(opts),
                                    disk_number)
    dev_letter = swift_device_letter(opts)
    mount_point = '%s/sd%s%s' % (swift_mount_base_dir(opts),
                                 str(dev_letter),
                                 str(disk_number))
    return '%s %s %s %s' % (device_spec,
                            mount_point,
                            swift_fs_type(opts),
                            swift_mount_options(opts))


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


def setup_fstab_entries(opts):
    fstab_entries = ''
    for x in range(swift_disk_count(opts)):
        fstab_entries += fstab_entry(opts, x + 1) 
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
    dev_letter = swift_device_letter(opts)

    for x in range(swift_disk_count(opts)):
        disk_num = '%d' % (x+1)
        SWIFT1_DISK_DIR = '%s/%s_%s' % (disk_base_dir, user_name, disk_num)
        disk_dir = '%s/%s_%s' % (disk_base_dir, user_name, disk_num)
        mount_dir = '%s/sd%s%s/%s_%s' % (mount_base_dir,
                                         str(dev_letter),
                                         disk_num,
                                         user_name,
                                         disk_num)
        create_dir(opts, mount_dir) 
        change_owner(opts, mount_dir, user_name, group_name)
        create_link(opts, mount_dir, disk_dir)
        change_owner(opts, disk_dir, user_name, group_name)

    cache_base_dir = swift_cache_base_dir(opts)
    create_dir(opts, cache_base_dir)

    mount_all_filesystems(opts)

    for x in range(swift_disk_count(opts)):
        disk_num = '%d' % (x+1)
        dir_path = '%s/%s_%s/node/sd%s%s' % (disk_base_dir,
                                            user_name,
                                            disk_num,
                                            str(dev_letter),
                                            disk_num)
        create_dir(opts, dir_path)

    #PJD: SWIFT1_DISK_DIR doesn't seem correct here
    #chown -R ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT1_DISK_DIR}
    change_owner(opts, SWIFT1_DISK_DIR, user_name, group_name, True)


def exec_as_user(opts, cmd, exec_user):
    if swift_is_logic_mode(opts):
        print('exec (%s): %s' % (exec_user, cmd))
    else:
        cmd = 'su - %s -c %s' % (exec_user, cmd)
        if swift_is_preview_mode(opts):
            print(cmd)
        elif swift_is_exec_mode(opts):
            os.system(cmd)


def setup_local_swift_repo(opts):
    if swift_is_logic_mode(opts):
        print('setup local swift repo')
    user_home_dir = swift_home_dir(opts)
    if dir_exists(user_home_dir):
        cmd = 'cd %s && git pull' % user_home_dir
    else:
        cmd = 'git clone %s' % swift_remote_repo(opts)
    exec_as_user(opts, cmd, swift_user(opts))


def setup_bashrc(opts):
    if swift_is_logic_mode(opts):
        print('setup bashrc with config options')
    else:
        user = swift_user(opts)
        home_dir = swift_home_dir(opts)
        login_cfg_file = os.path.join(home_dir, '.bashrc')
        test_config_file = os.path.join(swift_config_dir(opts), 'test.conf')
        egg_cache_dir = os.path.join(home_dir, 'tmp')
        disk_path = 'swift-disk1'  #TODO: fix this (disk1)
        saio_block_device = os.path.join(swift_disk_base_dir(opts),disk_path)
        stmts  = 'export SAIO_BLOCK_DEVICE=%s\n' % saio_block_device
        stmts += 'export SWIFT_TEST_CONFIG_FILE=%s\n' % test_config_file
        stmts += 'export PATH=${PATH}:$HOME/%s\n' % opts[SWIFT_HOME_LOCAL_BIN]
        stmts += 'export PYTHON_EGG_CACHE=%s\n' % egg_cache_dir
        append_to_file(opts, stmts, login_cfg_file)


def make_dir_files_executable(opts, dir_path):
    if swift_is_logical_mode(opts):
        print('make executable %s/*' % dir_path)
    else:
        cmd = 'chmod +x %s/*' % dir_path
        if swift_is_preview_mode(opts):
            print(cmd)
        elif swift_is_exec_mode(opts):
            os.system(cmd)


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
    su - ${SWIFT1_USER} -c 'cd ${SWIFT1_USER_HOME}/swift;'
    python setup.py develop --user
    #PJD: mistake on next line (mixup of SWIFT1 and SWIFT2)
    cd ${SWIFT1_USER_HOME}; chown -R ${SWIFT1_USER}:${SWIFT_GROUP} ${SWIFT2_USER_LOCAL_BIN}
    cd ${SWIFT1_REPO_DIR}/doc/saio/bin; cp * ${SWIFT1_USER_LOCAL_BIN}; cd -
    """

    resetswift_file = os.path.join(home_local_bin, 'resetswift')
    delete_file_if_exists(opts, resetswift_file)

    mount_base_dir = swift_mount_base_dir(opts)
    disk_base_dir = swift_disk_base_dir(opts)

    #TODO: change out hard-coded values in resetswift
    stmts = ''
    stmts += '#!/bin/sh\n'
    stmts += 'swift-init all stop\n'
    stmts += '# Remove the following line if you did not set up rsyslog for individual logging:\n'
    stmts += 'sudo umount %s/sdb*\n' % mount_base_dir
    #TODO: correct comment below
    stmts += '# If you are using a loopback device set SAIO_BLOCK_DEVICE to "/srv/swift-disk"\n'
    #TODO: looks like mistake in expression below

    for x in range(swift_disk_count(opts)):
        disk_num = str(x + 1)
        stmts += 'mkfs.xfs -f ${SAIO_BLOCK_DEVICE:-%s/%s-disk%s}\n' % (disk_base_dir,user,disk_num)

    stmts += 'mount %s/sdb*\n' % mount_base_dir

    for x in range(swift_disk_count(opts)):
        disk_num = str(x + 1)
        stmts += 'mkdir -p %s/sdb%s/%s_%s\n' % (mount_base_dir,disk_num,user,disk_num)

    stmts += '\n'
    stmts += 'chown -R %s:%s %s/sdb*\n' % (user,group, mount_base_dir)

    for x in range(swift_disk_count(opts)):
        disk_num = str(x + 1)
        stmts += 'mkdir -p %s/%s_%s/node/sdb%s\n' % (disk_base_dir,user,disk_num,disk_num)

    #TODO: these are system level files. probably not the correct thing
    stmts += 'rm -f /var/log/debug\n'
    stmts += 'rm -f /var/log/messages\n'
    stmts += 'rm -f /var/log/rsyncd.log\n'
    stmts += 'rm -f /var/log/syslog\n'

    stmts += 'find /var/cache/%s* -type f -name *.recon -exec rm -f {} \;\n' % user

    stmts += 'if [ "`type -t systemctl`" == "file" ]; then\n'
    stmts += '    systemctl restart rsyslog\n'
    stmts += '    systemctl restart memcached\n'
    stmts += 'else\n'
    stmts += '    service rsyslog restart\n'
    stmts += '    /etc/init.d/memcached restart %s\n' % user
    stmts += 'fi\n'

    if swift_is_logical_mode(opts):
        print('create new resetswift script at %s' % resetswift_file)
    elif swift_is_preview_mode(opts):
        print('cat >> %s << EOF\n' % resetswift_file)
        print(stmts)
        print('EOF\n')
    elif swift_is_exec_mode(opts):
        with open(resetswift_file, 'w') as f:
            f.write(stmts)

    make_dir_files_executable(opts, home_local_bin)

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

    if swift_is_logic_mode(opts):
        print('replacements: %s' % repr(replacements))
    elif swift_is_preview_mode(opts):
        #TODO: implement preview mode
        pass
    elif swift_is_exec_mode(opts):
        #TODO: implement exec mode
        #cd ${SWIFT1_REPO_DIR}; su - swift1;
        pass


def get_swift_users(opts):
    #TODO: implement get_swift_users
    return ['swift1']  #, 'swift2', 'swift3']


def swift_setup_environment(opts):
    if swift_is_logic_mode(opts):
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
    opts[SWIFT_RUN_MODE] = RUN_MODE_PREVIEW

    port_adjust = 100
    proxy_port_adjust = 10
    device_letter = 'b'  # as in sdb2
    #                              ^
    #                              |
    #                              |

    swift_users = get_swift_users(opts)

    # check whether all users exist in system
    non_existent_users = []

    for swift_user in swift_users:
        if not user_exists(opts, swift_user):
            non_existent_users.append(swift_user)

    if len(non_existent_users) > 0:
        print('error: the following users are not valid os users')
        for invalid_user in non_existent_users:
            print(invalid_user)
        sys.exit(1)

    # setup swift for each system user
    for swift_user in get_swift_users(opts):
        opts[SWIFT_USER_NAME] = swift_user
        opts[SWIFT_PORT_ADJUST] = port_adjust
        opts[SWIFT_PROXY_PORT_ADJUST] = proxy_port_adjust
        opts[SWIFT_DEVICE_LETTER] = device_letter
        swift_setup_environment(opts)
        port_adjust += 100
        proxy_port_adjust += 10
        # advance device letter (e.g., 'b' to 'c')
        device_letter = chr(ord(device_letter)+1)


if __name__=='__main__':
    main()

