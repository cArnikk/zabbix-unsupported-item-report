# Zabbix Unsupported Items Report

Python script that connects to a Zabbix server, retrieves all **unsupported enabled items**, and exports the results to an Excel report.

## Features

* Connects to Zabbix API using `pyzabbix`
* Retrieves all enabled items with **Unsupported** status
* Collects host information:

  * Hostname
  * IP address
  * Item name
  * Unsupported reason
* Exports results to an Excel file (`.xlsx`)
* Uses environment variables for secure credential management

---

## Requirements

* Python 3.8+
* Zabbix API access

### Python Packages

Install required dependencies:

```bash
pip install pyzabbix pandas openpyxl python-dotenv urllib3
```

---

## Configuration

Create a file named `credentials.env` in the same directory as the script.

Example:

```env
ZABBIX_URL=<zabbix_ip_or_dns>
ZABBIX_USER=<username>
ZABBIX_PASS=<password>
```

---

## Usage

Run the script:

```bash
python3 unsupported_items_report.py
```

After successful execution, an Excel report will be generated:

```text
zabbix-unsupported-item-report.xlsx
```


---

## Output Example

<img width="1158" height="768" alt="obraz" src="https://github.com/user-attachments/assets/d85a82b5-0c7a-4113-8edb-956e6226739b" />

---

## How It Works

1. Loads Zabbix credentials from `credentials.env`
2. Connects to the Zabbix API
3. Retrieves all enabled items where:

   * `state = 1` (unsupported)
   * `status = 0` (enabled)
4. Retrieves host information and IP addresses
5. Combines the data into a Pandas DataFrame
6. Exports the results to an Excel file
7. Logs out from the Zabbix API session

---

## Notes

* SSL certificate verification is disabled (`verify=False`).
* Intended for internal environments where self-signed certificates are commonly used.
* The generated Excel file will overwrite any existing report with the same name.

---

## License

MIT License
