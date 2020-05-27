#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#define BUFF_LEN 200
#define STR_(X)
#define STR(X) STR_(X)
#define MAXDATA 1000


char mystrcmp(char str1[], char str2[]){
    int len=strlen(str1)+1;
    
    
    for (int i=0; i<len; i++){
        if (str1[i]!=str2[i]){
            printf("zadnji char %c\n", str1[i]);
            return str1[i];
        }
    }
    
    return 0;
}


int register_user(){
	char new_username[BUFF_LEN + 1];
    char new_password[BUFF_LEN + 1];
    
    puts("Please input your new username:");
    scanf("%" STR(BUFF_LEN) "s", new_username);
    puts("Please input your password:");
    scanf("%" STR(BUFF_LEN) "s", new_password);
    
    char new_user_file[BUFF_LEN + 7];
    strcpy(new_user_file, "users/");
    strcat(new_user_file, new_username);
    
    //prevert mormo če user že obstaja
    
    FILE* userfile=fopen(new_user_file, "w");
    fprintf(userfile, "%s %s\n", new_username, new_password);
    
    fclose(userfile);
}


long random_64_bit(){
    //TODO: should be replace with 64-bit rand()
    srand(time(NULL));
    uint64_t random_num = (((uint64_t) rand() <<  0) & 0x00000000FFFFFFFFull) | (((uint64_t) rand() << 32) & 0xFFFFFFFF00000000ull);
    return random_num;
    
}

int count_lines(char path[]){
    FILE * fp = fopen(path, "r"); 
    int count = 0;
    char c;

    if (fp == NULL) { 
        puts("Sorry, this user doesn't exist"); 
        return -1; 
    } 
  

    for (c = getc(fp); c != EOF; c = getc(fp)) {
        if (c == '\n')  
            count = count + 1; 
    }

    fclose(fp); 
    return count; 
}

int add_ticket(char username[]){
    uint64_t random = random_64_bit();
    char path[BUFF_LEN+7];

    strcpy(path,"users/");
    strcat(path,username);

    int lines = count_lines(path);

    if (lines != -1){

        FILE * userfile = fopen(path,"a+");

        fprintf(userfile,"%d %ld\n",lines,random);
        printf("loaded a new ticket on index %d\n",lines);
        fclose(userfile);

        char tickets_path[BUFF_LEN +7];
        char stringify_random[20];

        sprintf(stringify_random,"%ld",(uint64_t)random);
        strcpy(tickets_path,"tickets/");
        strcat(tickets_path,stringify_random);

        FILE * tickets_file = fopen(tickets_path,"w");
        char ticket_text[201]; 

        puts("Enter the content of your new ticket");
        getc(stdin); //flush stdin so we can use fgets insted of scanf since scanf cant take in spaces.
        fgets(ticket_text,200,stdin);

        fprintf(tickets_file,"%s\n",ticket_text);
        fclose(tickets_file);

    }else{
        return 0;
    }
}

int view_ticket(){

    char id[20];
    puts("Enter the unique id of your ticket");
    scanf("%20s",id);

    char path[30];
    strcpy(path,"tickets/");
    strcat(path,id);

    FILE * ticket = fopen(path,"r");
    if (ticket == NULL){
        puts("That is not a valid id");
        return 1;
    }

    char data[MAXDATA];
    puts("The contents of your ticket:");

    while (fgets(data, MAXDATA, ticket) != NULL){
        
        printf("%s", data);
    }

    fclose(ticket);
}


int print_menu1(){
    puts("Welcome to the airport");
    puts("======================");
    puts("How can we help you today?");
    puts("The menu");
    puts("================");
	puts("1: login");
    puts("2: register");
    puts("3: view ticket");
    puts("4: exit");
    puts("================");
    
}


int print_menu2(char usename[]){
    puts("\n");
    printf("wellcome %s\n",usename);
    puts("The menu");
    puts("================");
    puts("1: buy ticket");
    puts("2: view my tickets");
    puts("3: view tickets");
    puts("4: logout");
    puts("================");

}


int view_my_tickets(char username[]){
    char path[BUFF_LEN + 8];
    strcpy(path,"users/");
    strcat(path,username);
    FILE * tickets = fopen(path,"r");

    if(tickets == NULL){
        puts("something went really wrong! This should not happen");
        return 1;
    }

    char data[MAXDATA];
    while (fgets(data, MAXDATA, tickets) != NULL){
        printf("%s", data);
    }

    fclose(tickets); 
}


int login(){
    char username_put_in[BUFF_LEN + 1];
    char password_put_in[BUFF_LEN + 1];
    char username[BUFF_LEN + 1];
    char password[BUFF_LEN + 1];
    
    
    puts("Please input your username:");
    scanf("%" STR(BUFF_LEN) "s", username_put_in);
    puts("Please input your password:");
    scanf("%" STR(BUFF_LEN) "s", password_put_in);
    
    char user_file_path[BUFF_LEN + 7];
    strcpy(user_file_path, "users/");
    strcat(user_file_path, username_put_in);
    
    
    FILE* fptr=fopen(user_file_path, "r");
    if(!fptr){
        puts("username does not exist");
        
        return -1;
    }
    
    fscanf(fptr, "%s %s", username, password);
    
    if(mystrcmp(password_put_in, password)){
        puts("password is wrong");
        return -1;
    }
    //TODO: nov meni za add ticket
    //TODO: while loop za logiko ko si loged in idk.
    //TODO: SOCAT
    char Input[8];
    while (1){
        print_menu2(username);
        scanf("%3s",Input);

        if(Input[0] == '1'){
            add_ticket(username);

        }else if(Input[0] == '2'){
            view_my_tickets(username);

        }else if(Input[0] == '3'){
            view_ticket();

        }else if(Input[0] == '4'){
            return 0;

        }else{
            puts("Invalid option try again");

        }

    }
    
    puts("password is ok");
    puts("you could log in but it is not implemented");
    
    fclose(fptr);
}


int main(){
    char S[8];
    
    
    while(1){
        print_menu1();
        scanf("%3s", S);

        if(S[0] == '1'){ //login
            login();

        } else if(S[0] == '2'){ //register
            register_user();

        } else if(S[0] == '3'){
            puts("your could view a ticket here but it is not implemented");

        } else if(S[0] == '4'){
            puts("Bye");
            exit(0);

        } else {
            puts("chose again");
            
        }
        sleep(0.5);
        puts("\n");
        
    }   
	return 0;
}
