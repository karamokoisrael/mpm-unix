varname="/usr/local/sbin" 
echo uninstalling mpm
sudo rm -r $varname"/mpm_venv/"
sudo rm $varname"/mpm" 
sudo rm $varname"/mpm.py" 
 
echo npm removed successfully 

sudo rm -r $varname"/mpm_tools/"

exit
