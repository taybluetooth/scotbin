from colorama import init, Fore

init(autoreset=True)

def pr_error(prt):
    str_to_prnt = f':\t{prt}'.expandtabs(5)
    print(Fore.RED + "ERROR" + Fore.WHITE + str_to_prnt)
    
def pr_info(prt):
    str_to_prnt = f':\t{prt}'.expandtabs(6)
    print(Fore.GREEN + "INFO" + Fore.WHITE + str_to_prnt)