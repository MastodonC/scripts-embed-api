#!/usr/bin/python
import os, sys, csv
import time, json, requests
from requests.auth import HTTPBasicAuth

CODES = ['SP001', 'SP002', 'SP003', 'SP004', 'SP005', 'SP006', 'SP007', 'SP008', 'SP009', 'SP010', 'SP011', 'SP012', 'SP013', 'SP014', 'SP015', 'SP016', 'SP017', 'SP018', 'SP019', 'SP020', 'SP021', 'SP022', 'SP023', 'SP024', 'SP025', 'SP026', 'SP027', 'SP028', 'SP029', 'SP030', 'SP031', 'SP032', 'SP033', 'SP034', 'SP035', 'SP036', 'SP037', 'SP038', 'SP039', 'SP040', 'SP041', 'SP042', 'SP043', 'SP044', 'SP045', 'SP046', 'SP047', 'SP048', 'SP049', 'SP050', 'SP051', 'SP052', 'SP053', 'SP054', 'SP055', 'SP056', 'SP057', 'SP058', 'SP059', 'SP060', 'SP061', 'SP062', 'SP063', 'SP064', 'SP065', 'SP066', 'SP067', 'SP068', 'SP069', 'SP070', 'SP071', 'SP072', 'SP073', 'SP074', 'SP075', 'SP076', 'SP077', 'SP078', 'SP079', 'SP080', 'SP081', 'SP082', 'SP083', 'SP084', 'SP085', 'SP086', 'SP087', 'SP088', 'SP089', 'SP090', 'SP091', 'SP092', 'SP093', 'SP094', 'SP095', 'SP096', 'SP097', 'SP098', 'SP099', 'SP100', 'SP101', 'SP103', 'SP104', 'SP105', 'SP106', 'SP107', 'SP108', 'SP109', 'SP110', 'SP111', 'SP112', 'SP115', 'SP116', 'SP117', 'SP119', 'SP120', 'SP121', 'SP122', 'SP123', 'SP125', 'SP126', 'SP127', 'SP128', 'SP129', 'SP130', 'SP132', 'SP133', 'SP134', 'SP135', 'SP136', 'SP137', 'SP139', 'SP140', 'SP141', 'SP142', 'SP143', 'SP145', 'SP147', 'SP148', 'SP149', 'SP150', 'SP151', 'SP152', 'SP153', 'SP156', 'SP158', 'SP159', 'SP160', 'SP161', 'SP162', 'SP163', 'SP165', 'SP166', 'SP167', 'SP168', 'SP169', 'SP170', 'SP171', 'SP172', 'SP173', 'SP175', 'SP176', 'SP177', 'SP178', 'SP179', 'SP181', 'SP182', 'SP183', 'SP185', 'SP186', 'SP187', 'SP188', 'SP189', 'SP190', 'SP191', 'SP192', 'SP194', 'SP195', 'SP196', 'SP197', 'SP198', 'SP199', 'SP201', 'SP202', 'SP203', 'SP204', 'SP205', 'SP206', 'SP207', 'SP208', 'SP209', 'SP210', 'SP211', 'SP212', 'SP213', 'SP214', 'SP215', 'SP216', 'SP217', 'SP219', 'SP221', 'SP222', 'SP223', 'SP224', 'SP226', 'SP228', 'SP229', 'SP230', 'SP231', 'SP232', 'SP233', 'SP234', 'SP235', 'SP236', 'SP237', 'SP238', 'SP239', 'SP240', 'SP241', 'SP242', 'SP243', 'SP244', 'SP245', 'SP246', 'SP247', 'SP248', 'SP249', 'SP250', 'SP251', 'SP252', 'SP254', 'SP255', 'SP256', 'SP257', 'SP258', 'SP259', 'SP261', 'SP262', 'SP263', 'SP264', 'SP266', 'SP267', 'SP268', 'SP270', 'SP272', 'SP273', 'SP274', 'SP275', 'SP276', 'SP277', 'SP278', 'SP279', 'SP280', 'SP281', 'SP282', 'SP283', 'SP284', 'SP286', 'SP287', 'SP288', 'SP290', 'SP291', 'SP292', 'SP293', 'SP296', 'SP297', 'SP298', 'SP299', 'SP300', 'SP301', 'SP303', 'SP304', 'SP307', 'SP308', 'SP309', 'SP311', 'SP313', 'SP314', 'SP315', 'SP316', 'SP317', 'SP318', 'SP319', 'SP320', 'SP321', 'SP322', 'SP323', 'SP324', 'SP325', 'SP327', 'SP328', 'SP329', 'SP330', 'SP331', 'SP332', 'SP333', 'SP334', 'SP335', 'SP336', 'SP337', 'SP338', 'SP339', 'SP340', 'SP341', 'SP342', 'SP344', 'SP345', 'SP346', 'SP347', 'SP348', 'SP349', 'SP350', 'SP352', 'SP353', 'SP354', 'SP355', 'SP356', 'SP357', 'SP358', 'SP359', 'SP361', 'SP365', 'SP366', 'SP367', 'SP368', 'SP369', 'SP370', 'SP371', 'SP372', 'SP373', 'SP374', 'SP375', 'SP376', 'SP377', 'SP378', 'SP380', 'SP381', 'SP382', 'SP383', 'SP385', 'SP386', 'SP387', 'SP388', 'SP392']

LIST_CODES = [[i] for i in CODES]

URL = "https://www.getembed.com/4/"
PROJECT_ID = "63e590b0-4747-4e18-929b-8856a5f79a84"

example_url = "http://www.getembed.com/4/entities/?q=project_id%3A63e590b0-4747-4e18-929b-8856a5f79a84%20AND%20property_code%3ASP001&page=0&size=10&sort_key=programme_name.lower_case_sort&sort_order=asc"

def write_report(user, pwd):
    with open('sc_final_report.csv', 'w') as f:
        
        report_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        report_writer.writerow(['property code', 'property ID', 'device ID', 'sensor ID'])
        
        auth = HTTPBasicAuth(user, pwd)
        for i in range(len(CODES[:5])):
            url1 = URL + 'entities/?q=project_id3A' + PROJECT_ID + '%20AND%20property_code%3A' + CODES[i] + '&page=0'
            r1 = requests.get(url=url1, auth=auth)
            time.sleep(2)
            if r1.status_code == 200:
                results1 = r1.json()['entities'][0]
                LIST_CODES[i].append(results1['entity_id'] or '')
                devices = results1['devices']
                for device in devices:
                    for sensor in device['description']:
                        desc = sensor['sensor_id'] or ''
                        sen_id = sensor['sensor_id'] or ''
                        dev_id = sensor['device_id'] or ''
                        LIST_CODES[i].append(dev_id)
                        LIST_CODES[i].append(sen_id)
            report_writer.writerow(LIST_CODES[i])



if __name__ == '__main__':
    ##print LIST_CODES[:10]
    write_report(sys.argv[1], sys.argv[2])
