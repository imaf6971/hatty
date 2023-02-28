import os
import subprocess


def yes_or_no() -> bool:
    """Asks user for yes or no
    Returns True if 'y' and False otherwise"""
    return input('[y/n]: ') == 'y'


def exec_cmd(cmd: str, fallback: str):
    return_code = os.system(cmd)
    if return_code != 0:
        print(fallback)
        exit(return_code)


def ask_for_step(prompt: str, is_root: bool):
    print(prompt)
    if is_root:
        print('(That requires root privelegies)')
    ans = yes_or_no()
    if ans == False:
        print('Ok, skipping...')
    return ans


def exec_batch(prompt: str, cmds: list[str], is_root = True, fallback: str = 'Some error! Exiting...'):
    ans = ask_for_step(prompt, is_root)
    if ans == False:
        return
    for cmd in cmds:
        exec_cmd(cmd, fallback)


def exec_step(prompt: str, cmd: str, is_root: bool = True, fallback: str = 'Some error! Exiting...'):
    ans = ask_for_step(prompt, is_root)
    if ans == False:
        return
    exec_cmd(cmd, fallback)


def install_step(package_list: str | list[str]):
    packages = ''
    if isinstance(package_list, list): 
        packages = ' '.join(package_list)
    elif isinstance(package_list, str):
        packages = package_list
    exec_step(prompt=f'Do you want to install {packages}?',
              cmd=f'sudo dnf install -y {packages}', is_root=True,
              fallback=f'Error while installing {packages}! Exiting...')


if __name__ == "__main__":
    print('Welcome to hatty! Do you want to install everything?')
    inp = input('[y/n]: ')
    if inp != 'y':
        print('User cancelled installation, extiting...')
        exit()
    # patching dnf config
    print('Do you want hatty to path your dnf config for faster dnf speed?')
    inp = input('[y/n]: ')
    if inp == 'y':
        patch_result = subprocess.call(['sudo', 'python3', './patch_dnf_config.py'])
        if patch_result != 0:
            print('Error while patching dnf config, exiting...')
            exit(1)
    # running dnf update
    exec_step(prompt='Do you want hatty to update your system?', cmd='sudo dnf update')

    # add RPM Fusion Repositories
    exec_step(prompt='Do you want to add RPM Fusion Free repository?',
              cmd="sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm")
    exec_step('Do you want to add RPM Fusion Nonfree repository?',
              cmd="sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
    exec_step(prompt='Do you want to install Third Party Repositories?',
              cmd='sudo dnf install fedora-workstation-repositories')

    exec_step(prompt='Do you want to install Google Chrome?',
              cmd='sudo dnf config-manager --set-enabled google-chrome && sudo dnf install google-chrome')

    install_step('git')

    exec_step(prompt='Do you want to install nodejs?',
              cmd='sudo dnf module install nodejs:18/common')

    exec_step(prompt='Do you want to install rust?',
              cmd="curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")

    install_step(['neovim', 'python3-neovim'])

    install_step('fish')
    exec_step('Do you want to change your default shell to fish?',
              cmd='chsh -s /usr/bin/fish', is_root=False)
    # TODO: clone fish configs
    # exec_step('Do you want to clone my .config/fish ?', is_root=False)
    install_step('bat')
    install_step('alacritty')
    install_step('lf')
    install_step('lsd')

    exec_batch('Do you want to install Visual Studio Code?', [
        'sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc',
        'sudo sh -c \'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo\'',
        'dnf check-update',
        'sudo dnf install -y code',])
