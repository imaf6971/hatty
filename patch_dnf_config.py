import os

def is_root():
    return os.getuid() == 0


def check_root():
    if not is_root():
        print('Error! This script should be runned with root')
        exit(1)


def is_already_patched():
    with open('/etc/dnf/dnf.conf') as dnf_conf:
        config_content = dnf_conf.read()
        return ("max_parallel_downloads=10" in config_content) and ("fastestmirror=True" in config_content)


def check_already_patched():
    if is_already_patched():
        print('dnf.conf is already patched')
        exit(0)
 

def append_patch():
    with open('/etc/dnf/dnf.conf', "a") as dnf_conf:
        dnf_conf.write('\nmax_parallel_downloads=10')
        dnf_conf.write('\nfastestmirror=True')


if __name__ == "__main__":
    check_root()
    check_already_patched()
    append_patch()

