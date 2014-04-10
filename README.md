spaf
====

Static Php Analysis and Fuzzer

Description :
------------

This tool WILL NOT sploit any php scripts for you. It's a recon and helper tool for preparing pentest on local environment.

The aim of this tool is to identify every entry points of scripts (user-controlled inputs).
The included fuzzer send random printable data on each entry point, and then display every triggered logs.

Input arguments :
-----------------

usage: main.py [-h] -d FOLDER [-f] [-o OUTPUT] [-c COOKIES] [-n NB_TESTS] -u
               URL [-r] [-l LOG_FILE]

    - h, --help : show this help message and exit
    - d FOLDER, --directory : Php script folder matching the -u argument
    - f, --fuzz : Perform fuzzing on every entry point (optional)
    - o OUTPUT, --output : output type (pretty or json)
    - c COOKIES, --cookies : cookies to use durng fuzzing (ex : PHPSESSID=1234567890&logged=true )
    - n NB_TESTS, --nbtests : Number of random string to send during the fuzzing
    - u URL, --url URL : Url matching folder value
    - r, --recursive : Recursive file search in folder
    - l LOG_FILE, --logfile : If you want to display logs erros triggered by fuzzing, put your error.log full path here

Usage :
-------

####List entry points :

    foo@bar ~/spaf> ./main.py -d "/var/www/exemple_script/" -r

    [*] Start static scan
    [+] /var/www/exemple_script/admin/gauche.php
     | [GET] line 54 : f_sid
    [+] /var/www/exemple_script/languages/russian.php
     | [GET] line 168 : id_modif
    [+] /var/www/exemple_script/admin/titre.php
     | [GET] line 18 : lang_edit
     | [POST] line 36 : save

####Fuzz entry points :

    foo@bar ~/spaf> ./main.py -d "/var/www/exemple_script/" -u "http://localhost/exemple_script/" -r -l "/var/log/apache2/error_log" -f

    [*] Start static scan
    [*] Start fuzzing
    2%
    [...]
    100%
    [+] 200 get : http://localhost/exemple_script/admin/gauche.php
     |
     | f_sid : 0x65492634475f4b355b57456056492a633a51556b6f6f4051335d475279623c3a
    
    [+] 200 get : http://localhost/exemple_script/languages/russian.php
     |
     | id_modif : 0x3124560a5d7343765467295d3d4261447d49273d205f725073606576685b6a4a
     |
     |- logs :
     |
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Stack trace:
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP   1. {main}() /var/www/exemple_script/languages/russian.php:0
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Notice:  Undefined variable: chem_absolu in /var/www/exemple_script/languages/russian.php on line 48
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Stack trace:
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP   1. {main}() /var/www/exemple_script/languages/russian.php:0
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Notice:  Undefined variable: exemple_script_ext in /var/www/exemple_script/languages/russian.php on line 94
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Stack trace:
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP   1. {main}() /var/www/exemple_script/languages/russian.php:0
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Notice:  Undefined variable: exemple_script_version in /var/www/exemple_script/languages/russian.php on line 307
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Stack trace:
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP   1. {main}() /var/www/exemple_script/languages/russian.php:0
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Notice:  Undefined variable: exemple_script_version in /var/www/exemple_script/languages/russian.php on line 308
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Stack trace:
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP   1. {main}() /var/www/exemple_script/languages/russian.php:0
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Notice:  Undefined variable: exemple_script_version in /var/www/exemple_script/languages/russian.php on line 309
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Stack trace:
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP   1. {main}() /var/www/exemple_script/languages/russian.php:0
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Notice:  Undefined variable: exemple_script_version in /var/www/exemple_script/languages/russian.php on line 525
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP Stack trace:
     | [Thu Apr 10 14:17:47 2014] [error] [client 127.0.0.1] PHP   1. {main}() /var/www/exemple_script/languages/russian.php:0

    [+] 200 post : http://localhost/exemple_script/admin/titre.php
     |
     | save : 0x6539402e583e2b2f5b61724a09357b456b386e5b5b63552a447d232963283453
    
    [+] 200 get : http://localhost/exemple_script/admin/titre.php
     |
     | lang_edit : 0x6539402e583e2b2f5b61724a09357b456b386e5b5b63552a447d232963283453

License :
---------

    "THE BEER-WARE LICENSE" (Revision 42):
    ganapati@kalkulators.org> wrote this file. As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy me a beer in return. Ganapati
