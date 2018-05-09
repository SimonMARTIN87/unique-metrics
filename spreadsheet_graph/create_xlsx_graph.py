from produce_xlsx import create_xlsx
from viz import create_graph
import logging

# company = raw_input("Enter a company (Macdo, Jamba, Halal):")
# date_debut = raw_input("Enter date of begining ('dd/mm/aaaa'):")
# date_fin = raw_input("Enter date of end ('dd/mm/aaaa'):")

company = 'Macdo'
date_debut = '01/01/2018'
date_fin = '20/03/2018'

logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
logging.info('STARTED');

# create_xlsx(date_debut, date_fin, company)
logging.info('XLSX CREATED');

date_debut_ = date_debut.replace('/','-')
date_fin_ = date_fin.replace('/','-')
logging.info('starting plotly');
create_graph(str(company)+'_'+str(date_debut_)+'_'+str(date_fin_)+'.xlsx', company, date_debut, date_fin)