from xlrd import open_workbook,cellname
from xlwt import Workbook

mapping = {'Sl. No.':'id','Name of work':'name','WBPMS Project Code':'project_code','Requisition detail':'requisition','PE detail ':'pe_det','PE Amount (Rs.)':'pe_amt', 'Send to':'pe_sent_to','Final Send to Client':'fe_sent_to_client','Client':'client','A/A & E/S detail':'aa_es_detail','Head of Account':'head_acc','Amount (Rs.)':'final_amt', 'T/S Authority':'ts_auth','No of Packages/ Subwork':'no_sub', 'T/S Date':'ts_date', 'T/S Amount':'ts_amt', 'Time Allowed':'time_allowd', 'NIT detail':'nit', 'Date':'nit_date', 'Amount':'nit_amt', 'Agency':'agency', 'Address':'agency_add', 'Agmt. No.':'agent_no', 'Tendered Amount':'tender_amt', 'Date of Start':'date_start', 'Stipulated Date of com.':'stipulated_date', 'Actual Date of Completion':'actual_date', 'Work Status':'status', 'Expenditure':'expense', 'Remarks':'remarks' }

def generate_mapping():
    generated_mapping = {}
    format_book = open_workbook('media/format.xls')
    format_sheet = format_book.sheet_by_index(0)
    i=0
    for col_index in range(format_sheet.ncols):
        try:
            generated_mapping[mapping[format_sheet.cell(0,col_index).value]]=col_index
        except KeyError:
            print 'No such key'
    #print len(generated_mapping), len(mapping)
    return generated_mapping
