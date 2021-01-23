# OpenWanderer Server Bot

This 'bot' performs server-side processing of submitted panoramas. It will perform tasks such as:

- give each panorama an elevation, using the Terrarium elevation tiles on AWS;
- perform face and license plate blurring (not yet implemented);
- use Mapillary's Structure from Motion to correct the orientation of adjacent panos (not yet implemented).


## Installing

The 'bot' is being developed using Python 3.6. 

For now, it requires the `python-dotenv`, `pillow`, `psycopg2` and `requests` modules, which can be installed using `pip3` e.g.:

```
pip3 install python-dotenv
pip3 install requests
pip3 install pillow
pip3 install psycopg2
```

Later it's likely a virtualenv will be setup.
