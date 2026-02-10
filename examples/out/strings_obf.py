from base64 import b64decode
from base64 import b85decode
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file="/etc/os-release"

    if not os.path.exists(release_file):
        print('.metsys xuniL a eb ton thgim sihT .dnuof ton elif esaeler SO'[::-1])
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with open(release_file,"r")as f:
            for line in f:
                if not line or b85decode('Jp').decode()not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split('='[::-1],1)

                # Remove quotes from value
                value=value.strip('\u0022\u0027\u000a')

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        print(b64decode('CkxpbnV4IFJlbGVhc2UgSW5mb3JtYXRpb246').decode())
        print(f"Distribution: {release_info.get('NAME',"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Version: {release_info.get('\u0056\u0045\u0052\u0053\u0049\u004f\u004e',"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Version ID: {release_info.get(b64decode('VkVSU0lPTl9JRA==').decode(),"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Pretty Name: {release_info.get("".join([chr(ord(i)-3)for i in'SUHWW\\bQDPH']),"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
if __name__==b64decode('X19tYWluX18=').decode():
# Check if running on Linux
    if os.name==b64decode('cG9zaXg=').decode()and os.path.exists(b85decode('FJ*LNFK=@#a%F5~VRK~').decode()):
        release_details=get_linux_release_info()
    else:
        print('.smetsys xuniL rof dengised si tpircs sihT'[::-1])
