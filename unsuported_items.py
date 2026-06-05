#!/usr/bin/env python3

from pyzabbix import ZabbixAPI
import urllib3
import os
import pandas as pd
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.env")
load_dotenv(dotenv_path)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
EXCEL_OUTPUT = os.path.join(SCRIPT_PATH, f"zabbix-unsupported-item-report.xlsx")

credentials = {
    "username": os.getenv("ZABBIX_USER"),
    "password": os.getenv("ZABBIX_PASS"),
    "url": os.getenv("ZABBIX_URL")
}

def getUnsupportedItems(zapi):
        unsupported = []

        try:
            getItem = zapi.item.get(
                output=["itemid","name", "state", "hostid", "error"],
                filter={
                    "state": 1, # 0 - supported / 1 - unsupported
                    "status": 0 # 0 - item enabled
                    } 
            )

            getHost = zapi.host.get(
                 output=["host", "name"],
                 selectInterfaces=["ip"]
            )

            hosts = {
                 h["hostid"]: {
                        "hostname": h["name"],
                        "ip": h["interfaces"][0]["ip"]}
                 for h in getHost}

            for i in getItem:
                hostInfo = hosts.get(i["hostid"], {"hostname": "Unknown", "ip": "Unknown"})
                unsupported.append({
                    "Hostname": hostInfo["hostname"],
                    "IP": hostInfo["ip"],
                    "Item ID": int(i["itemid"]),
                    "Item name": i["name"],
                    "Unsupported reason": i.get("error", "")
                })

            if unsupported:
                df = pd.DataFrame(unsupported)
                df.to_excel(EXCEL_OUTPUT, index=False)
                print(f"\nData exported successfully to '{EXCEL_OUTPUT}'.")
            else:
                print(f"\nNo data to export.")

            return unsupported

        except Exception as e:
            print(f"Error retrieving item or trigger details: {e}")
            return  None

def main():
    zapi = None
    try:
        zapi = ZabbixAPI(credentials["url"])
        zapi.timeout = 10
        zapi.session.verify=False
        zapi.login(credentials["username"], credentials["password"])

        getUnsupportedItems(zapi)

    except Exception as e:
        print(f"\n Connection Error: {e}")
        
    finally:
        if zapi and zapi.user:
            zapi.user.logout()

if __name__ == "__main__":
    main()