# Stark-Wie-Ein-Baum

["Stark wie ein Baum!“](https://www.hof-grueneberg.de/Stiftung/Stiftung-hof-grueneberg/#c1669) ist ein Gemeinschaftsprojekt des Caritas-Kinderhospizdienstes und der [Stiftung Hof Grüneberg](https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/).

https://app.stark-wie-ein-baum.de


**Projektpartner: Stiftung Hof Grüneberg**<br>
https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/

### Funktionen

- API
- SMTP
- Admin Schnittstelle
- Google Login für Admins

### Ansible Deployment
Vor Ausführung des Playbooks müssen folgende Schritte unternommen werden:
- Erstellung eines SSH-key-pairs (ssh-keygen -t rsa)
- Hinzufügen des public keys zu den authorized_keys auf dem Server (ssh-copy-id user@IP)
- Einfügen des Nutzernames und der Server IP Adresse in das Playbook

- Erstellen eines Users "devops"
- Hinzufügen "devops" zu den Gruppen "sudo" und "www-data"


### Note

Frontend Entwickler: wkrl (https://github.com/wkrl/Stark-Wie-Ein-Baum)

