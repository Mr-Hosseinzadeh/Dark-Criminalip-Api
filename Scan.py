import requests as req
import json
import typer
from functions import *
import TempMailClass


class Criminalip:
    def get_ip(self, api_key:str, query:str, path: str, offset=1):
        old_save = unduplicate(path)
        create_api_key = True
        parse ={}
        ips = []
        if api_key!="":
            create_api_key = False
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
                    result = [item for item in tmp if item not in old_save]
                    ips.extend(result)
                else:
                    return ips
                offset += 1

            except Exception as e:
                if parse["status"] == 403:
                    if create_api_key:
                        api_key = TempMailClass.main()
                        header.update({"x-api-key": api_key})
                        
                    else:
                        return ips    
                    
                elif offset>1:    
                    typer.secho(f"\nend \n ofsset= {offset}", fg=typer.colors.RED)
                    old_save.extend(ips)
                    ips.clear()
