# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:48:27 2017

@author: mlopezd
"""

import pandas as pd
import os
import jinja2 as j2
import time

# Excel file with all the data
xls_data_file = "example.xlsx"

# Directory containing all the Jinja2 templates
template_directory = "./templates"

# Output directory where config files will be created
output_directory = "conf"

# Load the globals sheet into a list of dictionaries (will be only one dictionary as there's only one row in this sheet)
globals_list = pd.read_excel(xls_data_file,sheet_name='globals').to_dict(orient='records')

# Load the switches sheet into a list of dictionaries
switches_list = pd.read_excel(xls_data_file,sheet_name='switches').to_dict(orient='records')

# Load the vlans sheet into a list of dictionaries
vlans_list = pd.read_excel(xls_data_file,sheet_name='vlans').to_dict(orient='records')

# Load the interfaces sheet into a list of dictionaries
interfaces_list = pd.read_excel(xls_data_file,sheet_name='interfaces').to_dict(orient='records')

# Create an empty dictionary for the VLANs
vlantree = {}

# Populate first the vlan_tree dictionary with all networks as keys
for row in vlans_list:
    network = {row['network']: {}}
    vlantree.update(network)
    
# Then populate each network key with the corresponding VLANs data
for row in vlans_list:
    vlan = {row['vlanname']: row['vlanid']}
    vlantree[row['network']].update(vlan)

# Create an empty dictionary for the switches
switchtree = {}

# Populate first the switch_tree dictionary with all switches in the interfaces list as keys
for row in interfaces_list:
    switch = {row['switch']: {}}
    switchtree.update(switch)

# Then populate each switch key with the corresponding interfaces data
for row in interfaces_list:
    interface = {row['interface']: row}
    switchtree[row['switch']].update(interface)

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Create the parameters dictionary for each switch in the switches_list
for switch in switches_list: 
    
    # Create an empty parameters dictionary
    parameters_dict = {}
    
    # Populate the parameters dictionary with the current switch specific parameters
    parameters_dict.update(switch) 
    
    # Populate the parameters dictionary with the global parameters
    parameters_dict.update(globals_list[0]) 
    
    # Populate the parameters dictionary with all the vlans corresponding to the current switch network
    network_vlans = {'network_vlans': vlantree[switch['network']]}   
    parameters_dict.update(network_vlans) 
    
    # Load all the current switch interfaces data into a new dictionary
    switch_interfaces = switchtree[switch['switch']]
    
    # Populate the parameters dictionary with each interface data
    for interface, data in switch_interfaces.items():
        
        # Format the interface data to match Jinja2 template variables
        temp_dict = {"interface_" + str(interface) + "_description" : data['device'] + " - " + data['description'],
                     "interface_" + str(interface) + "_vlan" : str(int(data['vlanid'])),
                     }
        
        # Populate the parameters dictionary with the new interface formatted data
        parameters_dict.update(temp_dict)
        
    # Create the Jinja2 environment
    env = j2.Environment(loader=j2.FileSystemLoader(searchpath=template_directory))
    
    # Load the specific template for the current switch
    template = env.get_template(parameters_dict['template'])
    
    # Render the template with the parameters dictionary
    result = template.render(parameters_dict)
    
    # Create a file using the current switch name
    f = open(os.path.join(output_directory, parameters_dict['switch'] + ".txt"), "w")

    # Get current date and time to write it in the config file as generation time 
    date = time.strftime("%X") + " " + time.strftime("%x")
    f.write("! Generation time: " + date)
    f.write("\n!\n")
    
    # Write the template render result into the file
    f.write(result)
    
    # Close the file
    f.close()
    
    # Print some info
    print("Configuration '%s' created" % (parameters_dict['switch'] + ".txt"))

# All configuration files have been generated
print("DONE")