import re

#this can only assemble code that is 10,000 lines or less 
#need to remove all spaces in the file 


def openFile():
    print("input name of file you would like to compile")
    program_to_translate = input().strip()
    
    asmFile = open(program_to_translate, "r")
    lines = asmFile.readlines()
    return lines

def writeHack(binary):
    hackFile = open("new Hack File", "w+")
    for code in binary:
        hackFile.write(code)
        hackFile.write('\n')
    
    hackFile.close()
    
    
def RemoveComments(lines):
    comments_removed = []
    for line in lines:
        line = line.strip('\n')
        comments_removed.append(re.split("//",line)[0])
    return(comments_removed)
            
def convert(lines_with_removed_comments, dict_of_variables):
    lines = lines_with_removed_comments
    binary = []
    variables = dict_of_variables
    
   
   #first pass
    for line in lines:

        if(line != ''):
    
            if(line[0] == '('):
                #we are dealing with a jump point
                int_form = int(variables[line])
                binary_form = bin(int_form)
                binary.append((binary_form[2:].zfill(16))) #strips the '0b'            
    
    #second pass 
    for line in lines:
        if(line != ''):
            if(';' in line): # no dest
                dest_bits = '000'
                comp_code, jump_code = line.split(';')
                
                computation_bits = '111' + setCompBits(comp_code)
                jump_bits = setJumpBits(jump_code)
                binary_code = (computation_bits + dest_bits + jump_bits).zfill(16)
                binary.append(binary_code)                
                
            elif('=' in line): # no jump
                jump_bits = '000'
                dest_code, comp_code = line.split('=')
                computation_bits = '111' + setCompBits(comp_code)
                dest_bits = setDestBits(dest_code)
                
                binary_code = (computation_bits + dest_bits + jump_bits).zfill(16)
                binary.append(binary_code)                
            
            elif(line[0] == '@'):
                #setting 'A' register to a number (directly)
                if(line[1].isnumeric()):
                    int_form = int(line[1:])
                    binary_form = bin(int_form)
                    binary.append((binary_form[2:].zfill(16))) #strips '0b'
                    
                else:
                    #setting 'A' register to a variable 
                    variable = line[1:]
                    if(variable in dict_of_variables.keys()):
                        int_form = int(dict_of_variables[variable])
                        binary_form = bin(int_form)
                        binary.append((binary_form[2:].zfill(16)))

  
        
    return binary

def setJumpBits(jump_code:str):
    jmp = jump_code.strip()
    jmp_bits = '000'
    
    if(jmp == 'JGT'):
        jmp_bits = '001'
    elif(jmp == 'JEQ'):
        jmp_bits = '010'
    elif(jmp == 'JGE'):
        jmp_bits = '011'  
    elif(jmp == 'JLT'):
        jmp_bits = '100'   
    elif(jmp == 'JNE'):
        jmp_bits = '101'
    elif(jmp == 'JLE'):
        jmp_bits = '110'
    elif(jmp == 'JMP'):
        jmp_bits = '111' 
    
    return jmp_bits
    
    
def setDestBits(dest_code: str):
    dest = dest_code.strip()
    if(dest == 'M'): 
        dest_bits = '001'
    elif(dest == 'D'): 
        dest_bits = '010'
    elif(dest == 'MD'): 
        dest_bits = '011'  
    elif(dest == 'A'):  
        dest_bits = '100' 
    elif(dest == 'AM'):  
        dest_bits = '101'   
    elif(dest == 'AD'):  
        dest_bits = '110'  
    elif(dest == 'AMD'):  
        dest_bits = '111'                     
    else:
        dest_bits = '000' #null
        
    return dest_bits

def setCompBits(compCode: str):
    comp= compCode.strip()
    if(comp == '0'):
        computation_bits = '0101010'
    elif(comp == '1'):
        computation_bits = '0111111'
    elif(comp == '-1'):
        computation_bits = '0111010'
    elif(comp == 'D'):
        computation_bits = '0001100'
    elif(comp == 'A'):
        computation_bits = '0110000'  
    elif(comp == '!D'):
        computation_bits = '0001101' 
    elif(comp == '=!A'):
        computation_bits = '0110001' 
    elif(comp == '-D'):
        computation_bits = '0001111' 
    elif(comp == '-A'):
        computation_bits = '0110011' 
    
    elif(comp == 'D+1'):
        computation_bits = '0011111'  
    elif(comp == 'A+1'):
        computation_bits = '0110111'   
    elif(comp == 'D-1'):
        computation_bits = '0001110'  
    elif(comp == 'A-1'):
        computation_bits = '0110010'   
    elif(comp == 'D+A'):
        computation_bits = '0000010'  
    elif(comp == 'D-A'):
        computation_bits = '0010011'   
    elif(comp == 'A-D'):
        computation_bits = '0000111'  
    elif(comp == 'D&A'):
        computation_bits = '0000000' 
    elif(comp == 'D|A'):
        computation_bits = '0010101'
        
    elif(comp == 'M'):
        computation_bits = '1110000'
    elif(comp == '!M'):
        computation_bits = '1110001'
    elif(comp == '-M'):
        computation_bits = '1110011'  
    elif(comp == 'M+1'):
        computation_bits = '1110111'   
    elif(comp == 'M-1'):
        computation_bits = '1110010' 
    elif(comp == 'D+M'):
        computation_bits = '1000010'   
    elif(comp == 'D-M'):
        computation_bits = '1010011'  
    elif(comp == 'M-D'):
        computation_bits = '1000111'                    
    elif(comp == 'D&M'):
        computation_bits = '1000000'   
    elif(comp == 'D|M'):
        computation_bits = '1010101'    
    
    return computation_bits

def checkForVariables(lines):
    """
    used after comments are removed
    """

        
    i=0
    current_line = 0
    dict_of_variables = {}
    for line in lines:
        if(line != ''): #not empty string
            
            if(line[0] == '@' and ((line in dict_of_variables.keys()) == False)):
                if(line[1].isnumeric() == False):
                 #this is a variable declaration
                    dict_of_variables[line] = 10000+i
                    i += 1
                
            elif(line[0] == '(' and ((line in dict_of_variables.keys()) == False)):
                #declaring a jump point
                dict_of_variables[line] = current_line + 1
                
        current_line +=1 
    return (dict_of_variables)        
            
                


comments_Removed = RemoveComments(openFile())
dict_of_variables = checkForVariables(comments_Removed)
binary = convert(comments_Removed, dict_of_variables)
writeHack(binary)






