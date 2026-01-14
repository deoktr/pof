Lq0Uq="r"
SUAk='VERSION'
JAnqL4="OS release file not found. This might not be a Linux system."
KzgfDf="__main__"
U_bvmfZOQ=None
oWPrrs2Q5=open
NmcqAL4="/etc/os-release"
vgogGd=1
Za4eqlVOq="\"'\n"
KZSf="="
paBf3ru=__name__
qp9='NAME'
pPnH=Exception
GYw0='PRETTY_NAME'
Q_aog="posix"
VI7gU5v='Unknown'
fUN6vbBlW='VERSION_ID'
AbJYTcX="\nLinux Release Information:"
SnAK_="This script is designed for Linux systems."
iTRZ=print
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file=NmcqAL4

    if not os.path.exists(release_file):
        iTRZ(JAnqL4)
        return U_bvmfZOQ

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with oWPrrs2Q5(release_file,Lq0Uq)as f:
            for line in f:
                if not line or KZSf not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split(KZSf,vgogGd)

                # Remove quotes from value
                value=value.strip(Za4eqlVOq)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        iTRZ(AbJYTcX)
        iTRZ(f"Distribution: {release_info.get(qp9,VI7gU5v)}")
        iTRZ(f"Version: {release_info.get(SUAk,VI7gU5v)}")
        iTRZ(f"Version ID: {release_info.get(fUN6vbBlW,VI7gU5v)}")
        iTRZ(f"Pretty Name: {release_info.get(GYw0,VI7gU5v)}")

        return release_info

    except pPnH as e:
        iTRZ(f"Error reading release file: {e}")
        return U_bvmfZOQ


        # Main execution
if paBf3ru==KzgfDf:
# Check if running on Linux
    if os.name==Q_aog and os.path.exists(NmcqAL4):
        release_details=get_linux_release_info()
    else:
        iTRZ(SnAK_)
