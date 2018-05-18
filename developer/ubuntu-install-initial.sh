#!/bin/bash
source ./ubuntu/checkosversion
source ./ubuntu/installpython
source ./ubuntu/installcurl
source ./ubuntu/installdocker
source ./ubuntu/installmongo
source ./ubuntu/installpip
source ./ubuntu/installgit
source ./ubuntu/installvim


osisok=$(checkosversion)
if [[ $osisok != "yes" ]]; then
  echo "Please use ubuntu 18.04"
  echo "Sorry. Cannot continue NanoMine installation."
  exit
fi

echo " "
echo "NanoMine Ubuntu Developer Install"
echo "---------------------------------"
echo "It may help to increase the size of the terminal"
echo "   window vertically and horizontally to see more text"
echo " -- then press enter"
read
echo "NOTES:"
echo "---------- READ THIS!! -----------------------"
echo "  WARNING - THIS INSTALL WILL CHANGE OVER TIME"
echo "   since the development process will change."
echo "   Be prepared to re-install the development system"
echo "     from time to time."
echo "  "
echo "  WARNING - this script does not install MATLAB"
echo "     or COMSOL. If either of those are needed"
echo "     each will have to be installed using product installers."
echo " "
echo "This is a TWO PHASE install."
echo "  "
echo "  ** This process uses 'sudo' so your password"
echo "      may be required to complete some commands."
echo "  "
echo "  The steps of the first phase will:"
echo " "

cmds[1]="echo sudo useradd nanomine"
text[1]="    Create a nanomine user"

cmds[2]="echo sudo passwd nanomine"
text[2]="    Prompt for the new nanomine user\'s password twice.\n        Type something that can be remembered!!!\n        If the password is forgotten later user 'sudo passwd nanomine' to update it."

cmds[3]="echo sudo usermod -a -G nanomine $USER"
text[3]="    Add the current user $USER to the nanomine group for convenience"

cmds[4]="$(installpython)"
text[4]="    Install python2 if necessary"

cmds[5]="$(installcurl)"
text[5]="    Install curl downloader"

cmds[6]="$(installpip)"
text[6]="    Install python package installer 'pip' if necessary"

cmds[7]="$(installvirtualenv)"
text[7]="    Install python environment virtualizer 'virtualenv' if necessary"

cmds[8]="$(installgit)"
text[8]="    Install git if necessary"

cmds[9]="$(installdocker)"
text[9]="    Install docker if necessary"

cmds[10]="$(installmongo)"
text[10]="    Install mongo if necessary"

cmds[11]="sudo usermod -a -G $USER docker"
text[11]="   Add current user $USER to docker group"

cmds[12]="sudo usermod -a -G nanomine docker"
text[12]="   Add the nanomine user to the docker group"

cmds[13]="$(installvim)"
text[13]="   Install the vim editor"

for i in "${!text[@]}"; do
  printf "${text[i]}\n"
  echo " "
done

echo "press enter after reading the notes above"
read

echo "The install will run when you press enter. Use Ctrl+C to terminate"
read

for i in "${!text[@]}"; do
  printf "${text[i]}\n" | tee -a nanomine_install.log
  eval("$(cmd[i]}")
done

