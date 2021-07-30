__HEADER = '\033[95m'
__OKBLUE = '\033[94m'
__OKCYAN = '\033[96m'
__OKGREEN = '\033[92m'
__WARNING = '\033[93m'
__FAIL = '\033[91m'
__ENDC = '\033[0m'
__BOLD = '\033[1m'
__UNDERLINE = '\033[4m'

def __print(level : str, severity : str, msg : str):
    print("{}[ {} ]{} {}".format(level, severity, __ENDC, msg), flush=True)

def warn(msg : str):
    __print(__WARNING, "WARNING", msg)

def info(msg : str):
    __print(__OKGREEN, "INFO", msg)

def error(msg : str):
    __print(__FAIL, "ERROR", msg)
