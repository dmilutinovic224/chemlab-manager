Laboratorijski informacijski sistem za hemijska istraživanja

ChemLab Manager je laboratorijski informacioni sistem rađen kao studentski projekat na temu primene računarske hemije u web okruženju. Aplikacija omogućava upravljanje hemijskim jedinjenjima, literaturom, eksperimentima i lab inventarom, sa posebnim fokusom na vizuelizaciju molekulskih struktura i automatsko računanje hemijskih svojstava.

Funkcionalnost
Autentifikacija i autorizacija
Registracija novih korisnika
Prijava i odjava
Korisnički profil sa mogućnošću uređivanja
Brisanje profila (podaci korisnika ostaju u bazi)
Dve admin grupe: superuser i staff

Jedinjenja (Compounds)
Dodavanje, pregled, ažuriranje i brisanje hemijskih jedinjenja
SMILES notacija za 3D prikaz strukture
3D interaktivni prikaz molekula (3Dmol.js + NCBI iCn3D)
Automatsko računanje svojstava iz SMILES (logP, TPSA, H-donori, H-akceptori)
Kategorizacija jedinjenja (organska, neorganska, polimeri…)
Komentari i beleške
Pretraga 


Literatura (Literature)
Dodavanje, pregled, ažuriranje i brisanje naučnih radova
Praćenje autora, časopisa, DOI
Upload PDF fajlova
Beleške uz radove

Eksperimenti (Experiments)
Dodavanje, pregled, ažuriranje i brisanje eksperimenata
Praćenje statusa (planiran, u toku, završen, neuspešan)
Tipovi eksperimenata (sinteza, karakterizacija, računarski...)
Beleške uz eksperimente

Inventar (Inventory)
Dodavanje hemikalija (Chemical)
Dodavanje dobavljača (Supplier)
Praćenje serija (Batch) sa količinama i rokovima
Beleške uz serije

Asinhroni zadaci (Celery)
Automatsko računanje svojstava iz SMILES
Automatsko generisanje 3D struktura




REST API
Kompletan REST API za sve modele
Autentifikacija putem tokena
Browsable API interfejs
Filtriranje, pretraga i paginacija

Alati
Backend:	Django 5.2, Django REST Framework
Baza podataka:	SQLite (razvoj), PostgreSQL (produkcija)
Asinhroni zadaci:	Celery, Redis
Hemijska informatika:	RDKit
Frontend:	Bootstrap 5, Bootstrap Icons, 3Dmol.js
Version control:	Git
Deployment:	PythonAnywhere

Struktura aplikacija
Aplikacija	Opis
core	             glavna aplikacija – jedinjenja, svojstva, komentari, kategorije
accounts	korisnički nalozi, profil, registracija, prijava
literature	naučni radovi i beleške
experiments	eksperimenti i beleške
inventory	inventar, hemikalije, serije, dobavljači
api	             REST API endpointi


Instalacija
Python 3.10+
Redis server (opciono)
Git
Conda (za RDKit)
--------------------------
git clone https://github.com/dmilutinovic224/chemlab-manager.git
cd chemlab-manager

python -m venv venv
venv\Scripts\activate      
pip install -r requirements.txt

za RDKit (u conda)
conda create -n rdkit_env python=3.10
conda activate rdkit_env
conda install -c conda-forge rdkit
pip install celery redis django djangorestframework pillow django-crispy-forms crispy-bootstrap5

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver   


Da bi se  omogucio prikaz 3D struktura na lokalnoj mašini neophodno je instalirati miniconda okruženje za verzije Python 3.10+ iz razloga što novije verzije pajtona ne podržavaju RTKit library. 
Instalacija redis:
https://github.com/tporadowski/redis/releases - preuzimanje
C:\Redis  (raspakovati ovde)
Nakon instalacije i pokretanja svih navedenih komandi u conda, potrebno je otvoriti tri conda terminala:
I terminal(za redis):
cd C:\Redis
.\redis-server.exe

II terminal(celery zadaci):
conda activate rdkit_env
cd putanja do projekta
celery -A Projekat worker --loglevel=info --pool=solo

III terminal(pokretanje lok servera):
conda activate rdkit_env
cd putanja do projekta
python manage.py runserver

5.3. Pokretanje Celery
redis-server
celery -A Projekat worker --loglevel=info --pool=solo

API 
Metoda	Endpoint	Opis
GET	/api/compounds/	Lista spojeva
GET	/api/compounds/{id}/	Detalji spoja
POST	/api/compounds/	Kreiraj spoj
PUT	/api/compounds/{id}/	Ažuriraj spoj
DELETE	/api/compounds/{id}/	Obriši spoj
GET	/api/literature/	Lista literature
GET	/api/experiments/	Lista eksperimenata
GET	/api/chemicals/	Lista hemikalija
GET	/api/users/	Lista korisnika

Testovi
Komponenta	Broj testova
Models  20+
Forms	   10+
Views 15+
API	    5+

Deploy
PythonAnywhere
Aplikacija je deployvana na PythonAnywhere:
https://dmilutinovic224.pythonanywhere.com


Napomena: pošto je u pitanju školski primer i koristi se besplatna verzija, asinhrone operacije poput generisanja 3d strukture i računanja svojstava na osnovu smiles inputa nece biti prikazane.

Reference
1.	https://www.rdkit.org/ open source chemoinformatics – korišćeno za hem proračune
2.	https://www.ncbi.nlm.nih.gov/ online prikaz 3d struktura
3.	https://www.daylight.com/dayhtml/doc/theory/theory.smiles.html info o smiles notaciji
4.	https://3dmol.csb.pitt.edu/ JavaScript biblioteka za prikaz 3D molekula u pretraživaču
5.	https://github.com/tporadowski/redis/releases  link za preuzimanje redis-a

--------------------------

korisna literatura:
•	Bjerrum, E. J. et al. PySMILESUtils – Enabling deep learning with the SMILES chemical language. AstraZeneca, Gothenburg, Sweden.
•	Hill, C. Python for Chemists. International Atomic Energy Agency (IAEA).
•	Računarska hemija – skripta
