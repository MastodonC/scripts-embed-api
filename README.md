###Collection of (Python) scripts that use Embed API

* [Embed API doc](https://github.com/MastodonC/kixi.hecuba/blob/552e2fcfcb7aba46376ff743619334b410b26f5a/doc/api.md)

**-> Useful for basic search**

**-> Limit of 50 results**


* [Embed functionalities](https://github.com/MastodonC/kixi.hecuba/blob/master/doc/help/embed.md)

**-> Useful for advanced search**




Note: scripts run from the command line or via simple http server (simpleserver.py)



####Info on the scripts

**create_devices.py**

Used to go through a list of codes and create one new property with each code and one device per new property named with this code.

note: I failed to retrieve all existing entities and ended up with duplicates. I didn't know about the advanced search functionalities and must have hit the 50 results limit.

**check_upload.py**

The function named `find_entities_by_code` is where I start implementing the advanced search functionalities to check what I uploaded with the create_devices.py.

**delete_entities.py**

Used to list the properties to delete and delete them one by one using the basic search api.

**sc_final_report.py**

Used to list what properties and devices are currently in a particular project using the advanced search api.
