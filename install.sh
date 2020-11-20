echo installation of mpm

sudo apt-get install unzip 
sudo apt-get install wget
sudo apt-get install git

varname="$(./mpm_tools/getMpmDir)" 

sudo cp -r $varname"/mpm_tools/" /usr/local/sbin
sudo cp -r $varname"/mpm_venv/" /usr/local/sbin
sudo cp $varname"/mpm" /usr/local/sbin
sudo cp $varname"/mpm.py" /usr/local/sbin
sudo chmod +777 /usr/local/sbin/mpm
echo installation finished, you can delete all the files of this directory 
echo to delete it automaticaly, press y, to quit, press n
read response
if [[ "$response" == "y" ]]
then 
    sudo rm -r  $varname
fi

echo "---------"
echo "---------"

echo now open a new terminal an run mpm 

exit
