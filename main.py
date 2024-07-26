import TempMailClass 
from Scan import Criminalip
import typer
from Cracker import Crack
from typing_extensions import Annotated
from functions import *
from datetime import datetime
import traceback



def main(query,api_key,path,offset):
        typer.secho("Start Get Data...\n", fg=typer.colors.CYAN)
        query = query.removesuffix("\n")
        return Criminalip().get_ip(api_key, query, path, offset)


typer.clear()
app = typer.Typer(add_completion=False)


try:
    @app.command()
    def get( output: Annotated[str, typer.Option("-o")], query:Annotated[str, typer.Option("-q")],api_key:Annotated[str, typer.Option("--key")]="",metasploit:Annotated[bool, typer.Option("--metasploit/--no-metasploit")] = False, offset:Annotated[int, typer.Option("--offset")] = 1):
        typer.secho("Start Wrok...\n", fg=typer.colors.CYAN)
        # if api_key=="":
        #     typer.secho("Get API KEY...\n", fg=typer.colors.CYAN)
        #     api_key = TempMailClass.main()
            
        result = main(query,api_key,output,offset)
        save_ip(result,output,metasploit)
        
            
#=============================================================================================================================================================

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