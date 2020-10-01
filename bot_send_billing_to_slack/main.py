from google.cloud import bigquery
import requests
from collections import defaultdict
import datetime
import os
import requests
import sys

low_cost = 70
high_cost = 70

#definir o período atual que será pego a informacao do billing
x = datetime.datetime.now()
ano = x.year
mes = ('%02d' % x.month)


periodo = str(("%s%s" % (ano,mes))) #YYYYMM


def main(request):
   values = ""
   lista_servicos = ""
   
   client = bigquery.Client() 
   # Valores procurados 
   query_string = 'SELECT invoice.month, cost_type, SUM(cost) + SUM(IFNULL((SELECT SUM(c.amount) FROM  UNNEST(credits) c), 0)) AS total, (SUM(CAST(cost * 1000000 AS int64)) + SUM(IFNULL((SELECT SUM(CAST(c.amount * 1000000 as int64)) FROM UNNEST(credits) c), 0))) / 1000000 AS total_exact FROM `<project_ID>.<dataset>.<ID_billing_Account>` WHERE project.id = "<project_name>" AND invoice.month = "'+periodo+'" GROUP BY 1, 2 ORDER BY 1 ASC, 2 ASC;'
   query_job = client.query(query_string)
   results = query_job.result()

   for row in results:
      values = row.total
      
   client = bigquery.Client() 
   # Valores de serviços procurados 
   query_service = 'SELECT service.description, SUM (cost) AS cost FROM ``<project_ID>.<dataset>.<ID_billing_Account>`` WHERE project.id = "<project_name>" AND cost != 0 AND invoice.month = "'+periodo+'" GROUP BY service.description;'
   query_job = client.query(query_service)
   results = query_job.result()

   for row in results:
      lista_servicos += "%-40s R$%5.2f\n" % (row.description , row.cost)
      
   actual_bill = values

   if actual_bill < low_cost:
      emoji = ":money_mouth_face: Billing ta sussa!"
   elif actual_bill > high_cost:
      emoji = ":scream: ATENÇÃO @here o billing está muito alto :redsiren: \n"
   else:
      emoji = ":zany_face: ATENÇÃO @here o billing está em um nível preocupante :warning: \n"


   text = "%s Billing atual está em: ~R$%5.2f\n```Serviço                                  Custo\n%sTotal                                  ~R$%5.2f```" % (emoji,actual_bill,lista_servicos,actual_bill)

   json={
                "text": text + "",
            }

   response = requests.post('SLACKWEBHOOK', json=json)

   return str(text)
