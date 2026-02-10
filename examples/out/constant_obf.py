e2FmYvKjoo='VERSION'
UqtGOwHMbF="r"
blbdwyKJ=None
EoekDswy55="/etc/os-release"
wVg='NAME'
zZ3maSLJ=__name__
ISOM7r="posix"
uYJiP=Exception
MTK4jLW2xv="\nLinux Release Information:"
Q1t1Pa=print
qTMSOm="\"'\n"
ukQ5UGbX='Unknown'
id69Z="__main__"
NU6drFex8D='PRETTY_NAME'
gCac='VERSION_ID'
PerHqKoE=1
pjD_OXbg3="This script is designed for Linux systems."
e5wKHt0=open
uWFg="="
sz5FH_5="OS release file not found. This might not be a Linux system."
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file=EoekDswy55

    if not os.path.exists(release_file):
        Q1t1Pa(sz5FH_5)
        return blbdwyKJ

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with e5wKHt0(release_file,UqtGOwHMbF)as f:
            for line in f:
                if not line or uWFg not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split(uWFg,PerHqKoE)

                # Remove quotes from value
                value=value.strip(qTMSOm)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        Q1t1Pa(MTK4jLW2xv)
        Q1t1Pa(f"Distribution: {release_info.get(wVg,ukQ5UGbX)}")
        Q1t1Pa(f"Version: {release_info.get(e2FmYvKjoo,ukQ5UGbX)}")
        Q1t1Pa(f"Version ID: {release_info.get(gCac,ukQ5UGbX)}")
        Q1t1Pa(f"Pretty Name: {release_info.get(NU6drFex8D,ukQ5UGbX)}")

        return release_info

    except uYJiP as e:
        Q1t1Pa(f"Error reading release file: {e}")
        return blbdwyKJ


        # Main execution
if zZ3maSLJ==id69Z:
# Check if running on Linux
    if os.name==ISOM7r and os.path.exists(EoekDswy55):
        release_details=get_linux_release_info()
    else:
        Q1t1Pa(pjD_OXbg3)
