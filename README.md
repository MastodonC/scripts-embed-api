###Python scripts as example of using Embed API

* [Embed API doc](https://github.com/MastodonC/kixi.hecuba/blob/552e2fcfcb7aba46376ff743619334b410b26f5a/doc/api.md): useful for basic search, but note the limit of 50 results.


* [Embed functionalities](https://github.com/MastodonC/kixi.hecuba/blob/master/doc/help/embed.md): useful for advanced search


####Content:


**check_upload.py**

    find_entities_by_code(filename, user, pwd)
        Retrieves info for properties given their property codes.
        Writes this info into a csv file.
    
    get_entity_info(entity_id, user, pwd)
        Get devices and sensors for a property given its id.
    
    get_project_info(project_id, entity_code, user, pwd)
        Retrieve property, devices and sensor ids for
        a property code.


**create_devices.py**

    create_device(entity_id, user, pwd)
        Creates a device from an entity id
    
    create_entities_devices(csv_file, project_id, codes, user, pw)
        Create new entities, devices and write a report
    
    existing_devices(entity_id, name, user, pwd)
        Check whether a device already exists
    
    existing_entities(project_id, user, pwd)
        Check whether entities already exists
    
    get_entities_names(csv_file)
        Get the entities names from a csv header
    
    write_report(text_file, project_id, user, pwd)
        Get properties ids, devices ids, sensors ids


**delete_entities.py**

    delete_properties(list_properties, user, pwd)
    
    list_properties(filename)
        List ids of properties to be deleted.


**get_project_profiles_info.py**

    get_profiles(user, pwd, filename)
        Get properties profiles and write into csv file.
    
    list_all_entities(user, pwd)
        Lists all entities in a project
    
    list_all_projects(user, pwd)
        Lists all projects in a programme

**upload_measurements.py**

    check_device(entity_id, device_id, user, pwd)
        Check device exists and device info.
    
    post_measurements(entity_id, device_id, user, pwd)
        Post measurements for a device.
    
    upload_all_measurements(user, pwd)
        Add measurements for multiple devices.


**write_csv_report.py**

    check_device(entity_id, device_id, user, pwd)
        Check device exists and device info.
    
    post_measurements(entity_id, device_id, user, pwd)
        Post measurements for a device.
    
    upload_all_measurements(user, pwd)
        Add measurements for multiple devices.
