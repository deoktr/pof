from base64 import b64decode
from base64 import b85decode
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file='\x2f\x65\x74\x63\x2f\x6f\x73\x2d\x72\x65\x6c\x65\x61\x73\x65'

    if not os.path.exists(release_file):
        print(b85decode('Pg5XrWo%_(b7dfAX>4U6Zf|rTW^Z+FWG*07XlZjGZE0s{bRceTbRc47AYmX(X>N6RAai+hbY*QW').decode())
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with open(release_file,'\x72')as f:
            for line in f:
                if not line or'\u003d'not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split("=",1)

                # Remove quotes from value
                value=value.strip("\"'\n")

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        print(':noitamrofnI esaeleR xuniL\n'[::-1])
        print(f"Distribution: {release_info.get('\x4e\x41\x4d\x45',b64decode('VW5rbm93bg==').decode())}")
        print(f"Version: {release_info.get(b64decode('VkVSU0lPTg==').decode(),'\u0055\u006e\u006b\u006e\u006f\u0077\u006e')}")
        print(f"Version ID: {release_info.get('DI_NOISREV'[::-1],"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Pretty Name: {release_info.get("".join([chr(ord(i)-3)for i in'SUHWW\\bQDPH']),"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
if __name__=="".join([chr(ord(i)-3)for i in'bbpdlqbb']):
# Check if running on Linux
    if os.name=='\u0070\u006f\u0073\u0069\u0078'and os.path.exists("".join([chr(ord(i)-3)for i in'2hwf2rv0uhohdvh'])):
        release_details=get_linux_release_info()
    else:
        print(b85decode('RA^~)Aai4KX>fEPX>%ZCWpim~Ze?U3W^ZyJOlfX)cp!6mb97~Gb1n').decode())
