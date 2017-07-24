'''
###
#	Quick and dirty script to create a proposal for sales department
#	Uses Pipedrive's RESTful API to retrieve needed information
###
'''

from bs4 import BeautifulSoup
import requests
import datetime
import sys
import resourceshash

BASE_URL_PERSON = resourceshash.converted("1b61e43abeb45b6c46cb8a4e5f1a5591525018eea768842b16ae5bf65ea87bc1")
PERSON_ID = sys.argv[1]
API_TOKEN = resourceshash.converted("f01bd2bec244960584f67d8da539c8fa1e35ef480b57e249e457bbc68e44e236")
PROPOSAL_TEXT = "Proposal - Quote # "

if __name__ == "__main__":
	full_request = "{0}{1}{2}".format(BASE_URL_PERSON, PERSON_ID, API_TOKEN)
	print(full_request)
	r = requests.get(full_request)
	json_data = r.json()
		
	'''
	Company info
	'''
	account_name = json_data['data']['org_id']['name']
	contact_name = json_data['data']['name']
	address = json_data['data']['1615152572fcd9695cd75b0e1dfd7dd4f35972c0']
	phone_number = json_data['data']['phone'][0]['value']
	email_address = json_data['data']['email'][0]['value']
	
	bank_setup_fee = json_data['data']['747c8a9038f27c116877842b5db703f82c17e282']
	ach_fee = json_data['data']['df64ab5fb7f0b55e8597caa7a44ebf288e8e922a']
	logo_fee = json_data['data']['b3ff2f2d97ad17988b27eace46ec5c11a6d85b56']
	website_fee = json_data['data']['40dd6bcccb5f6311a97506ad52e297b76d70aea4']
	
	PD_owner = json_data['data']['owner_id']['name']
	
	'''
	print(account_name)
	print(contact_name)
	print(phone_number)
	print(email_address)
	print(address)
	print(bank_setup_fee)
	print(logo_fee)
	print(website_fee)
	print(PD_owner)
	'''
	
	today = datetime.date.today()
	today = today.strftime("%m/%d/%y")
	proposal_number = 0
	
	with open("number.txt", "r") as original_number:
		for line in original_number:
			proposal_number = line
	
	with open("number.txt", "w") as new_number:
		new_number.write(str(int(proposal_number) + 1))
	
	new_file = open("newproposal.html", "a+")
	soup2 = BeautifulSoup(new_file, 'html.parser')
	
	proposal_num = soup2.find(id="proposalid")
	proposal_num.append(PROPOSAL_TEXT + str(proposal_number))
	
	create_date = soup2.find(id="createdate")
	create_date.append(today)
	
	if PD_owner is not None:
		prepared_by = soup2.find(id="preparedby")
		prepared_by.append(PD_owner)
	
	if account_name is not None:
		acct_name = soup2.find(id="accountname")
		acct_name.append(account_name)
	
	if address is not None:
		addr = soup2.find(id="address")
		addr.append(address)
	
	if contact_name is not None:
		contact_person = soup2.find(id="contactname")
		contact_person.append(contact_name)
	
	if phone_number is not None:
		phone_num = soup2.find(id="phone")
		phone_num.append(phone_number)
	
	if email_address is not None:
		email_addr = soup2.find(id="email")
		email_addr.append(email_address)
	
	if bank_setup_fee is not None:
		if bank_setup_fee != "":
			bank_fee = soup2.find(id="banksetupfee")
			bank_fee.append("$" + str(bank_setup_fee))
	
	if logo_fee is not None:
		if logo_fee != "":
			logo = soup2.find(id="logofee")
			logo.append("$" + logo_fee)
	
	if website_fee is not None:
		if website_fee != "":
			website_f = soup2.find(id="websitefee")
			website_f.append("$" + website_fee)
	
	with open("newnewproposal.html", "wb") as f_output:
		f_output.write(soup2.prettify("utf-8"))
	
	new_file.close()
