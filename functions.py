import os
import typer

def save_ip(ip_list:list, path: str, metasploit: bool):
    ip_list = list(set(ip_list))
    if metasploit:
        ip_list = list(map(lambda x: x.replace("\n", " "), ip_list))
    if os.path.exists("result"):
        with open("result/" + path, "+a", encoding="utf-8") as file:
            file.writelines(ip_list)  
            typer.secho("Save Success", fg=typer.colors.YELLOW)
    else:
        os.mkdir("result")
        save_ip(ip_list, path, metasploit)
           
   
def read_file(path):
    if os.path.exists(path):
        with open(path,"r+",encoding="utf-8") as file:
            lines = file.readlines()
        return lines        
    else:
        raise Exception(f"Not Found {path}")     
    
    
def unduplicate(path: str):
    if os.path.exists(path):
        with open(path, "+r", encoding="utf-8") as file:
            ip_list = file.readlines()
        return ip_list
    else:
        return []    