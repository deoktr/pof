Dss2X9jhA="This script is designed for Linux systems."
rmW='PRETTY_NAME'
fFh=1
BVXyUt="__main__"
jmE2SYVmOq="/etc/os-release"
P9_tubnhU='NAME'
KLzmXdwGfs=__name__
cqF_='VERSION'
SV_D_1=open
zMo='Unknown'
jDNJt="posix"
EZeW=print
SYlw5=None
jFYOJ='VERSION_ID'
k1oTsq4N="OS release file not found. This might not be a Linux system."
ELjbxoZ3="\nLinux Release Information:"
U2Eln_ht=Exception
JOq="\"'\n"
yCquhP2Sw="="
vOQIu6Gzmx="r"
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file=jmE2SYVmOq

    if not os.path.exists(release_file):
        EZeW(k1oTsq4N)
        return SYlw5

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with SV_D_1(release_file,vOQIu6Gzmx)as f:
            for line in f:
                if not line or yCquhP2Sw not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split(yCquhP2Sw,fFh)

                # Remove quotes from value
                value=value.strip(JOq)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        EZeW(ELjbxoZ3)
        EZeW(f"Distribution: {release_info.get(P9_tubnhU,zMo)}")
        EZeW(f"Version: {release_info.get(cqF_,zMo)}")
        EZeW(f"Version ID: {release_info.get(jFYOJ,zMo)}")
        EZeW(f"Pretty Name: {release_info.get(rmW,zMo)}")

        return release_info

    except U2Eln_ht as e:
        EZeW(f"Error reading release file: {e}")
        return SYlw5


        # Main execution
if KLzmXdwGfs==BVXyUt:
# Check if running on Linux
    if os.name==jDNJt and os.path.exists(jmE2SYVmOq):
        release_details=get_linux_release_info()
    else:
        EZeW(Dss2X9jhA)
