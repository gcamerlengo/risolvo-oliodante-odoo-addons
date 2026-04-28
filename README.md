# Risolvo Odoo Addons

Repository per moduli custom Odoo Community sviluppati da Risolvo.

## Contenuto

- `odoo_addons/risolvo_olio_dante_assistenza`: modulo Odoo 17 per gestione assistenza, ticket, sedi, asset, interventi e SLA.

## Uso in Odoo

Configurare Odoo aggiungendo la directory `odoo_addons` al parametro `addons_path`.

Esempio:

```bash
--addons-path=/opt/odoo/odoo/addons,/opt/odoo/custom/odoo_addons
```

Poi riavviare Odoo, aggiornare la lista applicazioni e installare il modulo desiderato.

## Deploy consigliato

Per produzione, usare un server Linux su AWS con:

- Odoo Community
- PostgreSQL
- directory `odoo_addons` clonata da questo repository
- Nginx come reverse proxy
- certificato HTTPS con Let's Encrypt
- backup automatici del database e del filestore
