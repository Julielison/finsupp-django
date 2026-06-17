Agendamento (django-crontab)

Após instalar dependências, registre os jobs de cron:

```bash
pip install -r requirements.txt
python manage.py crontab add
```

Verificar jobs instalados:

```bash
python manage.py crontab show
```

Remover jobs:

```bash
python manage.py crontab remove
```

O job configurado chama `generate_bills` diariamente às 02:00 do servidor.
