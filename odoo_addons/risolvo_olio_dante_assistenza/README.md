# Risolvo - Assistenza Olio Dante

Addon Odoo per gestire i flussi di assistenza e il presidio gestionale di Olio Dante spa.

## Funzioni incluse

- Dashboard operativa con ticket aperti raggruppati per stato.
- Ticket assistenza con stati operativi: nuovo, qualificato, pianificato, in lavorazione, attesa cliente, risolto, chiuso.
- Anagrafiche sedi/reparti e asset produttivi o gestionali.
- Interventi tecnici remoti, telefonici, onsite o di analisi.
- SLA configurabili per categoria e priorita.
- Viste calendario, grafico e pivot per ticket e interventi.
- Menu rapidi per miei ticket, ticket da pianificare, SLA scaduti e interventi in corso.
- Tracciamento chatter e attivita tramite `mail.thread`.
- Menu dedicato `Risolvo Assistenza`.

## Installazione

1. Copiare la cartella `risolvo_olio_dante_assistenza` nella directory custom addons di Odoo.
2. Aggiungere la directory custom addons nel parametro `addons_path`.
3. Riavviare Odoo.
4. Aggiornare la lista applicazioni.
5. Installare `Risolvo - Assistenza Olio Dante`.

Esempio con Docker:

```bash
odoo -u risolvo_olio_dante_assistenza -d nome_database
```

## Prossimi sviluppi consigliati

- Integrazione email inbound per creare ticket automatici.
- Portale cliente per referenti Olio Dante.
- Report SLA mensile.
- Check-list interventi per reparti produttivi.
- Integrazione calendario per pianificazione tecnici.
