# OpenWanderer Elevation Script 

This script gives each panorama an elevation, using the Terrarium elevation tiles on AWS.

Note that other server-side processing tasks will be run as separate scripts. For example, see [the anonymiser script](https://github.com/openwanderer/anon)

## Installing

The script is being developed using Python 3.6. 

For now, it requires the `python-dotenv`, `pillow`, `psycopg2` and `requests` modules, which can be installed using `pip3` e.g.:

```
pip3 install python-dotenv
pip3 install requests
pip3 install pillow
pip3 install psycopg2
```

Later it's likely a virtualenv will be setup.
