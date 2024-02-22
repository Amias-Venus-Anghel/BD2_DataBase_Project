
Aplicatia se poate rula astfel:

python3 raports.py sau python3.9 raports.py

*Inainte de rurale* 

+ Sunt necesare instalarile:
    pip install mysql-connector-python
    pip install matplotlib
    pip install numpy
    pip install pandas

+ Baza de date se creeaza in MySQL Workbench. Trebuie retinute numele si parola bazei de date.
+ Pentru baza de date din MySQL trebuie rulate comenzile din urmatoarele fisiere:

    o Creare si populare cu date: 
        script_creare_populare_bd

    o Procedurile stocate:
        procedura_vanzariprodtop
        procedura_sologamesproducer
        procedura_gameselection

+ Modificari necesare in cod pentru conectarea la baza de date in scriptul raports.py:

connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='password',
            database='database',
            port=3306
        )
