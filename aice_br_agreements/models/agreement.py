# -*- coding: utf-8 -*-
from odoo import api, fields, models, http, _
import io
import base64
import requests, json
from odoo.http import request, content_disposition, Controller
from odoo.exceptions import ValidationError

# Class for the actual conponnent
class AgreeList(models.Model):
    _name = "a_agreement.list"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Agreement list system"
    #defining a sequence number for the name.
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Agreement'
            vals['state'] = 'sent'
        if vals.get('name', _('New Agreement')) == _('New Agreement'):
            vals['name'] = self.env['ir.sequence'].next_by_code('a_agreement.list') or _('New Agreement')
            vals['state'] = 'sent'
        res = super(AgreeList, self).create(vals)
        return res

    # Going to the next item in the sequence
    def toDraft(self):
        self.state = 'draft'

    def toSent(self):
        self.state = 'sent'

    # Name of the operation.
    name = fields.Char(string='Agreement Number', required=True, copy=False, readonly=True, default=lambda self: _('New Agreement'))
    
    # Gets the actual datte time from the server.
    date_creation = fields.Datetime(string='Cheated On ', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    
    # Observations
    note = fields.Text(string='Description')
    doc_name = fields.Char(string='Document Name', required=True)
    doc_reference = fields.Char(string='Document Ref', required=True)
    user_id = fields.Many2one('res.users', string='Responsible', index=True, tracking=2, required=True, default=lambda self: self.env.user)
    
    # Array of status names.
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Saved'),
        ('done', 'Document Sent'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # Archive / Unarchive
    active = fields.Boolean(string='Active', default=True, tracking=True)
    # PDF File field
    pdf_file = fields.Binary(string='PDF File')

    def download_pdf(self):
        file_data = self.pdf_file
        print(file_data)
        if file_data:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/?model=a_agreement.list&id=%s&field=pdf_file&download=true&filename=%s.pdf' % (self.id, self.doc_name),
                'target': 'self',
            }
        else:
            return False

    def request_download_agreement(self):
        self.request_auth_return_user_and_download()
            #dde
        #else:
            #return False
        
    # API Auth credentials
    assertion = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3ZGUwNGU4Yy1hODJlLTQzOTUtYWMzYi1iZmFjMTY0YjAxMjkiLCJzdWIiOiJiYzA5YWI0My1hM2YwLTQ2NjItOTQ1ZS1jNzE0MWU0ZmM2MGMiLCJhdWQiOiJhY2NvdW50LWQuZG9jdXNpZ24uY29tIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE4MTYyMzkwMjIsInNjb3BlIjoic2lnbmF0dXJlIGltcGVyc29uYXRpb24ifQ.Ncr7I6CQ8f19-pkDNwpFuJ07qgOpJHZx6FGaXr2aVrXTezaP3YC30pHOsYMewKIwQoOCAWQoIBPV258sN-we12MRHpaQGzSncSzNerP6_3_ryv2PBrbt0ILJnDW-mW8lKwMzvRc93_emNabeCrUqmWBKzSaCZRTvtUViYV0vRHkakwWnnZVf0TOxipe8Cl_NYZyjiXH7ulTjnsKtAsAGOWkrw7r_S958pyV7vr7vsnYSjpTrcSjWkQBmIR3JdN326rfobqFzvTQr2Kb2CFcC-1FDnaWYj2DP0abPm64A4oakw6jpd-JS9geB49Y8RIiXkW5vGplh6hOwBYTFlJG7-g'
    grant_type = 'urn:ietf:params:oauth:grant-type:jwt-bearer'

    # API PART ----------------------------------------------------------------------------------------------------------
    def request_auth_return_user_and_done_agreements(self):
        url = 'http://localhost:3000/restapi/v1/retrieveAPIKey'
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}
        json_data = {'assertion': self.assertion , 'grant_type': self.grant_type}

        response = requests.post(url, data=json.dumps(json_data), headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Calls the API action with the new key generated. 
            self.request_return_user_info(data.get('access_token'))
        else:
            pass

    # AUTH for downloading agreement 
    def request_auth_return_user_and_download(self):
        url = 'http://localhost:3000/restapi/v1/retrieveAPIKey'
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}
        json_data = {'assertion': self.assertion , 'grant_type': self.grant_type}

        response = requests.post(url, data=json.dumps(json_data), headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Calls the API action with the new key generated. 
            self.request_return_user_info_download(data.get('access_token'))
        else:
            pass
    
    # Return user information to complete agreements
    def request_return_user_info(self, key):
        url_user = 'http://localhost:3000/restapi/v1/retrieveUserInfo'
        headers_user = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}
        json_data_user = {'access_prefix': 'Bearer' , 'access_token': key}

        response_user = requests.post(url_user, data=json.dumps(json_data_user), headers=headers_user)
        if response_user.status_code == 200:
            data_from_user = response_user.json()
            accounts = data_from_user.get('accounts')

            # Calls the API action with the new key generated and user id
            self.request_return_completed_agreements(key, accounts[0].get('account_id'))
        else:
            pass
    
    # Return user information to download agreement
    def request_return_user_info_download(self, key):
        url_user = 'http://localhost:3000/restapi/v1/retrieveUserInfo'
        headers_user = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}
        json_data_user = {'access_prefix': 'Bearer' , 'access_token': key}

        response_user = requests.post(url_user, data=json.dumps(json_data_user), headers=headers_user)
        if response_user.status_code == 200:
            data_from_user = response_user.json()
            accounts = data_from_user.get('accounts')

            # Calls the API action with the new key generated and user id
            self.request_return_download_agreement(key, accounts[0].get('account_id'), self.doc_reference)
        else:
            pass
    
    # Downloads the agreement
    def request_return_download_agreement(self, key, user, env_id):
        url_download = 'http://localhost:3000/restapi/v1/downloadEnvelope'
        headers_download = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}
        json_data_download = {'access_prefix': 'Bearer' , 'access_token': key, 'user_id': user, 'env_id': env_id}

        response_download = requests.post(url_download, data=json.dumps(json_data_download), headers=headers_download)
        if response_download.status_code == 200:
            file_data = response_download.content
            self.pdf_file = base64.b64encode(file_data)
            pass
        else:
            pass

    # Returns all completed agreements
    def request_return_completed_agreements(self, key, user):
        url_agreements = 'http://localhost:3000/restapi/v1/showEnvelopes'
        headers_agreements = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}
        json_data_agreements = {'access_prefix': 'Bearer' , 'access_token': key, 'user_id': user}

        response_agreements = requests.post(url_agreements, data=json.dumps(json_data_agreements), headers=headers_agreements)
        if response_agreements.status_code == 200:
            data_agreements = response_agreements.json()
            print(data_agreements)

            # List of envelopes 
            envelopes = data_agreements.get('envelopes')

            for env in envelopes:
                record = self.search([('doc_name', '=', env['emailSubject'])])
                if record:
                    # Update it if the record already has inside the db
                    record.write({
                        'doc_name': env['emailSubject'],
                        'doc_reference': env['envelopeId']
                    })
                else:
                    # Creates one if its not
                    self.create({
                        'doc_name': env['emailSubject'],
                        'doc_reference': env['envelopeId']
                    })

                # Putting the download link inside the binary feld of each data
                url_download = 'http://localhost:3000/restapi/v1/downloadEnvelope'
                headers_download = {"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}
                json_data_download = {'access_prefix': 'Bearer' , 'access_token': key, 'user_id': user, 'env_id': env['envelopeId']}

                response_download = requests.post(url_download, data=json.dumps(json_data_download), headers=headers_download)
                if response_download.status_code == 200:
                    file_data = response_download.content
                    self.pdf_file = base64.b64encode(file_data)
                else:
                    pass
        else:
            pass
    
    
    