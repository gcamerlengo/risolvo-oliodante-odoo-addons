# Deploy Odoo con Docker

Questa cartella avvia Odoo Community 17 con PostgreSQL e monta i moduli custom da `odoo_addons`.

## Primo avvio sul server

```bash
mkdir -p oca_addons
git clone --depth 1 --branch 17.0 https://github.com/OCA/helpdesk.git oca_addons/helpdesk
cp deploy/odoo/.env.example deploy/odoo/.env
nano deploy/odoo/.env
docker compose --env-file deploy/odoo/.env -f deploy/odoo/docker-compose.yml up -d
```

Poi aprire:

```text
http://IP_SERVER:8069
```

## Aggiornare il codice

```bash
git pull
git -C oca_addons/helpdesk pull
docker compose --env-file deploy/odoo/.env -f deploy/odoo/docker-compose.yml restart odoo
```

## Installare Helpdesk OCA

Dopo l'avvio, installare il modulo tecnico `helpdesk_mgmt` dal menu App di Odoo.

In alternativa, da terminale:

```bash
docker compose --env-file deploy/odoo/.env -f deploy/odoo/docker-compose.yml exec odoo odoo -d risolvo -i helpdesk_mgmt --stop-after-init
docker compose --env-file deploy/odoo/.env -f deploy/odoo/docker-compose.yml restart odoo
```
