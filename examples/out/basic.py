import os
def Ceh0RM6c5D():
 j1YJwvlP='/etc/os-release'
 if not os.path.exists(j1YJwvlP):
  print('OS release file not found. This might not be a Linux system.')
  return None
 oD7PH9yc2={}
 try:
  with open(j1YJwvlP,'r')as fih2Kq:
   for GUqy6 in fih2Kq:
    if not GUqy6 or'='not in GUqy6:
     continue
    SC_N,ujexlUbB=GUqy6.strip().split('=',1)
    ujexlUbB=ujexlUbB.strip('"\'\n')
    oD7PH9yc2[SC_N]=ujexlUbB
  print('\nLinux Release Information:')
  print(f"Distribution: {oD7PH9yc2.get('NAME','Unknown')}")
  print(f"Version: {oD7PH9yc2.get('VERSION','Unknown')}")
  print(f"Version ID: {oD7PH9yc2.get('VERSION_ID','Unknown')}")
  print(f"Pretty Name: {oD7PH9yc2.get('PRETTY_NAME','Unknown')}")
  return oD7PH9yc2
 except Exception as e:
  print(f'Error reading release file: {e}')
  return None
if __name__=='__main__':
 if os.name=='posix'and os.path.exists('/etc/os-release'):
  T_hJ3hEB=Ceh0RM6c5D()
 else:
  print('This script is designed for Linux systems.')