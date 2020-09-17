from google.cloud import bigquery
import requests
from collections import defaultdict
import datetime
import os
import requests
import sys

low_cost = #valor mínimo orçamento
high_cost = #valor máximo orçamento


def main(request):
   values = ""
   client = bigquery.Client() 
   # Valores procurados 
   query_string = 'SELECT invoice.month, cost_type, SUM(cost) + SUM(IFNULL((SELECT SUM(c.amount) FROM  UNNEST(credits) c), 0)) AS total, (SUM(CAST(cost * 1000000 AS int64)) + SUM(IFNULL((SELECT SUM(CAST(c.amount * 1000000 as int64)) FROM UNNEST(credits) c), 0))) / 1000000 AS total_exact FROM `<ID_PROJECT>.<DATASET>.gcp_billing_export_v1_<BILLING_ACCOUNT_ID>` GROUP BY 1, 2 ORDER BY 1 ASC, 2 ASC;'
   query_job = client.query(query_string)
   results = query_job.result()

   for row in results:
      values = row.total
      
   actual_bill = values

   if actual_bill < low_cost:
      emoji = ":money_mouth_face: Billing ta sussa!"
   elif actual_bill > high_cost:
      emoji = ":scream: ATENÇÃO @here o billing está muito alto :redsiren: \n"
   else:
      emoji = ":zany_face: ATENÇÃO @here o billing está em um nível preocupante :warning: \n"


   text = "%s ```Billing atual está em: US$ %5.2f```" % (emoji,actual_bill)

   json={
                "text": text + "",
            }

   response = requests.post('WEBHOOKSLACK', json=json)

   return str(text)
