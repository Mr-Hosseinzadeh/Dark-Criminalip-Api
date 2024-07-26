import TempMailClass 
from Scan import Criminalip
import typer
from Cracker import Crack
from typing_extensions import Annotated
import os
from datetime import datetime
import traceback

def main(query,api_key,path,metasploit,offset,query_file):
    if query!="":
        typer.secho("Start Get Data...\n", fg=typer.colors.CYAN)
        Criminalip().get_ip(api_key, query, path, metasploit,offset)
    elif query_file!="":
        if not os.path.exists(query_file):
            typer.secho("Not Found File",fg=typer.colors.RED)
            exit()
        with open(query_file,"r+",encoding="utf-8") as file:
            querys = file.readlines()   
        if not len(querys)>0:
            typer.secho("Not Found Query",fg=typer.colors.RED)
        else:
            for query in querys:
                query = query.removesuffix("\n")
                Criminalip().get_ip(api_key, query, path, metasploit,offset,)
    else:
        typer.secho("query required",fg=typer.colors.RED)
        input("\npress enter...")
        exit()



try:
    typer.clear()
    app = typer.Typer(add_completion=False)


    @app.command()
    def get( path: Annotated[str, typer.Option("--output")], query:Annotated[str, typer.Option("--query")]="", query_file:Annotated[str, typer.Option("--query-file")]="" ,gold_api_key:Annotated[str, typer.Option("--gold-api-key")]="",api_key_list:Annotated[str, typer.Option("--api-key-list")]="",metasploit:Annotated[bool, typer.Option("-m/-M","--metasploit/--no-metasploit")] = False, offset:Annotated[int, typer.Option("--offset")] = 1):
        typer.secho("Start Wrok...\n", fg=typer.colors.CYAN)
        if gold_api_key!="":
            api_key = gold_api_key
            main(query,api_key,path,metasploit,offset,query_file)
        elif api_key_list !="":
            with open(api_key_list,"r+",encoding="utf-8") as file:
                api_keys = file.readlines()
            for api_key in api_keys:
                api_key = api_key.removesuffix("\n")
                main(query,api_key,path,metasploit,offset,query_file)
                    
        else:                
            typer.secho("Get API KEY...\n", fg=typer.colors.CYAN)
            api_key = TempMailClass.main()
            main(query,api_key,path,metasploit,offset,query_file)
            
        
            
            

    @app.command()
    def crack(
        targets: Annotated[str, typer.Option("--targets")] = "targets.txt",
        usernames: Annotated[str, typer.Option("--usernames")] = "usernames.txt",
        passwords: Annotated[str, typer.Option("--passwords")] = "passwords.txt",
        output: Annotated[str, typer.Option("--output")] = "Cracked.txt",
    ):
        crack = Crack()
        crack.crack(targets, usernames, passwords, output)


    app()
except Exception as e:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error_message = str(e)
    detailed_error_message = traceback.format_exc()

    log_message = f"Time: {current_time}\nError Message: {error_message}\nDetailed Error:\n{detailed_error_message}\n---\n"

    log_file_name = 'error_log.txt'
    with open(log_file_name, 'a+') as log_file:
        log_file.write(log_message)



#