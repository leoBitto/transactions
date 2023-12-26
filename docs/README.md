# Transactions App - Applicazione di Gestione Finanziaria

Benvenuti nell'applicazione Transactions, un'app Django per la gestione delle tue entrate, spese, asset e debiti.

## Caratteristiche Principali

1. **Registrazione delle Transazioni:** Puoi registrare entrate e spese tramite moduli dedicati. Le entrate includono categorie come "Salary", "Bonus", ecc., mentre le spese includono categorie come "Food", "Transport", ecc.

2. **Visualizzazione dei Dati Finanziari:** L'app offre una dashboard per visualizzare un riepilogo delle entrate e spese nel tempo. Vengono mostrati grafici a torta per le categorie di entrate e spese, nonché grafici a linee che tracciano le entrate e le spese nel corso del tempo.

3. **Controlli di Bilancio:** Prima di registrare una spesa, l'app esegue controlli per assicurarsi che il saldo del conto o del saldo cash non diventi negativo.

## Come Utilizzare l'App

### Requisiti

- Python 3.7 o versioni successive
- Django 3.1 o versioni successive
- Pacchetti Python aggiuntivi elencati in `requirements.txt`

### Installazione

1. Clona il repository dell'app:

   ```bash
   git clone https://github.com/leoBitto/transactions.git
Naviga nella directory del progetto:

cd transactions
Crea un ambiente virtuale (consigliato) e attivalo:

python3 -m venv venv
source venv/bin/activate
Installa i requisiti:

pip install -r requirements.txt
Applica le migrazioni:


python manage.py migrate
Avvia il server di sviluppo:


python manage.py runserver
Accedi all'app nel tuo browser all'indirizzo http://localhost:8000.

Uso dell'App
Dashboard: Accedi all'area protetta per visualizzare i tuoi dati finanziari, grafici e riepiloghi delle entrate e delle spese.

Registrazione delle Transazioni: Utilizza i moduli dedicati per registrare nuove entrate e spese. I controlli di bilancio assicurano che le spese non portino il conto o il saldo cash a un valore negativo.

Contributi
Se vuoi contribuire all'applicazione Transactions, sentiti libero di aprire un problema o inviare una richiesta pull nel repository GitHub: https://github.com/leoBitto/transactions

Licenza
L'applicazione è distribuita con licenza MIT. Consulta il file LICENSE per ulteriori dettagli.


# Documentazione dei Modelli

## Modello Bank Account

Il modello `BankAccount` rappresenta un'entità di un conto bancario.

- **Campi**:
  - `bank_name` (CharField): Il nome della banca associata al conto.
  - `balance` (DecimalField): Il saldo attuale del conto.
  - `start_date` (DateField): La data in cui è stato creato il conto.

- **Metodi**:
  - `transfer_money(target_account, amount, commissione)`: Trasferisce denaro da questo conto a un altro conto bancario.
  - `withdraw_money(amount, commissione)`: Preleva denaro dal conto.
  - `total_balance`: Calcola il saldo totale del conto fino alla data corrente.

## Modello Cash

Il modello `Cash` rappresenta un'entità contante.

- **Campi**:
  - `amount` (DecimalField): L'importo contante attuale.
  - `start_date` (DateField): La data in cui è stata creata l'entità contante.

- **Metodi**:
  - `total_amount`: Calcola l'importo totale del contante fino alla data corrente.

## Modello BalanceLog

Il modello `BalanceLog` registra le modifiche al saldo di un conto bancario.

- **Campi**:
  - `bank_account` (ForeignKey a BankAccount): Il conto bancario associato al registro del saldo.
  - `balance` (DecimalField): Il saldo al momento dell'entrata nel registro.
  - `timestamp` (DateTimeField): Il timestamp dell'entrata nel registro.

## Modello AmountLog

Il modello `AmountLog` registra le modifiche all'importo del contante.

- **Campi**:
  - `cash` (ForeignKey a Cash): L'entità contante associata al registro dell'importo.
  - `amount` (DecimalField): L'importo al momento dell'entrata nel registro.
  - `timestamp` (DateTimeField): Il timestamp dell'entrata nel registro.

## Modello Transaction

Il modello `Transaction` rappresenta una transazione finanziaria.

- **Campi**:
  - `date` (DateField): La data della transazione.
  - `amount` (DecimalField): L'importo della transazione.
  - `description` (CharField, opzionale): Una descrizione della transazione.
  - `bank_account` (ForeignKey a BankAccount, opzionale): Il conto bancario associato alla transazione.
  - `cash` (ForeignKey a Cash, opzionale): L'entità contante associata alla transazione.


## Modello Income

Il modello `Income` estende il modello `Transaction` per le transazioni di entrata.

- **Campi Aggiuntivi**:
  - `type` (CharField): Il tipo di entrata (ad esempio, stipendio, bonus).

## Modello Expenditure

Il modello `Expenditure` estende il modello `Transaction` per le transazioni di spesa.

- **Campi Aggiuntivi**:
  - `type` (CharField): Il tipo di spesa (ad esempio, cibo, bollette).

## Modello InvestmentAccount

Il modello `InvestmentAccount` rappresenta un conto d'investimento.

- **Campi**:
  - `account` (OneToOneField a BankAccount): Il conto bancario associato.
  - `portfolio` (ForeignKey a Portfolio, opzionale): Il portafoglio associato al conto d'investimento.



