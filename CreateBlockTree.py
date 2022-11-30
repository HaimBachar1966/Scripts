#!/usr/bin/env python3
'''
-------------------------------------------------------------------------
File name    : CreateBlockTree.py
Title        :
Project      : 
Developers   : Haimb
Created      : 11/10/2022 
Description  :
Notes        :
---------------------------------------------------------------------------
Copyright 2015 (c) Satixfy Ltd
---------------------------------------------------------------------------*/
'''
import getpass

from datetime import datetime
import os,sys,argparse
from sys import argv
# from label_utils import check_label_path
# import utils
import logging
global_verbosity = int(os.getenv("SCRIPT_VERBOSITY",logging.INFO))
formatter = logging.Formatter('%(name)s (%(levelname)s) %(message)s')

def start_log(logging_unit_param="Default", logging_path_param=".", add_log_file=False, override_formatter=None):
    global formatter
    logger = logging.getLogger(logging_unit_param+'_logger')
    logger.setLevel(global_verbosity)
    logger.debug("started logger %s %s",logger,logger.name)
    if logger.handlers:
        logger.debug(("Logger for "+logging_unit_param+" already exists!"))
        return logger

    if override_formatter:
        my_formatter = override_formatter
    else:
        my_formatter = formatter

    if add_log_file:
        logger_file_hdlr = logging.FileHandler(logging_path_param+'/'+logging_unit_param+'.log')
        logger_file_hdlr.setFormatter(my_formatter)
        logger_file_hdlr.setLevel(logging.DEBUG)
        logger.addHandler(logger_file_hdlr)

    logger_console_hdlr = logging.StreamHandler()
    logger_console_hdlr.setFormatter(my_formatter)
    logger_console_hdlr.setLevel(global_verbosity)
    logger.addHandler(logger_console_hdlr)
#    logging.getLogger("").addHandler(logger_console_hdlr)
    return logger

logger = start_log("python_script",".",False)

def yes_no_question(question):
    try:
        answer = os.environ["DEBUG_YES_NO_QUES"]
        
    except:
        answer = input(question+"?(n)")
 
    yes=["y","Y","Yes","yes","YES"]
    if answer in yes:
 
        return True
    else:
        return False


# globals
#----------------------------------------------
green_open = '\033[32m'
red_open = '\033[91m'
color_close = '\033[0m'
logger = start_log("CreateBlockTree")
legal_parent_list = ["design","verif"]
legal_project_list = ["Xilinx_IPs","CommEngine","IP","Common"]
parent_name = "design"
#----------------------------------------------

def create_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def ParseArgs(imported=False):
    usage = "\n"+green_open+"for design"+color_close+": CreateBlockTree.py BLOCK_PATH\n"+green_open+"for verif"+color_close+": CreateBlockTree.py BLOCK_PATH -uvm \n"
    parser = argparse.ArgumentParser(description='Populating the desired directory to suit methodology', usage=usage, epilog='\n',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('BLOCK_PATH' , action='store' , help='the relative (to WS) path to the block you want to populate.\nfor example: \n\t\t/design/new_module\n\t\t/verif/new_module\n')
    parser.add_argument('-uvm'  , dest   = 'uvm'   , action = 'store_true' , default = False , help = 'in case it is a verification folder, make dirs for "UVM" style')
    parser.add_argument('-vivado' , dest   = 'vivado'  , action = 'store_true' , default = False , help = 'Create "vivado" folders under BLOCK_PATH')
    parser.add_argument('-dir' , dest   = 'dir'  , action = 'store_true' , default = False , help = 'Create Project SUB folders under BLOCK_PATH')
    parser.add_argument('-ovr' , dest   = 'ovr'  , action = 'store_true' , default = False , help = 'Override existing content !!!')
 

    if imported:
        return parser

    args = vars(parser.parse_args())
 #   print args
    return args

def check_args(args):
    global parent_name
    global module_name
    # label_path_department = check_label_path(args["BLOCK_PATH"])[1]
    total_splits = len (args["BLOCK_PATH"].split(os.sep))
    print (total_splits)
    parent_name = args["BLOCK_PATH"].split(os.sep)[1]
    if total_splits == 3:
       logger.error("invalid path: must be --> /design/Project_name/sub_module_name")
       module_name = args["BLOCK_PATH"].split(os.sep)[2]
       sys.exit(1)
    if total_splits == 4:
        module_name = args["BLOCK_PATH"].split(os.sep)[3]
        project_name = args["BLOCK_PATH"].split(os.sep)[2]
    print (parent_name)
    print (project_name)
    print (module_name)
    if project_name not in legal_project_list:
        logger.error("invalid parent directory. must be from those options : "+str(legal_project_list))
        sys.exit(1)
    if parent_name not in legal_parent_list:
        logger.error("invalid parent directory. must be from those options : "+str(legal_parent_list))
        sys.exit(1)
    if parent_name == "verif":
        logger.error("Not supported : "+str(parent_name))
        sys.exit(1)
        if (args["uvm"] ):
            logger.error(red_open+"Error: "+color_close+"Wrongly specified '-uvm' flags. \nexiting....")
            sys.exit(1)
        elif (not args["uvm"]):
            logger.info("No Verif block type specified, defaulting to 'UVM'")
            args["uvm"] = True;

def CreateBlockTree(dir_path, parent_name,args):
    dir_path = dir_path.strip("/")
    folder_path = os.path.join(".",dir_path)
    completeName = os.path.join(folder_path+"/src/rtl", module_name +'.sv')
    print(completeName)
    isExist = os.path.exists(completeName)
    if (isExist):
            if  (args["ovr"]==False):
                logging.error (red_open + "Module already exist !!!"+color_close)
                sys.exit(1)

    logger.info(green_open+ "Populating Block Tree for:\n\t%s" %(module_name)+color_close)
    logger.info("Remember to check 'CreateBlockTree.py -h' to add extra 'non mandatory' directories to your block.")
#    if not yes_no_question("\nProceed "):
#        sys.exit(1)

    if parent_name == "design" : #design
                create_dir(folder_path +"/src/rtl")
                create_dir(folder_path +"/tb")

    if (args["dir"] ):
            # create mandatory directories
        # --------------------------------------------------------------
        if parent_name == "design" : #design
                create_dir(folder_path +"/sim")
                create_dir(folder_path +"/scripts")
                create_dir(folder_path +"/src/pkg")
                create_dir(folder_path +"/src/Xilinx_IPs")
        elif parent_name == "verif" : # verif
                create_dir(folder_path +"/tb")
                create_dir(folder_path +"/if")
                create_dir(folder_path +"/src")
                create_dir(folder_path +"/inc")
                create_dir(folder_path +"/cov")
                os.symlink("../../../SOD",folder_path+"/sim")
                create_dir(folder_path +"/tests")
                create_dir(folder_path +"/setup")
                create_dir(folder_path +"/seq")

    
        # create optioanl directories
        # --------------------------------------------------------------
        if parent_name == "design" : # design
    
    
            if args["vivado"]:
                create_dir(folder_path +"/vivado_project")
  
    
    # create files
    UserName = getpass.getuser()
    today = datetime.today()
#    open(folder_path + '/release_notes.txt','a').close()
##############################
# Writing a rtl src file
##############################
    completeName = os.path.join(folder_path+"/src/rtl", module_name +'.sv')
    open(completeName ,'a').close() 
    rtl_file = open(completeName, "w")
    rtl_file.write("`timescale 1ns / 1ns\n")
    rtl_file.write("//////////////////////////////////////////////////////////////////////////////////\n")
    rtl_file.write("// Company: \tGuardknox.com\n")
    rtl_file.write("// Engineer: \t" + UserName + "\n" )
    rtl_file.write("//\n")
    rtl_file.write("%s %s \n" %("// Create Date: " ,today ))
    rtl_file.write("// Module Name:  " + module_name +"\n")
    rtl_file.write("// Project Name: CommEngine\n")
    rtl_file.write("// Description:\n")
    rtl_file.write("//\n")
    rtl_file.write("// Additional Comments:\n")
    rtl_file.write("//\n")
    rtl_file.write("//////////////////////////////////////////////////////////////////////////////////\n")


    rtl_file.write("module " + module_name + "#(\n")
    rtl_file.write("parameter PARAM = 0")
    rtl_file.write(")(\n")
    rtl_file.write("input logic clk,\t//Clock Signal \n")
    rtl_file.write("input logic reset,\t//Active High reset signal \n")
    rtl_file.write("output logic led\t//LED Active High Output signal\n")
    rtl_file.write(");\n")
    rtl_file.write("\n")
    rtl_file.write("\n")
    rtl_file.write("\n")
    rtl_file.write("endmodule\n")

    rtl_file.close()  
 #   print(datetime.now())
 #   print (today)



##############################
# Writing a test bech template
##############################
    completeName = os.path.join(folder_path+"/tb/", module_name +'_tb.sv')
    open(completeName ,'a').close() 
    rtl_file = open(completeName, "w")
    rtl_file.write("`timescale 1ns / 1ns\n")
    rtl_file.write("//////////////////////////////////////////////////////////////////////////////////\n")
    rtl_file.write("// Company: \tGuardknox.com\n")
    rtl_file.write("// Engineer: \t" + UserName + "\n" )
    rtl_file.write("//\n")
    rtl_file.write("%s %s \n" %("// Create Date: " ,today ))
    rtl_file.write("// Module Name:  " + module_name +"_tb.sv\n")
    rtl_file.write("// Project Name: CommEngine\n")
    rtl_file.write("// Description:\n")
    rtl_file.write("//\n")
    rtl_file.write("// Additional Comments:\n")
    rtl_file.write("//\n")
    rtl_file.write("//////////////////////////////////////////////////////////////////////////////////\n")
    rtl_file.write("module " + module_name + "_tb;#(\n")
    rtl_file.write("\n")
    rtl_file.write("reg  clk;\n")
    rtl_file.write("\n")
    rtl_file.write("always #10 clk =~clk;\n")
    rtl_file.write("\n")

    rtl_file.write( module_name  + "\tuut (\n")
    rtl_file.write( "\t\t\t.clk(clk),\n")
    rtl_file.write( "\t\t\t.reset(reset));\n")

    rtl_file.write("iinitial begin \n")
    rtl_file.write("clk <= 0; \n")
    rtl_file.write("reset <=1;\n")
    rtl_file.write("#20 reset <= 0;\n")
    rtl_file.write("\n")
    rtl_file.write("\n")
    rtl_file.write("\n")
    rtl_file.write("endmodule\n")
    rtl_file.close()  
#   print(datetime.now())
#   print (today)
def main():
    args = ParseArgs()
 #   print args
    check_args(args)
    CreateBlockTree(args["BLOCK_PATH"],parent_name,args)

if __name__=="__main__":
    if len(argv)<2:
        logger.error("Missing arguments, try 'CreateBlockTree.py -h' for help")
    else:
        ParseArgs()
        main()
