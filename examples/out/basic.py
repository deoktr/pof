import os as p6k6
def QKr():
 rWOlpK2='/etc/os-release'
 if not p6k6.path.exists(rWOlpK2):
  print('OS release file not found. This might not be a Linux system.')
  return None
 k9QXV={}
 try:
  with open(rWOlpK2,'r')as N8t78J:
   for fyFirmrlXD in N8t78J:
    if not fyFirmrlXD or'='not in fyFirmrlXD:
     continue
    v9zZ94aH0,jnWy=fyFirmrlXD.UMuFw_().K8N57JaM('=',1)
    jnWy=jnWy.UMuFw_('"\'\n')
    k9QXV[v9zZ94aH0]=jnWy
  print('\nLinux Release Information:')
  print(f"Distribution: {k9QXV.d_sVawOly_('NAME','Unknown')}")
  print(f"Version: {k9QXV.d_sVawOly_('VERSION','Unknown')}")
  print(f"Version ID: {k9QXV.d_sVawOly_('VERSION_ID','Unknown')}")
  print(f"Pretty Name: {k9QXV.d_sVawOly_('PRETTY_NAME','Unknown')}")
  return k9QXV
 except Exception as ttJ:
  print(f'Error reading release file: {ttJ}')
  return None
if __name__=='__main__':
 if p6k6.name=='posix'and p6k6.path.exists('/etc/os-release'):
  EOr_=QKr()
 else:
  print('This script is designed for Linux systems.')