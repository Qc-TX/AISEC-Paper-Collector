# -- coding: utf-8 --**
import os
import json
import time
from datetime import datetime
import requests

#自动更新conf文件
SEC_A=["NDSS", "IEEE S&P", "USENIX", "CCS","CRYPTO","EUROCRYPT","TDSC","TIFS"]

SEC_B=["ACSAC", "ASIACRYPT", "CHES", "CSF","DSN","ESORICS","FSE","PKC","RAID","SRDS","TCC"]
'''
CCFB
ACSAC : Annual Computer Security Applications Conference
ASIACRYPT : Annual International Conference on the Theory and Application of Cryptology and Information Security
CHES : Conference on Cryptographic Hardware and Embedded Systems
CSF : IEEE Computer Security Foundations Symposium
DSN : International Conference on Dependable Systems and Networks
ESORICS : European Symposiumon Research in Computer Security
FSE : Fast Software Encryption
PKC : International Workshop on Practice and Theory in Public Key Cryptography
RAID : International Symposium on Research in Attacks, Intrusions, and Defenses
SRDS : IEEE International Symposium on Reliable Distributed Systems
TCC : Theory of Cryptography Conference
'''
SEC_C=["ACISP", "ACNS", "ASIACCS", "CT-RSA", "DFRWS-EU", "DIMVA", "EuroS&P", "FC", "ICDF2C", "ICICS", "IFIP WG 11.9", "IH&MMSec", "ISC", "Inscrypt", "NSPW", "PAM", "PETS", "SAC", "SACMAT", "SEC", "SOUPS", "SecureComm", "TrustCom", "WiSec"]
'''
ACISP : Australasia Conference on Information Security and Privacy
ACNS : International Conference on Applied Cryptography and Network Security
ASIACCS : ACM Asia Conference on Computer and Communications Security
CT-RSA : RSA Conference, Cryptographers' Track
DFRWS-EU : Digital Forensic Research Workshop
# DFRWS-USA : Digital Forensic Research Workshop (未收录)
DIMVA : Detection of Intrusions and Malware & Vulnerability Assessment
EuroS&P : IEEE European Symposium on Security and Privacy
FC : Financial Cryptography and Data Security
HotSec : USENIX Workshop on Hot Topics in Security(未收录)
ICDF2C : International Conference on Digital Forensics & Cyber Crime
ICICS : International Conference on Information and Communications Security
IFIP WG 11.9 : IFIP WG 11.9 International Conference on Digital Forensics
IH&MMSec : ACM Workshop on Information Hiding and Multimedia Security
ISC : Information Security Conference
Inscrypt : International Conference on Information Security and Cryptology
NSPW : New Security Paradigms Workshop
PAM : Passive and Active Measurement Conference
PETS : Privacy Enhancing Technologies Symposium
SAC : Selected Areas in Cryptography
SACMAT : ACM Symposium on Access Control Models and Technologies
SEC : IFIP International Information Security and Privacy Conference
SOUPS : Symposium On Usable Privacy and Security
SecureComm : International Conference on Security and Privacy in Communication Networks
TrustCom : IEEE International Conference on Trust, Security and Privacy in Computing and Communications
WiSec : ACM Conference on Security and Privacy in Wireless and Mobile Networks
'''
NAME_MAP = {
        "NDSS": "ndss",
        "IEEE S&P": "sp",
        "USENIX": "uss",
        "CCS": "ccs",
        "CRYPTO": "crypto",
        "EUROCRYPT": "eurocrypt",
        "TDSC": "tdsc",
        "TIFS": "tifs",
        # CCF-B
        "ACSAC": "acsac",
        "ASIACRYPT": "asiacrypt", #1-4
        "CHES": "tches",#变成期刊 TCHES
        "CSF": "csfw",
        "DSN": "dsn",
        "ESORICS": "esorics",#1-3
        "FSE": "tosc", # 2017年后 本次会议论文集作为IACR对称密码学交易的文章发表。
        "PKC": "pkc", #1-2
        "RAID": "raid",
        "SRDS": "srds",
        "TCC": "tcc",#1-3
        # CCF-c
        "ACISP": "acisp",
        "ACNS": "acns",
        "ASIACCS": "asiaccs",
        "CT-RSA": "ctrsa",
        "DFRWS-EU": "dfrwseu",
        "DIMVA": "dimva",
        "EuroS&P": "eurosp", #w
        "FC": "fc", #1-2/3
        "ICDF2C": "icdf2c", # 2018
        "ICICS": "icics", # 2021 1-2
        "IH&MMSec": "ihmmsec", #ih/ihmmsec2023.html
        "ISC": "isw",
        "Inscrypt": "inscrypt", #cisc/inscrypt2022.html
        "NSPW": "nspw",
        "PAM": "pam",
        "PETS": "popets", #journal
        "SAC": "sacrypt",
        "SACMAT": "sacmat",
        "SEC": "sec",
        "SOUPS": "soups",
        "SecureComm": "securecomm",
        "TrustCom": "trustcom",
        "WiSec": "wisec",
        }

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}


def check_duplicate(confs, item):
    for conf in confs:
        if conf["name"] == item["name"] and conf["url"] == item["url"]:
            return True
    return False


def add_conf(conf,year):
    conf_value = NAME_MAP[conf]    
    try:
        url = f"https://dblp.org/db/conf/{conf_value}/{conf_value}{year}.html"
        print(url)
        r = requests.get(url, timeout=10, headers=HEADERS)
        if r.status_code == 200:
            re_info =[{'url': f'{url}', 'name': f'{conf}{year}'}]
            if conf in SEC_A: 
                path = os.path.join("conf","secA_conf.json")
            elif conf in SEC_B:
                path = os.path.join("conf","secB_conf.json")
            else:
                path = os.path.join("conf","secC_conf.json")
            confs = json.load(open(path, "r"))  # [{'url': '', 'name': ''}]
            if not check_duplicate(confs,re_info[0]):
                re_info[0]["name"] = re_info[0]["name"].upper()
                # confs.append(re_info[0])
                confs += re_info
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(confs, f, indent=4, ensure_ascii=False)
                print(f"[+] {conf}{year}Add list Done!")
            else:
                print(f"[-] {re_info[0]['name']} already exists!")

        else:
            print(f"[-] {conf}{year} 并未更新!")
            return False
        
    except Exception as e:
        print(f"[-] {conf}{year}Wrong!")
        print(e)
        return False
    
def add_journal(conf,year):
    conf_value = NAME_MAP[conf]
    try:
        if conf == "TDSC":
            url = f"https://dblp.org/db/journals/{conf_value}/{conf_value}{year-2003}.html"
        if conf == "TIFS":
            url = f"https://dblp.org/db/journals/{conf_value}/{conf_value}{year-2005}.html"
        else:
            url = f"https://dblp.org/db/journals/{conf_value}/{conf_value}{year}.html"
        print(url)
        r = requests.get(url, timeout=10, headers=HEADERS)
        if r.status_code == 200:
            re_info =[{'url': f'{url}', 'name': f'{conf}{year}'}]
            if conf in SEC_A: 
                path = os.path.join("conf","secA_conf.json")
            elif conf in SEC_B:
                path = os.path.join("conf","secB_conf.json")
            else:
                path = os.path.join("conf","secC_conf.json")
            confs = json.load(open(path, "r"))  # [{'url': '', 'name': ''}]
            if not check_duplicate(confs,re_info[0]):
                re_info[0]["name"] = re_info[0]["name"].upper()
                # confs.append(re_info[0])
                confs += re_info
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(confs, f, indent=4, ensure_ascii=False)
                print(f"[+] {conf}{year}Add list Done!")
            else:
                print(f"[-] {re_info[0]['name']} already exists!")
        else:
            print(f"[-] {conf}{year} 并未更新!")
            return False
    except Exception as e:
        print(f"[-] {conf}{year}Wrong!")
        print(e)
        return False

def add_1234(conf,year):
    conf_value = NAME_MAP[conf]
    try:
        re_info = []
        for i in range(1,5):
            url = f"https://dblp.org/db/conf/{conf_value}/{conf_value}{year}-{i}.html"
            r = requests.get(url, timeout=10, headers=HEADERS)
            if r.status_code == 200:
                #写入name大写
                print(url)
                re_info.append({'url': f'{url}', 'name': f'{conf}{year}'.upper()})
        #如果re_info为空，说明没有找到对应的会议，不再继续执行
        if len(re_info) == 0:
            print(f"[-] {conf}{year} 并未更新!")
            return False
        if conf in SEC_A: 
            path = os.path.join("conf","secA_conf.json")
        elif conf in SEC_B:
            path = os.path.join("conf","secB_conf.json")
        else:
            path = os.path.join("conf","secC_conf.json")
        confs = json.load(open(path, "r"))  # [{'url': '', 'name': ''}]

        if not check_duplicate(confs,re_info[0]):
            # confs.append(re_info[0])
            confs += re_info
            with open(path, "w", encoding="utf-8") as f:
                json.dump(confs, f, indent=4, ensure_ascii=False)
            print(f"[+] {conf}{year}Add list Done!")
        else:
            print(f"[-] {re_info[0]['name']} already exists!")
    except Exception as e:
        print(f"[-] {conf}{year} Wrong!")
        print(e)
        return False

#一些奇奇怪怪的会议
def add_EuroSP(conf,year):
    conf_value = NAME_MAP[conf]    
    try:
        url = f"https://dblp.org/db/conf/{conf_value}/{conf_value}{year}.html"
        print(url)
        r = requests.get(url, timeout=10, headers=HEADERS)
        if r.status_code == 200:
            re_info =[{'url': f'{url}', 'name': f'{conf}{year}'.upper()},
                      {'url': f'https://dblp.org/db/conf/eurosp/eurosp{year}w.html', 'name': f'{conf}{year}'.upper()}]
            path = os.path.join("conf","secC_conf.json")
            confs = json.load(open(path, "r"))  # [{'url': '', 'name': ''}]
            if not check_duplicate(confs,re_info[0]):
                confs += re_info
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(confs, f, indent=4, ensure_ascii=False)
                print(f"[+] {conf}{year}Add list Done!")
            else:
                print(f"[-] {re_info[0]['name']} already exists!")
        else:
            print(f"[-] {conf}{year} 并未更新!")
            return False
        
    except Exception as e:
        print(f"[-] {conf}{year}Wrong!")
        print(e)
        return False
def add_Ihmmsec(conf,year):
    conf_value = NAME_MAP[conf]    
    try:
        url = f"https://dblp.org/db/conf/ih/{conf_value}{year}.html"
        print(url)
        r = requests.get(url, timeout=10, headers=HEADERS)
        if r.status_code == 200:
            re_info =[{'url': f'{url}', 'name': f'{conf}{year}'.upper()},]
            path = os.path.join("conf","secC_conf.json")
            confs = json.load(open(path, "r"))  # [{'url': '', 'name': ''}]
            if not check_duplicate(confs,re_info[0]):
                confs += re_info
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(confs, f, indent=4, ensure_ascii=False)
                print(f"[+] {conf}{year}Add list Done!")
            else:
                print(f"[-] {re_info[0]['name']} already exists!")
        else:
            print(f"[-] {conf}{year} 并未更新!")
            return False
    except Exception as e:
        print(f"[-] {conf}{year}Wrong!")
        print(e)
        return False

def add_Inscrypt(conf,year):
    conf_value = NAME_MAP[conf]    
    try:
        url = f"https://dblp.org/db/conf/cisc/{conf_value}{year}.html"
        print(url)
        r = requests.get(url, timeout=10, headers=HEADERS)
        if r.status_code == 200:
            re_info =[{'url': f'{url}', 'name': f'{conf}{year}'.upper()},]
            path = os.path.join("conf","secC_conf.json")
            confs = json.load(open(path, "r"))  # [{'url': '', 'name': ''}]
            if not check_duplicate(confs,re_info[0]):
                confs += re_info
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(confs, f, indent=4, ensure_ascii=False)
                print(f"[+] {conf}{year}Add list Done!")
            else:
                print(f"[-] {re_info[0]['name']} already exists!")
        else:
            print(f"[-] {conf}{year} 并未更新!")
            return False
    except Exception as e:
        print(f"[-] {conf}{year}Wrong!")
        print(e)
        return False

    
def main():
    # conference = ["NDSS", "IEEE S&P", "USENIX", "CCS","CRYPTO","EUROCRYPT","TDSC","TIFS","ACSAC", "ASIACRYPT", "CHES", "CSF","DSN","ESORICS","FSE","PKC","RAID","SRDS","TCC"]
    conference = ["ACISP", "ACNS", "ASIACCS", "CT-RSA", "DFRWS-EU", "DIMVA", "EuroS&P", "FC", "ICDF2C", "ICICS", "IH&MMSec", "ISC", "Inscrypt", "NSPW", "PAM", "PETS", "SAC", "SACMAT", "SEC", "SOUPS", "SecureComm", "TrustCom", "WiSec"]
    for conf in conference:
        for year in range(2018, datetime.now().year+1):
            if conf == "CRYPTO" or conf == "EUROCRYPT" or conf == "ASIACRYPT" or conf == "PKC" or conf == "TCC" or conf == "FC":
                add_1234(conf,year)
            elif conf == "TDSC" or conf == "TIFS" or conf == "FSE" or conf == "CHES" or conf == "ESORICS" or conf == "PKC" or conf == "TCC" or conf == "PETS" : 
                add_journal(conf,year)
            elif conf == "EuroS&P":
                add_EuroSP(conf,year)
            elif conf == "IH&MMSec":
                add_Ihmmsec(conf,year)
            elif conf == "Inscrypt":
                add_Inscrypt(conf,year)
            else:
                add_conf(conf,year)


if __name__ == "__main__":
    main()

                                    





