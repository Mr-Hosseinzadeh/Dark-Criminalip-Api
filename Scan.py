import requests as req
import json
import typer
import os
import TempMailClass
import concurrent.futures
import time


class Criminalip:
    def save_ip(self, ip_list, path: str, metasploit: bool):
        ip_list = list(set(ip_list))
        if metasploit:
            ip_list = list(map(lambda x: x.replace("\n", " "), ip_list))
        if os.path.exists("result"):
            with open("result/" + path, "+a", encoding="utf-8") as file:
                file.writelines(ip_list)  # type: ignore
                typer.secho("Save Success", fg=typer.colors.YELLOW)
        else:
            os.mkdir("result")
            self.save_ip(ip_list, path, metasploit)

    def unduplicate(self, path: str):
        if os.path.exists(path):
            with open(path, "+r", encoding="utf-8") as file:
                ip_list = file.readlines()
            return ip_list
        else:
            return []

    def get_ip(self, api_key, query, path: str, metasploit, offset=1,api_keys=False):
        old_save = self.unduplicate(path)
        parse ={}
        ips = []
        header = {"x-api-key": api_key}
        while True:
            try:
                typer.secho(f"\nGet Data From offset= {offset}", fg=typer.colors.GREEN)
                url = f"https://api.criminalip.io/v1/banner/search?query={query}&offset={offset}"
                response = req.get(url, headers=header)
                parse = json.loads(response.text)
                tmp = list(
                    map(
                        lambda x: "http://"
                        + x["ip_address"]
                        + ":"
                        + str(x["open_port_no"])
                        + "\n",
                        parse["data"]["result"],
                    )
                )
                if len(tmp) > 0:
                    if len(old_save) > 0:
                        for ip in tmp:
                            if not ip in old_save:
                                ips.append(ip)
                    else:
                        ips.extend(tmp)
                else:
                    self.save_ip(ips, path, metasploit)
                    break
                offset += 1

            except Exception as e:
                typer.secho(f"\nend \n ofsset= {offset}", fg=typer.colors.RED)
                self.save_ip(ips, path, metasploit)
                old_save.extend(ips)
                ips.clear()
                if not api_keys:
                    if parse["status"]==403:
                        api_key = TempMailClass.main()
                        header.update({"x-api-key": api_key})
                else:
                    break
                            
