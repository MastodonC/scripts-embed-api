#!/usr/bin/python
import os, sys, csv
import time, json, requests
from requests.auth import HTTPBasicAuth

PROJECTS = [u'003f8085a4464cf3feb43ec0ae9d8ce155399053', u'bc879a61765cabdf4c5a588ca074b65abb00d785', u'f5c91762990610a30de61e93b6b5b9f378aa1ef1', u'b0b545c9a6c7b7cab1dfeafa5d8768f33516e980', u'a5d46fd91971308faef99e92f2c80da79f4508dd', u'8be8eb6cb307d8048a3ec67c551d1cb3f4b0fe35', u'0e96af3e9e36e21e062db61fba899e64489efe14', u'd1aa67e09481edcbe97168898e0f35ab0a1bed6d', u'99ec20944c13709a9b7faebbba87fdcfa3f30e55', u'f1fe27d77b272a9ef968157c877271a271f1fc56', u'502c0ec2601982bbc7919c2a849d836531c7e31d', u'9844e4e624a02157aabbb4b1525bcf615c1d7854', u'ab55b07de10b3541a11070ba36c2a3343d649e22', u'7733438f9fc3460141927b99d071b98eaa181fc8', u'10ee6a401f9a85dd48919ae80ced891c4df21d4a', u'd6f0a57408b0f644a9a3e0b20c62d24108e25f5b', u'39ed9e694786add5251d99eff3115c2d55c28209', u'afa297d409fa7e7c0d902b4ea11a970c25a9e29c', u'5c01b1a46cee8c5295436fe6ee396e9905e05c7d', u'35ded735e631e9332ada322369d8c98abb111fed', u'ce759804b93f716af28f4ca97bcc083d1da6d255', u'66a1ade5a7fecd82507b5eeaf83e16c5a1cf02fd', u'22ee8f230e2e33e6aec3a9d70d013b74420e1fe6', u'74f029b14feeb835c80d84a5450ab6edc1657e86', u'2bca6a06a7b1b6a03ed3791140e7a83a25acfbe5', u'abd2ca103c648becf14f655e462d8afa292a7375', u'12ce7bbb5cceea4736e501bd0c0f27e190ffd754', u'32f344d2e8a4c8d567c9174996d6d9648f9b76f2', u'b88bfb461b3fa5e5897015c412f2454a2514a123', u'194f146edbb95f2cf7907d0ca4fc1e9474903c99', u'350865b5f8df914bba0cb754f28bec08d9150818', u'5f13ab15582b4e9161997831404ccf9756748dab', u'843b0e1e5b1844fb2583c6de111dd3d4cefbc5c1', u'60fef0470cfd990f1280dc48a3409342872e82b2', u'7ea88d642553512c5352a2f31b438ccf70727af2', u'27018d4de4823554509c0006a9e632dbc41b295a', u'db8f66d754a43f20f1d1c48c457c13dea88c1f64', u'408e05fc610af605977e207ce6bb1c166bc9f241', u'c5eb27e941b257b8a82834ed0db84657d6a73a42', u'5d3b5079fad5e96879da7ef841c624002eae999e', u'4af13de337d5bf7dbbfa010ef44c0e98d89c29ba', u'7c0ac21389c6922d4ea8e705391c1d9c7a0b130b', u'9c1b0e4813b841e20ff936dd40d3f3d53843d193', u'b109d00145de43f62e41cbbf666dcc0069b3b717', u'095c7b21786c8040722c786f6f22dbb6eb72b584', u'439b3f618024dd969467d0ed51816aef216112fe', u'701bf003d85a59a9fd9f2fa36b4de26cf3853eb7']

ENTITIES = [u'd52942fd-bda2-4ecc-98b6-5b6a948f907a', u'28e0563d-5515-4534-a5cc-db973ea66179', u'43574507-fea9-468b-8f05-9347c443526d', u'78742532-631d-4aab-8727-df04a549b889', u'b9b19789-e0fe-48e8-8db8-27d281714769', u'7f0527e9-16c7-48fd-90c1-3310afcb42e5', u'5c230d38-7713-4a0b-abcc-db77661396c1', u'9c6ec875-448d-4a9e-86ba-0638f26fc596', u'f726b558-68b6-480e-909a-499ff39f0598', u'65a0171b-9a9b-4037-837a-9badac1ea59e', u'a42eb6e3-6d9f-4f5d-aa36-ddb76b4095c0', u'6fc87d88-95b5-44bc-892f-b4de9bc1885d', u'c1ab3c7f-8d47-4089-bd2a-b45646f12c9b', u'20097a04-84eb-439b-89c2-fd2a2e2b7632', u'282b9497-d8fb-49af-982a-b444d4097d78', u'1d3f8fbcd69bdc40aa6f8b0df1323b44100d99c3', u'3db570e2bc30b07c1e11247c1d6deaf52151fdc6', u'ac72c1391a5da81b6ae29c2f6eea572685151088', u'd6bc74c6c7d40fbcb3bf729de2ab41bd834a1c94', u'2fda5e554c56225bdb16882b234ae786c2bf83e1', u'1df709a562f6ae894f54d552eda6f822bbf1b92b', u'2d7947615bde4fda1d70d77dd45f1d5d4463bef9', u'4601b60f79a41b3b0faf1cbdb30f94102ee3db7b', u'6001b5989d5e865b2222e85d505d134e21360347', u'3fafaf098435b4b21d8a6eb868b9121a695bb9db', u'1bfde63b6d538fd4383a47c83fad56272338364a', u'3025076f3e268ac7c1bf5744c435e87d3bc7d36f', u'4b37b032-a8dc-4e98-b31f-6f8429b276c3', u'0aeaae34-475e-4ee4-95d5-fae05169ea93', u'62fceb58-5292-43c9-a925-64bae550898f', u'cb6ff169ca7f455f59594b923584dc2c54095f69', u'd0e777ad-ff33-4912-a82d-e1986aa48cdb', u'd9bea476-b8c4-4cea-8717-aea84670242d', u'f1a66f6adb6b788b35183c67e326d5637364059c', u'58d86b88239b09faa48c26e9caf269e4f5199561', u'4ddb244e4e82305fd2e75cb73f588c509c1dea8b', u'da0158b39a68c545da7a18da5c2628001a504544', u'9084d574c02743d4473259340db8cfa01301cef5', u'9ff08736-70ef-4bda-adc4-d82b4f4f1d18', u'62c1894c-3a18-4557-9882-b197714881a8', u'eba10227-17f8-41ef-b851-ff6ad9130ad6', u'9af0a801-2ab1-484c-8cf1-511dbac33a10', u'81c13370-4e17-4e32-bf03-60f140ec4bb3', u'2d78bdec-5d35-483e-b578-0e856d67dc39', u'5cb35364b2f212ffdd5d0384a551cbb489f16531', u'c419cdaa4551c738d73217ed3d25b40f66938793', u'de69e5988d9159227ba3b90bab52492cf4fd3ada', u'e7cf18577c4eb7a72cb0e80f2aaec97d91cccc4a', u'9f47852fa4b9adb41f97310a2238e9c4621f67b6', u'1f33e67d-4c15-402a-bb0e-40f05a3ace07', u'773d914e-cf75-415a-a3f3-ec745debc716', u'caa32bb7-cef4-46a9-8a55-fecbde6956f9', u'd420dcc0-1cce-4b18-8561-e1a151b2f221', u'e6da4c3f-b370-4a7a-b915-f5b5e6a91a3c', u'57d5b6de-2045-4193-b1fe-924c064bbdca', u'b43155a6-1b93-40eb-bc8f-f98b9592cc35', u'3454dc98-f4a1-4d18-9198-422d0da23355', u'c8356eac-f82e-4841-8110-eb8918840e16', u'396db5da-5442-4fd4-8a7e-130e70555d3b', u'477d7828-d41e-42a7-9635-e4224489581d', u'45857c35-b35f-49b3-a80e-7f48a15ac3af', u'4eb4cc58-f4ef-4f48-a39a-7ddcecb9ebc0', u'513eb019-276c-4ad3-b3c9-62aaef8902f2', u'6d9e30d8-ed74-49b7-bdf7-b5cdf145f5ea', u'f26c6b50-e581-4f02-8ac8-9b22b4c6e74f', u'83a54d9e-7e35-49c3-a349-44845cc6a881', u'5c43d4b0-1d2a-456d-818f-0f48717274c9', u'f793e56b-16e5-4d96-b455-527fdf600842', u'a9b617a4-1880-41c2-b5ad-f809b993f0fc', u'0392a02e-231f-40d6-9340-59b140b6ae89', u'8beb099380e765a6b77029a038dc72992c2547e1', u'b8eb3119ad740446c04b261093aed8719e82e7f7', u'e3ee2d7c10e78e21d792896d085c4f63892d376c', u'0f6c6781d360c898f1e16967ea7158cdec1ab863', u'df8d259dce700d4ca07e854a86d45b4c00250b90', u'0431f5c8f2b6f887a9a45105a3f27d154980262a', u'8f7e789d3725e0425bd40107c77fdd86c03b678f', u'2cd308755ae52fd27adacd75c4eb7b71de2e0a7d', u'0de39cd6-ad46-4068-a3fb-db96f03ef3ed', u'ed68e49b-3005-4bdf-b025-cd8760abdca9', u'fce457d8-f397-4d66-b929-139032fbb1fd', u'c19dd4acb0b76e5ff15fe98ee88a4d713681d9f9', u'f3d4269f866e6e09877e36b17a169d4802d60f59', u'56aa6e522add65b4f28835058ef585435f94ff17', u'f952fdae7bd30d4bbc51f5cc4c7b8d0088422ae5', u'84665562189c79aa354aa857249c152022949074', u'33c63542befa2be37df3f6836e2360defe00ca71', u'b870ce331498dfa8315131c200a8a689bdc63874', u'da719147229258435d52d4ef3b54a356985d8924', u'29e36c3ba5acaa799fda884896d9166764fffaf4', u'7b4b923d2cad30c09c206694fa13ede1cc228c55', u'bc587a10f6a4e204255c56e97fb52f68e05b2b52', u'19a3b7c508e5f074625e0757c5fd021ba1e6dfa3', u'8a95fe1f891a61ec4d55135bb689b48f554dd405', u'723ba6e766a717d23d15adcfcd11da6329d79bf0', u'0db15267df1355fe438ce463414edc08be0c1e99', u'727dd74cb712cd5ba1cad9a3a1b2c6c4fa32d166', u'24fbd8b97a21d88d62e235d1f69e21d1ed233a59', u'048b7eb20d3d0f83a91caac445c01f584b3ddcd0', u'ae2a60373a5592b2012118e388f986fede05df07', u'c3014110e7423d01beea130e221a560c9cfc7c8e', u'0f453bc3aff39570385afc7fd95050b0dbff6bb9', u'99b0613a078c01ca27d0e10083e1ad315bcb3fc5', u'396e5649a1e553ee3922669b762c98eafeea5e43', u'0e9e4cde284484f6016a4fa71463155c8ca82050', u'0d9726ba6c83c0fb07d945abd33bca2940734b27', u'98a20f9a-0260-4fe1-9dc3-53a874787060', u'c2072adcfe779f83bc36902816c9a6ffb1808dee', u'a47be04f3e23c8cacce174fa581aa67a773dc982', u'20523816-6f7c-45f8-bf25-bfe3d87a7b4f', u'1f4c7a21-4f03-4eba-bc80-19bfc36f3eea', u'0fe824d4-17ad-413f-9152-715c830fdb0c', u'a3a41d05d5954cdfe392b8f5ae0a79d77e213d3a', u'ed19430570053800610bc0f43ba4bd0583d4bef2', u'ebeb945fe04944933fc72eeb0e28342ea7064bd2', u'0b93fedc4c89d721e4eda337012924eaa8db2eaa', u'1e5e215292de0cd67fa661232a18e99702e58137', u'218f810fa847fe0f9ba2f18d358530c22f26c8bf', u'9d99683b5c6fde22bd31fcd20fa4c62015224dc6', u'63cb28a42d18ddbae5c1062d794df4206fe94dd6', u'd13147127a993bdf89fff6cff49420e2ac19c7d8', u'ab9f95b8e8b063bc0eb5bb34ecaa2e626bda3379', u'2a2e89ef1a7e4ce047529da5c9cab55877611058', u'91130ac89d1c1ed6d6b8301a2015f184c7518c51', u'cf900b11838d1c4625477a6a3475dbe2986af1bb', u'cc221149-2d5d-4ecc-a034-010bc4575210', u'3e8d1b18-a04b-47b3-83e4-5615bb5ab876', u'017b9c0e37bcad5b937d6a4b93b31042b17a732e', u'87eca0c5148f0bd8e98844595076314c2393ec2a']


URL = "https://www.getembed.com/4/"

PROG_ID = "bfb6e716f87d4f1a333fd37d5c3679b2b4b6d87f"


def list_all_projects(user, pwd):
    project_ids = []
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "programmes/" + PROG_ID + "/projects"
    r = requests.get(url=url, auth=auth)
    time.sleep(2)
    if r.status_code == 200:
        list_projects = r.json()
        print "There are %d projects." % len(list_projects)
        for project in list_projects:
            print project['project_id']
            project_ids.append(project['project_id'])
    return project_ids

def list_all_entities(user, pwd):
    entity_ids = []
    auth = HTTPBasicAuth(user, pwd)
    for proj_id in PROJECTS:
        url = URL + "projects/" + proj_id + "/entities"
        r = requests.get(url=url, auth=auth)
        time.sleep(2)
        if r.status_code == 200:
            list_entities = r.json()['entities']
            for entity in list_entities:
                entity_ids.append(entity['entity_id'])
    return entity_ids

def get_profiles(user, pwd, filename):
    auth1 = HTTPBasicAuth(user, pwd)
    
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Property ID', 'Profile ID', 'Event type', 'Timestamp'])
        
        for entity in ENTITIES:
            print "ENTITY: ", entity
            url1 = URL + "entities/" + entity + "/profiles"
            r = requests.get(url=url1, auth=auth1)
            time.sleep(2)
            print r.status_code
            if r.status_code == 200:
                list_profiles = r.json()
                print "There are %d profiles." % len(list_profiles)
                if len(list_profiles) > 2:
                    for profile in list_profiles:
                        profile_id = profile['profile_id']
                        profile_name = profile['profile_data'].get('event_type', '')
                        profile_date = profile['timestamp']
                        csv_writer.writerow([entity, profile_id, profile_name, profile_date])
                

if __name__ == "__main__":
    ##get_profiles(sys.argv[1], sys.argv[2])

    ##print list_all_projects(sys.argv[1], sys.argv[2])

    ##print list_all_entities(sys.argv[1], sys.argv[2])

    get_profiles(sys.argv[1], sys.argv[2], "duplicate_profiles.csv")
    print "CSV written!"

    #print ENTITIES.index('2cd308755ae52fd27adacd75c4eb7b71de2e0a7d')

    

