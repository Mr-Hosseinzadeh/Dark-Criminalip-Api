import TempMailClass 
from Scan import Criminalip
import typer
from Cracker import Crack
from typing_extensions import Annotated

# test=""
# with open("output.txt","+r",encoding="utf-8") as file:
#     test = file.read()
#     result = test.replace(","," ")
#     result = result.replace("\n","")


# with open("output2.txt","w+",encoding="utf-8") as file:
#     file.write(result)


typer.clear()
app = typer.Typer(add_completion=False)


@app.command()
def get( path: Annotated[str, typer.Option("--output")], query:Annotated[str, typer.Option("--query")]="", query_file:Annotated[str, typer.Option("--query-file")]="" ,gold_api_key:Annotated[str, typer.Option("--gold-api-key")]="",metasploit:Annotated[bool, typer.Option("-m/-M","--metasploit/--no-metasploit")] = False, offset:Annotated[int, typer.Option("--offset")] = 1):
    typer.secho("Start Wrok...\n", fg=typer.colors.CYAN)
    if gold_api_key!="":
        api_key = gold_api_key
    else:
        api_key = TempMailClass.main()
        
    if  query:
        Criminalip().get_ip(api_key, offset, query, path, metasploit)
    elif query_file:
        with open(query_file,"r+",encoding="utf-8") as file:
            querys = file.readlines()
        if not len(querys)>0:
            typer.secho("Not Found Query",fg=typer.colors.RED)
        else:
            for query in querys:
                Criminalip().get_ip(api_key, offset, query, path, metasploit)

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
