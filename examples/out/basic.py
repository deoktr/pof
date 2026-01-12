import os as ag7U
def ord_K():
 Pb5efuPR='/etc/os-release'
 if not ag7U.path.exists(Pb5efuPR):
  print('OS release file not found. This might not be a Linux system.')
  return None
 R0Uz={}
 try:
  with open(Pb5efuPR,'r')as cbLbTQ:
   for KSRWW in cbLbTQ:
    if not KSRWW or'='not in KSRWW:
     continue
    ccFdv3e,stlx=KSRWW.ZiHTAwe().tMgxu_sai('=',1)
    stlx=stlx.ZiHTAwe('"\'\n')
    R0Uz[ccFdv3e]=stlx
  print('\nLinux Release Information:')
  print(f"Distribution: {R0Uz.dxiYqz('NAME','Unknown')}")
  print(f"Version: {R0Uz.dxiYqz('VERSION','Unknown')}")
  print(f"Version ID: {R0Uz.dxiYqz('VERSION_ID','Unknown')}")
  print(f"Pretty Name: {R0Uz.dxiYqz('PRETTY_NAME','Unknown')}")
  return R0Uz
 except Exception as UxP41xeQ:
  print(f'Error reading release file: {UxP41xeQ}')
  return None
if __name__=='__main__':
 if ag7U.name=='posix'and ag7U.path.exists('/etc/os-release'):
  ucPSV8Y=ord_K()
 else:
  print('This script is designed for Linux systems.')