@author=Squandor
@title=Verkeer
@version=0.9.8
@description=This plugin calculates the driving time from one point to another (ANWB is used). Next to this speedlights are tracked. It also support a Google map with traffic jams.
@summary=It is possible to have multiple anwb traffics added to one page.
use the following possible configurations
[anwb]
  [[display_components]]
    components = top_tiles, anwb[work], anwb[prive]
  [[top_tiles]]
    Town = 162
    Road = 161
  [[anwb]]
  [[[work]]]
  adres = "Hoofdstraat 64, Nijmegen", "Korte minrebroederstraat 1, Utrecht"
  [[[prive]]]
  adres = "Meerhoek 209, Uden",  "Korte minrebroederstraat 1, Utrecht"

Just make sure to use the "","" format else the plugin won't now which address is the start or the end.
