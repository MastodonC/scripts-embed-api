##Python scripts as example of using Embed API


###API Docs


* [Embed API doc](https://github.com/MastodonC/kixi.hecuba/blob/552e2fcfcb7aba46376ff743619334b410b26f5a/doc/api.md): useful for basic search, but note the limit of 50 results.


* [Embed functionalities](https://github.com/MastodonC/kixi.hecuba/blob/master/doc/help/embed.md): useful for advanced search


###Content

* [check_profiles.py](#check_profilespy)
* [check_upload.py](#check_uploadpy)
* [create_devices.py](#create_devicespy)
* [delete_entities.py](#delete_entitiespy)
* [embed_programmes.py](#embed_programmespy)
* [get_project_profiles_info.py](#get_project_profiles_infopy)
* [send_requests.py](#send_requestspy)
* [upload_measurements.py](#upload_measurementspy)
* [write_csv_report.py](#write_csv_reportpy)


####check_profiles.py

	get_profiles(user, pwd, entities, filename)
        Returns a csv file containing profile info
        for a list of entity ids provided.
    
    list_all_entities(user, pwd, projects)
        Returns a list of all the entity ids
        for a list of project ids.
    
    list_all_projects(user, pwd, programme_id)
        Return a list of all project ids in a
        programme.
    
    read_json_data(filename)
        Get duplicate profiles projects and
        properties ids stored in a json file.


####check_upload.py

    find_entities_by_code(project_id, property_codes, outfile, user, pwd)
        Retrieves info for properties given their property codes.
        Writes this info into a csv file.
    
    get_entity_info(entity_id, user, pwd)
        Get devices and sensors for a property given its id.
    
    get_project_info(project_id, entity_code, user, pwd)
        Retrieve property, devices and sensor ids for
        a property code.


####create_devices.py

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


####delete_entities.py

    delete_properties(list_properties, user, pwd)
    
    list_properties(filename)
        List ids of properties to be deleted.


####embed_programmes.py

    get_all_programmes(user, password, action, *args)
        Return info on all your programmes:
        [action]: Results can be printed and/or written to 
        a csv file. Value should be 'stdout', 'csv' or 'both'.
        [*args]: (see PROGRAMME_INFO for the full list)
        - If *args is left blank the info returned is 
        set in DEFAULT_INFO.
        - Otherwise it returns DEFAULT_INFO and the other 
        parameters specified.
    
    get_programme_by_id(user, password, programme_id, action, *args)
    
    results_to_csv(data, *args)
        Write the results to a csv file
    
    results_to_stdout(data, *args)
        Print the results to your terminal


####get_project_profiles_info.py

    get_profiles(user, pwd, filename)
        Get properties profiles and write into csv file.
    
    list_all_entities(user, pwd)
        Lists all entities in a project
    
    list_all_projects(user, pwd)
		Lists all projects in a programme


####send_requests.py

    get_request(user, password, url)
        Generate a generic http get request,
        handle errors and return the json data.
    
    validate_hostname(url)
        Check the hostname is part of authorised 
        hostnames defined in HOSTNAMES
    
    work_locally(url)
        Print a warning message to tell you whether
        you're working on a local Embed instance or
        on the production server.


####upload_measurements.py

    check_device_info(entity_id, device_id, user, pwd)
        Check device exists and device info.
    
    check_measurements_upload(entity_id, device_id, sensor_type, start_date, end_date, user, pwd)
        Check measurements were uploaded to a specific device.
        Expect the sensor type and start/end dates as strings like '2015-09-09'.
    
    get_json_data(filename)
        Retrieve measurements from a json file.
    
    post_measurements(entity_id, device_id, measurements, user, pwd)
        Post measurements for a device.
    
    upload_all_measurements(user, pwd)
        Add measurements for multiple devices.


####write_csv_report.py

    write_report(filename, user, pwd)
        Retrieve info about properties in a project
        and with specific property codes.
        Write the results to a csv file.
