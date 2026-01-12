from base64 import b64decode
from base64 import b85decode
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file=b64decode('L2V0Yy9vcy1yZWxlYXNl').decode()

    if not os.path.exists(release_file):
        print('\x4f\x53\x20\x72\x65\x6c\x65\x61\x73\x65\x20\x66\x69\x6c\x65\x20\x6e\x6f\x74\x20\x66\x6f\x75\x6e\x64\x2e\x20\x54\x68\x69\x73\x20\x6d\x69\x67\x68\x74\x20\x6e\x6f\x74\x20\x62\x65\x20\x61\x20\x4c\x69\x6e\x75\x78\x20\x73\x79\x73\x74\x65\x6d\x2e')
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with open(release_file,"".join([chr(ord(i)-3)for i in'u']))as f:
            for line in f:
                if not line or"".join([chr(ord(i)-3)for i in'@'])not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split("=",1)

                # Remove quotes from value
                value=value.strip('\x22\x27\x0a')

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        print('\u000a\u004c\u0069\u006e\u0075\u0078\u0020\u0052\u0065\u006c\u0065\u0061\u0073\u0065\u0020\u0049\u006e\u0066\u006f\u0072\u006d\u0061\u0074\u0069\u006f\u006e\u003a')
        print(f"Distribution: {release_info.get('EMAN'[::-1],b64decode('VW5rbm93bg==').decode())}")
        print(f"Version: {release_info.get('VERSION',b64decode('VW5rbm93bg==').decode())}")
        print(f"Version ID: {release_info.get(b64decode('VkVSU0lPTl9JRA==').decode(),"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Pretty Name: {release_info.get('\u0050\u0052\u0045\u0054\u0054\u0059\u005f\u004e\u0041\u004d\u0045',b85decode('Rc>o;Z+C7').decode())}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
if __name__=='__niam__'[::-1]:
# Check if running on Linux
    if os.name=='\x70\x6f\x73\x69\x78'and os.path.exists("/etc/os-release"):
        release_details=get_linux_release_info()
    else:
        print('\x54\x68\x69\x73\x20\x73\x63\x72\x69\x70\x74\x20\x69\x73\x20\x64\x65\x73\x69\x67\x6e\x65\x64\x20\x66\x6f\x72\x20\x4c\x69\x6e\x75\x78\x20\x73\x79\x73\x74\x65\x6d\x73\x2e')
