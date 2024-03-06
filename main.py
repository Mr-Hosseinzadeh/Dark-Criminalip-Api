import re
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
def get(
    api_key: Annotated[str, typer.Option("--api-key")],
    path: Annotated[str, typer.Option("--output")],
    query: Annotated[str, typer.Option("--query")],
    metasploit: Annotated[
        bool, typer.Option("-m/-M", "--metasploit/--no-metasploit")
    ] = False,
    offset: Annotated[int, typer.Option("--offset")] = 1,
):
    typer.secho("Start Wrok...\n", fg=typer.colors.CYAN)
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
