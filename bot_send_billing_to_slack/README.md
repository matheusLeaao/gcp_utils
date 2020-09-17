# gcp_utils
# Matheus Lion

### Celular: 
+55 (11) 9 6484-5375

### Facebook: 
https://www.facebook.com/matheus.leao.5?ref=bookmarks

### LinkedIn: 
https://www.linkedin.com/in/matheus-le%C3%A3o-622151162/

## Projeto voltado a:
Projeto designado para o desenvolvimento de bot que envia o billing de um determinado horário da conta da GCP.

## Passo a passo para implementação
- Acessar Biling
- Habilitar o account Management para o Projeto (para obter o Billing Account ID)
- Billing Export
- Habilitar o Export Billing para um determinado Dataset (criar Dataset para que o billing seja exportado e armazenado)
- <PROJECT_ID>.<DATASET>.gcp_billing_export_v1_<BILLING_ACCOUNT_ID>
- criar a Function com trigger type HTTP
- Deploy da Function (OK status)
- Testar a saída (acessar a URL da function, é para mostrar o billing no navegador e enviar a mensagem ao Slack)
- Criar o Job Scheduler (Configurar a frequencia desejada em unix-cron format https://crontab.guru/,Timezone: Brasilia Standar Time (BRT), Target: HTTP, URL: function_url, HTTP method: POST)
- GG Easy lek
