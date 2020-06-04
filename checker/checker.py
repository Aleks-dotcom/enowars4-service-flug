#!/usr/bin/env python3
#socat TCP-LISTEN:1337,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"
from pwn import *
import sys
import time
from enochecker import *
import string
from random import randrange

class FlugChecker(BaseChecker):

    flag_count = 1
    noise_count = 1
    havoc_count = 1
    port = 1337


    def putflag(self):  # type: () -> None
        username = self.gen_user()
        password = self.gen_password()
        try:
            print('Connecting ...')
            #p = remote(self.address,port)
            p= remote('localhost',1337)
            print("Connection succeded")
        except:
            raise EnoException("Unable to connect to the service at putflag")
        try:
            print("Reistering a user with username: {} and password {}".format(username,password))
            p.recvuntil(b"================")
            p.sendlineafter(b"================",b"2")
            p.sendlineafter(b"Please input your new username:",bytes(username,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(username,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Enter the content of your new ticket\n")
            print("Putting in flag: {}".format(self.flag))
            p.sendline(bytes(self.flag,'ascii'))
            time.sleep(.1)
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            stdo = p.recvline()
            ticket_id = p.recvline().decode('ascii').split(" ")[1]
            print("The new flag is at index: {}".format(ticket_id))
            self.team_db[self.flag] = (username,password,ticket_id)
        except:
            raise EnoException("Put flag failed")

    def getflag(self):  # type: () -> None
        try:
            print('Connecting ...')
            #p = remote(self.address,port)
            p= remote("localhost",1337)
            print("Connection succeded")
        except:
            raise EnoException("Connection failed at getflag")

        try:
            print('Retrieveng Flag ...')
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n","3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.flag][2],'ascii'))
            p.recvline()
            p.recvline()
            flag2 = p.recvline().decode('ascii')
            print('flag retireved: {}'.format(flag2))
            print('flag should be: {}'.format(self.flag))
            if flag2.strip() != self.flag.strip():
                raise EnoException("The flags dont mach!")
        except:
            raise EnoException("Unable to put flag in the service")

    def putnoise(self):  # type: () -> None
        username = self.gen_user()
        password = self.gen_password()
        try:
            print('Connecting ...')
            #p = remote(self.address,port)
            p = remote('localhost',1337)
            print("Connection succeded")
        except:
            raise EnoException("Connection failed at put noise")
        try:
            print('Puting in noise with username: {} and password: {}'.format(username,password))
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            p.sendlineafter(b"Please input your new username:\n",bytes(password,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(password,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Enter the content of your new ticket\n")
            p.sendline(bytes(self.noise,'ascii'))
            print('puting in noise: {}'.format(self.noise))    
            time.sleep(.1)
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            stdo = p.recvline()
            noise_id = p.recvline().decode('ascii').split(' ')[1]
            print('Noise is set at id: {}'.format(noise_id))
            self.team_db[self.noise] = (username,password,noise_id)

        except:
            raise EnoException("Put noise failed")


        self.team_db["noise"] = self.noise

    def getnoise(self):  # type: () -> None
        try:
            print('Connecting ...')
            #p = remote(self.address,port)
            p= remote("localhost",1337)
            print("Connection succeded")
        except:
             raise EnoException("Connection at getnoise failed")

        try:
            print("Getting noise ...")
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.noise][2],'ascii'))
            p.recvline()
            p.recvline()
            noise2 = p.recvline().decode('ascii') 
            print('Got noise: {}'.format(noise2))
            print('Extepcted noise: {}'.format(self.noise))                 
            if noise2.strip() != self.noise.strip():
                raise EnoException("Noises dont match")
        except:
            EnoException('Get noise failed')
        """
        This method retrieves noise in the service.
        The noise to be retrieved is inside self.flag
        The difference between noise and flag is, tht noise does not have to remain secret for other teams.
        This method can be called many times per round. Check how often using flag_idx.
        On error, raise an EnoException.
        :raises EnoException on error
        :return this function can return a result if it wants
                if nothing is returned, the service status is considered okay.
                the preferred way to report errors in the service is by raising an appropriate enoexception
        """
    def havoc(self):  # type: () -> None
        """
        This method unleashes havoc on the app -> Do whatever you must to prove the service still works. Or not.
        On error, raise an EnoException.
        :raises EnoException on Error
        :return This function can return a result if it wants
                If nothing is returned, the service status is considered okay.
                The preferred way to report Errors in the service is by raising an appropriate EnoException
        """
        self.info("I wanted to inform you: I'm  running <3")
        self.http_get(
            "/"
        )  # This will probably fail, depending on what params you give the script. :)

    def exploit(self ):
        #1st vuln
        p = remote(self.address,port)
        p.recvuntil("================\n")
        p.sendlineafter("================\n",'1')
        p.sendlineafter("Please input your username:\n",str(username))
        p.sendlineafter("Please input your password:\n",'\x00')
        p.recvline() #TODO: odstrani ko urban popravi svoje randomly placed printfe
        p.recv(2) 
        check_line = p.recvline()
        if username in check_line:
            print("You got pwnd")
        else:
            print("Sad nox")
        pass

    def gen_user(self): 
        source = list(string.ascii_lowercase)
        username =''
        for num in range(25):
            rand_int = randrange(25)
            username += source[rand_int]
        return username

    def gen_password(self): 
        source = list(string.ascii_lowercase)
        password =''
        for num in range(25):
            rand_int = randrange(25)
            password += source[rand_int]
        return password



if __name__ == "__main__":
    run(FlugChecker)
    # Example params could be: [StoreFlag localhost ENOFLAG 1 ENOFLAG 50 1]
    # exit(ExampleChecker(port=1337).run())