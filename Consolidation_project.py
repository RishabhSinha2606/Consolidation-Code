# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:52:26 2022

@author: Rishabh Sinha
"""


import pandas as pd
import os
import glob
import re

col_list = ['Company name','Established In','Address','Company address','Head Office Address','Headquarters','Corporate Office Address','HO Address','City','Company city','HQ City','State','Company state','Zipcode','Company zipcode','HQ Zip Code','Country','Company country','HQ Country','Region','Branches(Local & Overseas)','Number Of Branches','Company website','Employee Count','SFDC Employee Range','Employee size','Employee Range','Employee Size in the country','Linkedin Employee Count','Employee Count(HQ)','Dell Employee Size','crease','Number of employees','Employee Size','Linkedin Registered Employee','Organisation Size','Industry type','Vertical','Industry','Lenovo Industry Type','Sector','SFDC Industry','Indutry Type - Sub Type','Industry Type - Sub Type','Industry Type - Sub Category','Lenovo Sub Industry','Lenovo Sub Sub Industry','Current Revenue (in Crores)','Company annual revenue (Crore)','Company annual revenue','Company Revenue/Evaluation','Current Revenue(specify Currency)','Revenue (in USD)','Funding Amount (Cr)','Total Funding Amount (in USD)','Number of PC','PC Count in the country','Desktop/ Laptop','No. of PCs DM or Entity is responsible for','Existing Install Base  (No. of PC & Laptops)','Number of IT Users (End Points)','No. of Desktops','Workstation Count','Notebook Count','No. of Laptops','Servers','First name','Last name','Job title','Title','Job Function','SFDC Job Function','Department','Emails','Secondary Email','Generic Email ID','Work','Mobile','Company phone','Parent Account','Parent Company (if any)','Lead stage','Unqualified reason','filename']
listc = ['Company name','Stripped Company name','Established In','A','C','S','Z','Address','Company address','Head Office Address','Headquarters','Corporate Office Address','HO Address','City','Company city','HQ City','State','Company state','Zipcode','Company zipcode','HQ Zip Code','Country','Company country','HQ Country','Region','Branches(Local & Overseas)','Number Of Branches','Company website','Employee Count','SFDC Employee Range','Employee size','Employee Range','Employee Size in the country','Linkedin Employee Count','Employee Count(HQ)','Dell Employee Size','crease','Number of employees','Employee Size','Linkedin Registered Employee','Organisation Size','Industry','I1','I2','I3','I4','I5','SFDC Industry','Sub-Industry','SI1','SI2','SI3','SI4','SI5','Turnover','T1','T2','T3','T4','T5','T6','Funding Amount (Cr)','Total Funding Amount (in USD)','Number of PC','PC Count in the country','Desktop/ Laptop','No. of PCs DM or Entity is responsible for','Existing Install Base  (No. of PC & Laptops)','Number of IT Users (End Points)','No. of Desktops','Workstation Count','Notebook Count','No. of Laptops','Servers','First name','Last name','Contact_Person','Stripped_Contact_Person','Job title','Title','Job Function','SFDC Job Function','Department','Emails','Secondary Email','Generic Email ID','Work','Mobile','Company phone','Parent Account','Parent Company (if any)','Lead stage','Unqualified reason','filename']
listsel = ['Company name','Stripped Company name','Established In','A','C','S','Z','Address','Company address','Head Office Address','Headquarters','Corporate Office Address','HO Address','City','Company city','HQ City','State','Company state','Zipcode','Company zipcode','HQ Zip Code','Country','Company country','HQ Country','Region','Branches(Local & Overseas)','Number Of Branches','Company website','Employee Count','Industry','SFDC Industry','Sub-Industry','Turnover','Funding Amount (Cr)','Total Funding Amount (in USD)','Number of PC','No. of Desktops','Workstation Count','Notebook Count','No. of Laptops','Servers','First name','Last name','Contact_Person','Stripped_Contact_Person','Job title','SFDC Job Function','Department','Emails','Secondary Email','Generic Email ID','Work','Mobile','Company phone','Parent Account','Parent Company (if any)','Lead stage','Unqualified reason','filename'] 
file_path = r'C:\Users\Rishabh Sinha\Documents\Consolidation project\Consolidation_files'
os.chdir(file_path)
listfiles = glob.glob('*')
listdf = []
header_flag = True

for i in listfiles:
    print(i)
    df = pd.read_excel(i)
    req_cols = [i for i in col_list if i in df.columns]
    df = df[req_cols]
    df['filename'] = i.split('.')[0]
    listdf.append(df)
    header_flag = False
df_final = pd.concat(listdf)

##########################################################################

df_final = df_final.reset_index()
df_final = df_final.rename(columns = {'index':'SD_ID'})
#df_final['SD_ID'] = df_final.index+1


df_test = df_final
df_test = df_test.astype(str)


df_test['Company name'] = df_test['Company name'].astype(str).apply(lambda x: re.sub("\(.*?\)","()",x))
df_test = df_test.replace(r'[''"";()?%]','',regex=True)
df_test.fillna('',inplace=True)
for cols in col_list:
    df_test[cols] = df_test[cols].apply(lambda x:x if ((x!='-')&(x!='0')&(x!='/')&(x!=0)&(x!='.')) else '')



df_test= df_test.apply(lambda x:x.astype(str).str.strip())
df_test= df_test.apply(lambda x:x.astype(str).str.lower())


#removing special characters
df_test = df_test.apply(lambda x:x.str.encode('ascii','ignore').str.decode('ascii'))
df_test = df_test.apply(lambda x:x.str.strip())



df_test['First name'] = df_test['First name'].replace(['miss ','mr\. ','ms\. ','dr\. ','mrs\. ','prof\. '],'', regex=True)
df_test['First name'] = df_test['First name'].replace(['miss','mr\.','ms\.','dr\.','mrs\.','prof\.'],'', regex=True)

df_test['Last name'] = df_test['Last name'].replace(['miss ','mr\. ','ms\. ','dr\. ','mrs\. ','prof\. '],'', regex=True)
df_test['Last name'] = df_test['Last name'].replace(['miss','mr\.','ms\.','dr\.','mrs\.','prof\.'],'', regex=True)

df_test['First name'] = df_test['First name'].str.strip()
df_test['Last name'] = df_test['Last name'].str.strip()


df_test['Contact_Person'] = df_test['First name'].astype(str) +" "+ df_test['Last name'].astype(str)
df_test['Contact_Person'] = df_test['Contact_Person'].str.strip()
df_test['Stripped_Contact_Person'] = df_test['Contact_Person'].apply(lambda x:"".join(w for w in x.split()))

stop_words = ['private','public','limited','corporation','group','pvt.','pvt','ltd.','ltd','corp.','corp','plc.','plc','pte.','pte']

df_test['Stripped Company name']= df_test['Company name'].apply(lambda x:"".join(w for w in x.split() if not w in stop_words))

df_test['Stripped Company name'] = df_test['Stripped Company name'].replace(['private','public','limited','corporation','group'],"",regex=True)

df_test['Stripped Company name'] = df_test['Stripped Company name'].replace(['pvt\.','ltd\.','corp\.','plc\.','pte\.'],"",regex=True)

df_test['Stripped Company name'] = df_test['Stripped Company name'].replace(['pvt','ltd','corp','plc','pte'],"",regex=True)












df_test['Employee Count'] = df_test.apply(lambda x:x['Employee Count'] if x['Employee Count']!='' else x['SFDC Employee Range'] if x['SFDC Employee Range']!='' else x['Employee size'] if x['Employee size']!='' else x['Employee Range'] if x['Employee Range']!='' else x['Employee Size in the country'] if x['Employee Size in the country']!='' else x['Linkedin Employee Count'] if x['Linkedin Employee Count']!='' else x['Employee Count(HQ)'] if x['Employee Count(HQ)']!='' else x['Dell Employee Size'] if x['Dell Employee Size']!='' else x['crease'] if x['crease']!='' else x['Number of employees'] if x['Number of employees']!='' else x['Employee Size'] if x['Employee Size']!='' else x['Linkedin Registered Employee'] if x['Linkedin Registered Employee']!='' else x['Organisation Size'],axis=1)

df_test['Job title'] = df_test.apply(lambda x:x['Job title'] if x['Job title']!='' else x['Title'] if x['Title']!='' else 'Job Function', axis=1)

df_test.rename(columns={'Industry type':'I1','Vertical':'I2','Industry':'I3','Lenovo Industry Type':'I4','Sector':'I5'},inplace=True) 

df_test['Industry'] = df_test.apply(lambda x:x['I1'] if x['I1']!='' else x['I2'] if x['I2']!='' else x['I3'] if x['I3']!='' else x['I4'] if x['I4']!='' else x['I5'],axis=1 )

df_test.rename(columns={'Indutry Type - Sub Type':'SI1','Industry Type - Sub Type':'SI2','Industry Type - Sub Category':'SI3','Lenovo Sub Industry':'SI4','Lenovo Sub Sub Industry':'SI5'},inplace=True)

df_test['Sub-Industry'] = df_test.apply(lambda x:x['SI1'] if x['SI1']!='' else x['SI2'] if x['SI2']!='' else x['SI3'] if x['SI3']!='' else x['SI4'] if x['SI4']!='' else x['SI5'],axis=1)

df_test.rename(columns={'Current Revenue (in Crores)':'T1','Company annual revenue (Crore)':'T2','Company annual revenue':'T3','Company Revenue/Evaluation':'T4','Current Revenue(specify Currency)':'T5','Revenue (in USD)':'T6'},inplace=True)

df_test['Turnover'] = df_test.apply(lambda x:x['T1'] if x['T1']!='' else x['T2'] if x['T2']!='' else x['T3'] if x['T3']!='' else x['T4'] if x['T4']!='' else x['T5'] if x['T5']!='' else x['T6'],axis=1)


df_test['Number of PC'] = df_test.apply(lambda x:x['Number of PC'] if x['Number of PC']!='' else x['PC Count in the country'] if x['PC Count in the country']!='' else x['Desktop/ Laptop'] if x['Desktop/ Laptop']!='' else x['No. of PCs DM or Entity is responsible for'] if x['No. of PCs DM or Entity is responsible for']!='' else x['Existing Install Base  (No. of PC & Laptops)'] if x['Existing Install Base  (No. of PC & Laptops)']!='' else x['Number of IT Users (End Points)'],axis=1)


listaddr = []
for(idx1,row1) in df_test.iterrows():
    if(row1['Company address']!=''):
        row1['A'] = row1['Company address']
        row1['C'] = row1['Company city']
        row1['S'] = row1['Company state']
        row1['Z'] = row1['Company zipcode']
    else:
        if(row1['Address']!=''):
            row1['A'] = row1['Address']
            row1['C'] = row1['City']
            row1['S'] = row1['State']
            row1['Z'] = row1['Zipcode']
        else:
            if(row1['Headquarters']!=''):
                row1['A'] = row1['Headquarters']
                row1['C'] = row1['HQ City']
                row1['S'] = ''
                row1['Z'] = row1['HQ Zip Code']
            else:
                if(row1['Head Office Address']!=''):
                    row1['A'] = row1['Head Office Address']
                    row1['C'] = row1['HQ City']
                    row1['S'] = ''
                    row1['Z'] = row1['HQ Zip Code']
                else:
                    if(row1['HO Address']!=''):
                        row1['A'] = row1['HO Address']
                        row1['C'] = row1['HQ City']
                        row1['S'] = ''
                        row1['Z'] = row1['HQ Zip Code']
                    else:
                        if(row1['Corporate Office Address']!=''):
                            row1['A'] = row1['Corporate Office Address']
                            row1['C'] = row1['HQ City']
                            row1['S'] = ''
                            row1['Z'] = row1['HQ Zip Code']
    listaddr.append(row1)                    
df_test = pd.DataFrame(listaddr)
                        
            
#df_test1 = df_test     


df_test['Employee Count1'] = df_test['Employee Count'].astype(str)
df_test['Turnover1'] = df_test['Turnover'].astype(str)
df_test['Number of PC1'] = df_test['Number of PC'].astype(str)
df_test['SFDC Employee Range1'] = df_test['SFDC Employee Range'].astype(str)
df_test['Industry1'] = df_test['Industry'].astype(str)
df_test.sort_values(by=['Employee Count1','SFDC Employee Range1','Turnover1','Number of PC1','A','Company website','Industry1'],inplace=True)












listr = ['Employee Count','Number of PC','Turnover']

for cols in listr:
    temp_df = df_test[df_test[cols]!='']
    
temp_df.drop_duplicates(subset='Stripped Company name',keep='first',inplace=True)

temp_dict = dict(zip(temp_df['Stripped Company name'],temp_df[cols]))

df_cols = df_test['Stripped Company name'].apply(lambda x : temp_dict.get(x,''))



####################################################################

df_test = df_test[listc]
df_test.to_csv(r'C:\Users\Rishabh Sinha\Documents\Consolidation project\splitting\AUG25\TOTALDATA\SELCOLUMNS\SelColumns_TotalData_FreshSales_Consolidated.csv')

df_contact = df_test.drop_duplicates(subset = {'Stripped Company name','Stripped_Contact_Person','Emails','Mobile'}, keep='first')
df_contact.to_csv(r'C:\Users\Rishabh Sinha\Documents\Consolidation project\splitting\AUG25\Final.csv')
df_contact = df_contact[listsel]
##################################################

def chunker(seq,size):
    return(seq[pos:pos + size] for pos in range(0,len(seq),size))








file_dir = 'C:/Users/Rishabh Sinha/Documents/Consolidation project/splitting/AUG25/TOTALDATA/ALLCOLUMNS/'
file_name = file_dir + 'AllColumns_TotalData_Consolidated_File_Chunk_'
counter_suffix = 1

for row in chunker(df_test,round(len(df_test.index)/10)):
    row.to_csv(file_name + str(counter_suffix) + '.csv',index=False)
    counter_suffix+=1
    print(counter_suffix-1)



###########################################################

df_test =df_test[listsel]



##################################################3
def chunker(seq,size):
    return(seq[pos:pos + size] for pos in range(0,len(seq),size))








file_dir = 'C:/Users/Rishabh Sinha/Documents/Consolidation project/splitting/AUG25/TOTALDATA/SELCOLUMNS/'
file_name = file_dir + 'SelColumns_TotalData_Consolidated_File_Chunk_'
counter_suffix = 1

for row in chunker(df_test,round(len(df_test.index)/10)):
    row.to_csv(file_name + str(counter_suffix) + '.csv',index=False)
    counter_suffix+=1
    print(counter_suffix-1)




##############################################################
def chunker(seq,size):
    return(seq[pos:pos + size] for pos in range(0,len(seq),size))








file_dir = 'C:/Users/Rishabh Sinha/Documents/Consolidation project/splitting/AUG25/UNIQUEDATA/ALLCOLUMNS/'
file_name = file_dir + 'AllColumns_UniqueData_Consolidated_File_Chunk_'
counter_suffix = 1

for row in chunker(df_contact,round(len(df_contact.index)/10)):
    row.to_csv(file_name + str(counter_suffix) + '.csv',index=False)
    counter_suffix+=1
    print(counter_suffix-1)
    

###############################################################################

df_contact = df_contact[listsel]
#########################################################################33

def chunker(seq,size):
    return(seq[pos:pos + size] for pos in range(0,len(seq),size))








file_dir = 'C:/Users/Rishabh Sinha/Documents/Consolidation project/splitting/AUG25/'
file_name = file_dir + 'chunk_'
counter_suffix = 1

for row in chunker(df_contact,round(len(df_contact.index)/2)):
    row.to_csv(file_name + str(counter_suffix) + '.csv',index=False)
    counter_suffix+=1
    print(counter_suffix-1)
    










############################################################################
#Sorting contacts

df_it = df_contact[df_contact['Job title'].str.contains('it','information technology','developer','technology','testing','software')]
df_it.to_excel()
df_it_company = df_it.drop_duplicates(subset={'Stripped Company name'})

df_fin = df_contact[df_contact['Job title'].str.contains('financ','')]
df_fin.to_excel()
df_fin_company = df_it.drop_duplicates(subset={'Stripped Company name'})


df_proc = df_contact[df_contact['Job title'].str.contains('purchase','procur')]
df_proc.to_excel()
df_proc_company = df_it.drop_duplicates(subset={'Stripped Company name'})


df_cxo = df_contact[df_contact['Job title'].str.contains('chief','founder','chairman','ceo','cto','cio','cfo',)]





##################################################################
#splitting



#lst_vg =[286756,733941,379398,33812,628578,593944,397466,593532,323302,543497,168631,493203,830085,278728,156667,320509,861061,826626,229318,22035]
lst_vg =['approx500-1000','approx1001-5000','approx 500-1000','approx 500','approx 2500','approx 1500','approx 10000','above 2000','above 10,000','999-1000','900-1000','9000+','9,000+','8300+','800-999','800-950','800-900','8000-10000','800+','750-900','750-1k','750-1200','750-1000','700-900','700-800','700-1000','70000-80000','700+','650-900','650-800','65000-70000','6300+','600-800','600-750','60000+','6000+','600+','600 - 650','5700+','551-1000','550-700','550-1000','550+','510+','501-999','501-700','501-600','501-550','501-500','501-2000','501-200','501-1001','501-10000','501-1000','501-100','501-1,000 employees','501-1,000','501- 1000','501 -1000','501 - 999','501 - 1000','501  - 1000','500-999+','500-999','500-900','500-800','500-750','500-700','500-600','500-550','500-4999','500-499','500-2000','5001-9999','5001-20000','5001-10001','5001-10000','5001-1000','5001-10,000 employee','5001-10,000','500-1001','500-1000','500-100','5001+','500-1,000','5001 - 10000','5001 - 1000','5000-99999','5000-9999','5000-6000','50001-100000','50001-10000','5000-10001+','5000-10001','5000-10000','5000-1000','50000-99999','50000+','5000+','5000 +','5000 - 9999','5000 - 10000','500+1000+','500+','500 to 999','500 -999','500 - 999','500  999','500 - 1000','50,000 to 99,999','5,001-10,000 employees','5,001-10,000','5,000-9,999','5,000-10,000','5,000+','5,000 to 9,999','499-999','499-799','499-500','499-1000','499 - 999','499 - 500','499 - 1000','4500-5000','4500 - 5000','450+','400-800','400-600','4000-5000','4000-4999','4000+','3500-4500','3500-4000','3500+','300-800','300-700','300-600','3001-5000','3000-4999','3000-4000','3000-3999','3000-3500','3000-3250','30000+','3000+','251-5000','251-1000','2510-5000','2501-5000','2501-10000','250-1000','2500-5000','2500-500','2500-4999','25000-49999','25000+','2500+','2500 - 3000','25,000 to 49,999','201-5000','201-1000','200-600','200-5000','2001-5000','2001 - 5000','2000-5000','2000-4999','2000-3000','2000-2999','2000-2500','20000-250000','20000+','20000 or more','2000+','2000- 2500','2000 - 2500','20,000 +','2,000-4,999','19000+','18500+','1800+','1700+','16000+','1501-2500','1500-5000','1500-2000','1500-1999','15000+','1500+','1300-1500','1300+','1100-5000','11.7k','10k - 50k','101-999','101-1000','100-999','100-800','100-600','100-599','100-5000','100-2000','1001-5001','1001-5000','1001-500','1001-5,000','1001-4999','1001-4000','1001-2999','1001-2501','1001-2500','1001-2001','1001-2000','1001-1500','1001-10000','100-1000','1001+','1001 to 5000','1001 to 2000 people','1001 to 2000','1001 - 5000','1001 - 4999','1001 - 2000','1000-9999','1000-8999','1000-5001','1000-5000','1000-4999+','1000-4999','1000-4900','1000-2500','1000-2499','1000-2000','10001-above','1000-1999+','1000-1999','10001-5000','1000-1500','1000-1499','10001-25000','10001-20000','10001-2000','1000-1200','10001+','10000-and above','10000-above','10000-49999','10000-24999','10000-20000','10000-19999','10000-19000','10000-15000','10000-120000','10000-11999','100000+','10000<','10000+','10000- and above','10000 above','10000  above','10000 - 10500','1000+','1000- 4999+','1000 -4999','1000- 1999+','1000 - 5000','1000 - 4999','1000 - 1500','100,000+','10,001-20000','10,001-15000','10,001+ employees','10,001+','10,001 +','10,000-19,999','10,000-19,000','10,000+','10,000 to 24,999','10,000 +','10,000 - 19,999','10 - 100','1,001-5,000 employees','1,001-5,000','1,001-4,999','1,000-5,000','1,000-1,999','1,000 to 4,999','1,000 - 4,999','0-10000','0-1000','>5000','>20000','>100000','>10000','500110000','445000000','429000000','150000000','1308000','750000','417929','396859','380000','377000','350000','291000','285000','272445','249448','244400','243000','225000','209567','200000','180000','177500','173863','172258','162302','160000','153000','150000','145000','144400','140000','137965','133000','120000','117693','114628','111200','111092','111000','110009','110000','105000','103000','100001','100000','96000','95000','93116','90335','90000','88213','84922','84282','84027','81233','78906','78300','77000','76752','75000','74096','73000','72973','72222','70810','70000','69824','68742','66926','65807','64000','63000','60592','60000','59000','57000','56767','56700','55132','55000','51000','50500','50000','49000','48353','47000','46000','45962','45931','45658','45000','44836','44835','44805','44510','44501','44474','44471','44470','44440','44432','44379','44332','44317','44136','44105','43831','43000','42875','42278','42005','42000','41620','40401','40000','39821','39222','39000','38886','38000','36434','36161','36000','35637','35000','34989','34738','34000','33797','33614','33498','33013','33000','32999','32874','32448','32364','32115','32000','31708','31514','31500','31437','31000','30674','30500','30001','30000','29696','29495','29221','29000','28345','28291','28000','27700','27668','27600','27174','27000','26969','26383','26354','26147','26000','25959','25927','25620','25284','25191','25000','24123','24000','23531','23131','23000','22795','22500','22383','22239','22036','22000','21991','21847','21650','21565','21349','21100','21000','20981','20680','20394','20373','20257','20222','20154','20001','20000','19918','19868','19834','19533','19470','19400','19000','18933','18902','18759','18629','18568','18537','18522','18302','18264','18130','18000','17574','17500','17464','17375','17179','17000','16962','16500','16400','16000','15945','15819','15500','15216','15000','14630','14600','14500','14467','14200','14000','13850','13655','13520','13511','13500','13474','13434','13405','13101','13077','13000','12900','12881','12800','12740','12734','12675','12599','12568','12500','12496','12378','12157','12107','12000','11888','11886','11747','11526','11500','11495','11471','11263','11232','11000','10990','10959','10881','10789','10700','10682','10652','10533','10510','10500','10352','10200','10001','10000','9993','9931','9805','9777','9700','9615','9612','9500','9440','9330','9312','9255','9200','9148','9120','9008','9001','9000','8918','8900','8818','8800','8790','8700','8656','8613','8599','8569','8500','8300','8234','8200','8159','8032','8003','8000','7962','7900','7885','7874','7839','7800','7723','7700','7669','7610','7600','7560','7521','7500','7435','7406','7400','7221','7200','7116','7098','7097','7000','6900','6800','6753','6742','6700','6680','6675','6643','6600','6546','6500','6496','6450','6439','6400','6378','6374','6360','6310','6300','6285','6284','6223','6220','6200','6195','6185','6180','6175','6153','6151','6149','6100','6085','6034','6000','5973','5911','5900','5895','5887','5832','5822','5814','5808','5801','5800','5700','5692','5690','5600','5575','5538','5500','5494','5460','5439','5410','5405','5400','5385','5351','5300','5236','5200','5133','5100','5001','5000','4985','4952','4946','4900','4899','4868','4852','4800','4702','4700','4698','4695','4688','4684','4680','4666','4638','4629','4625','4615','4602','4600','4589','4584','4535','4529','4512','4510','4500','4495','4490','4480','4471','4441','4411','4400','4354','4322','4314','4300','4280','4267','4259','4258','4256','4233','4200','4174','4130','4111','4103','4100','4062','4054','4043','4028','4005','4002','4000','3991','3956','3945','3941','3901','3900','3899','3898','3895','3880','3875','3818','3800','3790','3773','3768','3763','3754','3750','3712','3710','3703','3700','3684','3655','3603','3601','3600','3587','3568','3551','3550','3546','3531','3518','3509','3500','3477','3475','3449','3448','3430','3410','3400','3382','3364','3351','3333','3321','3311','3309','3304','3302','3300','3297','3236','3230','3216','3204','3200','3184','3171','3162','3156','3150','3133','3101','3100','3097','3062','3050','3042','3029','3027','3010','3000','2998','2978','2975','2972','2949','2944','2910','2903','2900','2880','2851','2849','2840','2827','2818','2817','2806','2802','2800','2789','2786','2784','2768','2766','2700','2698','2690','2659','2655','2650','2649','2642','2625','2600','2598','2597','2596','2592','2587','2580','2569','2567','2564','2553','2550','2547','2508','2500','2485','2482','2459','2440','2439','2420','2410','2404','2400','2394','2388','2377','2372','2370','2358','2351','2350','2344','2343','2333','2322','2321','2320','2315','2302','2300','2276','2260','2255','2250','2245','2241','2217','2200','2196','2183','2166','2146','2134','2103','2100','2090','2083','2078','2058','2050','2036','2013','2002','2001','2000','1987','1983','1964','1957','1955','1947','1945','1942','1936','1934','1932','1927','1915','1900','1899','1894','1891','1877','1870','1869','1863','1856','1850','1847','1839','1831','1828','1826','1825','1812','1800','1796','1788','1787','1779','1762','1759','1758','1750','1749','1744','1742','1738','1733','1726','1720','1704','1700','1693','1687','1684','1672','1662','1661','1652','1651','1648','1635','1631','1627','1625','1624','1617','1613','1611','1608','1600','1599','1598','1596','1595','1580','1576','1569','1566','1564','1562','1551','1547','1534','1533','1529','1500','1496','1491','1485','1484','1473','1472','1470','1465','1458','1452','1436','1432','1430','1425','1400','1399','1397','1390','1389','1388','1382','1377','1356','1352','1350','1349','1343','1340','1335','1332','1322','1320','1307','1300','1298','1297','1290','1289','1284','1281','1280','1275','1266','1261','1259','1256','1254','1252','1250','1245','1242','1237','1236','1227','1224','1222','1220','1216','1208','1207','1203','1200','1197','1195','1192','1178','1165','1163','1159','1155','1150','1144','1140','1135','1124','1121','1120','1110','1107','1100','1095','1089','1080','1074','1072','1065','1062','1060','1057','1056','1055','1048','1042','1040','1021','1020','1013','1001','1000','998','994','987','986','985','984','983','982','980','975','970','966','965','964','959','958','950','945','944','936','935','933','932','930','927','923','915','913','910','909','905','904','901','900','898','897','895','893','892','887','884','883','882','880','879','878','877','876','872','870','869','867','865','862','861','859','857','856','854','852','850','848','847','845','841','840','839','836','835','834','833','832','830','829','827','825','824','821','820','815','814','810','809','807','803','800','799','798','793','792','791','787','780','778','777','775','771','766','764','762','760','759','758','756','755','754','752','751','750','747','745','743','742','741','740','735','734','733','732','730','729','726','725','723','720','718','713','712','710','708','705','704','703','700','699','698','696','692','691','690','689','684','681','679','678','676','675','673','670','669','667','666','664','663','660','659','658','657','656','655','653','650','647','645','643','642','640','636','635','630','628','626','625','623','622','621','620','619','618','617','616','613','612','611','610','608','607','600','599','598','596','594','592','591','590','589','588','587','585','584','583','581','580','579','577','574','573','572','571','570','569','568','567','566','565','562','560','557','556','554','553','552','550','548','546','545','544','543','542','541','540','539','537','536','532','531','530','529','528','526','525','524','523','522','521','520','519','517','515','513','512','511','510','509','508','504','502','501']
df_contact = df_contact.reset_index()
df_contact = df_contact.rename(columns = {'index':'SD_ID'})
df_contact['SD_ID'] = df_contact.index+1


df_contact1 = df_contact[df_contact['Employee Count'].isin(lst_vg)]

df_contact.replace('nan','',inplace=True)

df_contact= df_contact.apply(lambda x:x.astype(str))

for cols in listsel:
    df_contact[cols] = df_contact[cols].apply(lambda x:"" if str(x)=='0' else x)
    
    
df_contact['Employee Count'] = df_contact['Employee Count'].astype(int)
df_emp = df_contact.drop_duplicates(subset='Employee Count').astype(str)
df_emp = df_emp[['Employee Count']].astype(str)
df_emp.to_csv('C:/Users/Rishabh Sinha/Documents/Consolidation project/test_consolidation/employeesize500plus.csv')





df_contact1 = df_contact[df_contact['Employee Count'].isin(lst_vg)]

df_contact1.to_csv(r'C:\Users\Rishabh Sinha\Documents\Consolidation project\splitting\AUG25\500PLUSCONTACTS.csv')












