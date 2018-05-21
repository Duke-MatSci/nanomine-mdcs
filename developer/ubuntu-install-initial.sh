#!/bin/bash
source ./ubuntu/checkosversion
source ./ubuntu/installdocker
source ./ubuntu/installmongo
source ./ubuntu/installpip
source ./ubuntu/installvirtualenv



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

echo "The install will now run when you press enter. Use Ctrl+C to terminate"
read
sudo apt-get update; sudo apt-get -y install python git curl vim

osisok=$(checkosversion)
if [[ $osisok != "yes" ]]; then
  echo "Please use ubuntu 18.04"
  echo "Sorry. Cannot continue NanoMine installation."
  exit
fi


echo "    Create a nanomine user"
sudo useradd -g nanomine -d /home/nanomine -m nanomine

echo "    Setting the password for the nanomine user."
echo "    The program will prompt for the new nanomine user\'s password twice."
echo "    Type something that can be remembered!!!"
echo "        If the password is forgotten later user 'sudo passwd nanomine' to update it."
sudo passwd nanomine

echo "    Add the current user $USER to the nanomine group for convenience"
sudo usermod -a -G nanomine $USER

echo "    Install pip the python package installer if necessary"
$(installpip)

echo "    Install virtualenv the python environment virtualizer if necessary"
$(installvirtualenv)

echo "    Install docker if necessary"
$(installdocker)

echo "    Install mongo if necessary"
$(installmongo)

echo "   Add current user $USER to docker group"
sudo usermod -a -G docker $USER

echo "   Add the nanomine user to the docker group"
sudo usermod -a -G docker nanomine

echo "   Install the vim editor"
$(installvim)

echo all done with phase 1



