For local run APP:

INSTALL:

1. postgressql
2. pytho3.9
3. requirements

Configuration postgresql

sudo su - postgres -c "initdb --locale ru_RU.UTF-8 -E UTF8 -D '/var/lib/postgres/data'"
sudo chown -R postgres:postgres /var/lib/postgres/
systemctl start postgresql

