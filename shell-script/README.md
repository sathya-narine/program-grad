Instructions to run the shell scripts
All the scripts requires execute permission, which could be done by:chmod +x *.sh

1. userinfo.sh expects one agrument - user name.
   ./userinfo <user_name>
   Ex ./userinfo.sh test
   adduser.sh adds test user, but the script has to be run as root.
   sudo -i
   ./adduser.sh 
2. healthcheck.sh
   This scipt doesnot require any arguments.
   ./healthcheck.sh
3. backupdir.sh expects two arguments,path to source directory and backup location.
   ./backupdir.sh <path_dir> <path_dst>
   Ex ./backupdir.sh /home/test/src /home/test/dst 
4. rename.sh
   This script expects two argument, path to drectory and prefix
   Ex ./rename.sh /home/test/src new
5. processmonitor.sh
   This script expects one argument that is process name.
   Ex ./processmonitor.sh bash
      ./processmonitor.sh date