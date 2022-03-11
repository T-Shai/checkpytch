#!/bin/python3

# INCLUDES
import subprocess
from enum import Enum, auto

# CONSTANTS
PARSER_STR_ERROR    = "ERROR"
PARSER_STR_WARNING  = "WARNING"
PARSER_STR_TOTAL    = "total"

# ERRORS 
class ERROR(Enum):
    TRAILING_WHITESPACE = auto()
    PTR_ASTERISK_SIDE   = auto()
    C99_COMMENTS        = auto()

# WARNINGS
class WARNING(Enum):
    START_SPACE = auto()

def run_cmd(vargs : list) :
    result = subprocess.Popen(vargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.communicate()[0].decode()

# get checkpatch output
to_fix = run_cmd(["./checkpatch.pl", "-f", "--no-tree", "test/lab1-fixed.c"])

# parse output
has_error = False
n_error   = 0
errors_list = list()

has_warning = False
n_warning   = 0
warnings_list = list()

curr_error = []
in_error = False

curr_warning = []
in_warning = False

for line in to_fix.split('\n'):

        if line.replace(" ","") != "":
            if in_error:
                if line.startswith("#"):
                    curr_error.append(line)

                if line.startswith("+"):
                    curr_error.append(line)
                    errors_list.append(curr_error)
                    in_error = False
                    curr_error = []

            if in_warning:
                if line.startswith("#"):
                    curr_warning.append(line)

                if line.startswith("+"):
                    curr_warning.append(line)
                    warnings_list.append(curr_warning)
                    in_warning = False
                    curr_warning = []
        
        if line.startswith(PARSER_STR_TOTAL):
            n_error = int(line.split()[1])
            has_error = (n_error != 0)

            n_warning = int(line.split()[3])
            has_warning = (n_warning != 0)
        
        if line.startswith(PARSER_STR_ERROR):
            in_error = True
            curr_error.append(line)
        
        if line.startswith(PARSER_STR_WARNING):
            in_warning = True
            curr_warning.append(line)


print(f"{has_error  =  }")
print(f"{n_error    =  }")
print(f"{errors_list    =  }")
print()
print(f"{has_warning  =  }")
print(f"{n_warning    =  }")
print(f"{warnings_list    =  }")

def parse_message(msg):
    # ERROR
    if msg.startswith(PARSER_STR_ERROR):
        msg = msg[7:]
        
        if msg == "trailing whitespace":
            return ERROR.TRAILING_WHITESPACE
        
        elif msg == "\"foo* bar\" should be \"foo *bar\"":
            return ERROR.PTR_ASTERISK_SIDE
        
        elif msg == "do not use C99 // comments":
            return ERROR.C99_COMMENTS

        else :
            raise NotImplementedError("Error type not implemented :" + msg)

    # WARNING 
    elif msg.startswith(PARSER_STR_WARNING):
        msg = msg[9:]

        if msg == "please, no spaces at the start of a line":
            return WARNING.START_SPACE
    else :
        raise NotImplementedError("neither an error nor a warning :"+ msg)

files_cache = dict()

def get_file(file_name):
    if file_name not in files_cache:
        with open(file_name) as f:
            files_cache[file_name] = f.readlines()

    return files_cache[file_name]


def fix_warning(warn_l):
    for warng in warn_l:
        if len(err) == 3:
            war_msg, line_msg, code_msg = warng
            error_type = parse_message(war_msg)
            index_f_col = line_msg.find(':')
            error_line = int(line_msg[1:index_f_col])-1
            line_msg = line_msg[index_f_col+1:]
            index_s_col = line_msg.find(':')
            line_msg = line_msg[index_s_col+2:]
            index_t_col = line_msg.find(':')
            error_file = line_msg[:index_t_col]

            err_file_line = get_file(error_file)[error_line]

            if error_type == WARNING.START_SPACE:
                n_spaces = len(err_file_line) - len(err_file_line.lstrip())

def fix_error(err_l) :
    for err in err_l:
        if len(err) == 3:
            err_msg, line_msg, code_msg = err
            error_type = parse_message(err_msg)
            index_f_col = line_msg.find(':')
            error_line = int(line_msg[1:index_f_col])-1
            line_msg = line_msg[index_f_col+1:]
            index_s_col = line_msg.find(':')
            line_msg = line_msg[index_s_col+2:]
            index_t_col = line_msg.find(':')
            error_file = line_msg[:index_t_col]

            err_file_line = get_file(error_file)[error_line]
            if error_type == ERROR.TRAILING_WHITESPACE:
                fixed_err_file_line = err_file_line.rstrip()
                
            elif error_type == ERROR.PTR_ASTERISK_SIDE:
                i_asterisk = err_file_line.find('*')
                fixed_err_file_line = list(err_file_line)
                fixed_err_file_line[i_asterisk] = ' '
                fixed_err_file_line[i_asterisk+1] = '*'
                fixed_err_file_line = "".join(fixed_err_file_line)

            elif error_type == ERROR.C99_COMMENTS:
                fixed_err_file_line = err_file_line.replace("//", "/*").replace('\n', " */\n")

            else :
                raise NotImplementedError("Error type unknown, None or not implemented :" + str(error_type))

            get_file(error_file)[error_line] = fixed_err_file_line

        else :
            raise NotImplementedError("Error not implemented :" + err)

if has_warning:
    fix_warning(warnings_list)
# if has_error :
#     fix_error(errors_list)

# for fixed_files in files_cache:
#     with open(fixed_files.replace(".c", "-fixed.c"), 'w') as f:
#         f.writelines(files_cache[fixed_files])
