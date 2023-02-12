# Ansible Deployment

## Vorbereitung

Vor Ausführung des Playbooks müssen folgende Schritte manuell unternommen werden:

- 1x Virtuelle Maschine (VM), Ubuntu 22
- Erstellen eines Users "devops"
- Hinzufügen "devops" zu den Gruppen "sudo" und "www-data"

- Erstellung eines SSH-key-pairs:

```
ssh-keygen -t rsa
```
- Hinzufügen des public keys zu den authorized_keys auf dem Server
```
ssh-copy-id devops@VM_IP
```

- Einfügen des Server-Users in inventory.yaml:
    - ansible_user = devops
    - ansible_group = sudo
    - ansible_python_interpreter = /usr/bin/python3
    - nodejs_version = 18
- alle weiteren Variablen im inventory nach belieben ausfüllen, wenn nicht gesetzt
- Einfügen der ServerIP in "hosts" im inventory.yaml

### DNS

unter https://jweiland.net:

- Konfiguration -> Domainverwaltung -> Stark-wie-ein-Baum.de -> Bearbeiten -> Nameserver editieren
- `app.stark-wie-ein-baum` und `admin.stark-wie-ein-baum` werden jeweils ein CNAME von der Server IP
- `app42.stark-wie-ein-baum` und `admin42.stark-wie-ein-baum` existieren nur für Testzwecke und könnten gelöscht werden

Mehr braucht es dort nicht. Das handling der Subdomänen wird dann durch den Http-Server in der VM (nginx als reverse
proxy) übernommen.


### TLS, Letsencrypt

Auf dem Server läuft ein Cronjob der alle 90 Tage das TSL Zertifikat erneuert. (certbot)
