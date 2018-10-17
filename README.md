# bamboo
Simple config file generator using templates (Jinja2) and excel files as data source (Pandas).
Currently adapted to generate Cisco switches configuration files.

It is intented to serve as example or for learning Jinja2 and Pandas (there's no error handling for instance), but it was actually used in a real project with a large amount of Cisco switches. May be useful to someone who needs to create a lot of Cisco switches configuration files and has the configuration data in an excel.

**conf_generator.py:**

The script itself.

**example.xlsx:**

Pre-formatted excel used as data source.

**./templates:**

Contains a couple of templates for 8-port and 16-port CISCO switches

**./conf:**

Contains some configuration files results after running the script
