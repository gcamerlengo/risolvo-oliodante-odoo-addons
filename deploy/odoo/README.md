# Deploy Odoo con Docker

Questa cartella avvia Odoo Community 17 con PostgreSQL e monta i moduli custom da `odoo_addons`.

## Primo avvio sul server

```bash
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
docker compose --env-file deploy/odoo/.env -f deploy/odoo/docker-compose.yml restart odoo
```
