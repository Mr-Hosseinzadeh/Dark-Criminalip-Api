import requests
import requests.adapters
from urllib3.util.retry import Retry
import json
import typer
import os
import logging
import TempMailClass


class Criminalip:
    def __init__(self):
        self.result_path = "result"
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        self.session = requests.Session()
        retries = Retry(total=50, backoff_factor=1)

        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def save_ip(self, ip_list, path: str, metasploit: bool):
        ip_list = list(set(ip_list))
        if metasploit:
            ip_list = [x.replace("\n", " ") for x in ip_list]
        full_path = os.path.join(self.result_path, path)
        with open(full_path, "a", encoding="utf-8") as file:
            file.writelines(ip_list)
            typer.secho("Save Success", fg=typer.colors.YELLOW)

    def unduplicate(self, path: str):
        full_path = os.path.join(self.result_path, path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as file:
                return file.readlines()
        return []

    def get_ip(self, api_key, query, path: str, metasploit, offset=1):
        self.session.headers.update({"x-api-key": api_key})
        old_save = self.unduplicate(path)
        ips = []

        while True:
            try:
                typer.secho(f"\nGet Data From offset= {offset}", fg=typer.colors.GREEN)
                url = f"https://api.criminalip.io/v1/banner/search?query={query}&offset={offset}"
                response = self.session.get(url)
                response.raise_for_status()
                pars = response.json()
                tmp = [
                    f"http://{x['ip_address']}:{x['open_port_no']}\n"
                    for x in pars["data"]["result"]
                ]

                if not tmp:
                    break

                ips.extend([ip for ip in tmp if ip not in old_save])
                offset += 1

            except Exception as e:
                typer.secho(
                    f"\nEnd of data or an error occurred at offset = {offset}",
                    fg=typer.colors.RED,
                )
                typer.secho(f"Error: {e}", fg=typer.colors.RED)
                if pars["status"] == 403:
                    api_key = TempMailClass.main()
                    self.session.headers.update({"x-api-key": api_key})

        if ips:
            self.save_ip(ips, path, metasploit)
