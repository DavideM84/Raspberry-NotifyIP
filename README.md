# Raspberry - Notify IP

Phyton script that send an email when the public IP change.  

Davide Mencarelli - d.mencarelli@outlook.com  
First release: **01/02/2021**  

## Notes

Script for Raspberry Pi  
The phyton file is **notifyIP.py**  
Add your SMTP account detail in **notifyIP.py**  
Script for **Phyton 3.7+**  

## How works

The script check current IP with the previous saved value.  
If changed send the email.  
The  current IP are saved in: '/prevIP.dat'.  
The body of the email can be changed by: '/email.tmpl' file  
