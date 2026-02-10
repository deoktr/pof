import os

def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""
    qpmvku = '/etc/os-release'
    if not os.path.exists(qpmvku):
        print('OS release file not found. This might not be a Linux system.')
        return None
    ayCWD = {}
    try:
        with open(qpmvku, 'r') as bnW:
            for UBrTZVp in bnW:
                if not UBrTZVp or '=' not in UBrTZVp:
                    continue
                amv, sX5sRamg = UBrTZVp.strip().split('=', 1)
                sX5sRamg = sX5sRamg.strip('"\'\n')
                ayCWD[amv] = sX5sRamg
        print('\nLinux Release Information:')
        print(f"Distribution: {ayCWD.get('NAME', 'Unknown')}")
        print(f"Version: {ayCWD.get('VERSION', 'Unknown')}")
        print(f"Version ID: {ayCWD.get('VERSION_ID', 'Unknown')}")
        print(f"Pretty Name: {ayCWD.get('PRETTY_NAME', 'Unknown')}")
        return ayCWD
    except Exception as e:
        print(f'Error reading release file: {e}')
        return None
if __name__ == '__main__':
    if os.name == 'posix' and os.path.exists('/etc/os-release'):
        Wvw = get_linux_release_info()
    else:
        print('This script is designed for Linux systems.')