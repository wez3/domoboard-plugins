@author=Squandor
@title=Afvalwijzer
@version=0.0.2
@description=Small plugin which uses the site mijnafvalwijzer.nl to show which garbage will be picked up on which date, you configure this plugin by adding the following to an configuration:   [[afvalwijzer]] postcode = zipcode, housenr

@summary=To use this plugin on you're dashboard you first need to check if you zipcode is in the mijnafvalwijzer.nl site. so check this first before you configure you're .conf file.
[afvalwijzer]
[[display_components]]
components = afvalwijzer
[[afvalwijzer]]
zipcode = xxxxXX, 11

