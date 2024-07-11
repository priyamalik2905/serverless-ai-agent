from flask import Flask
from flask_login import current_user
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from typing import Optional, List, Any
import os
import json
import mimetypes
from dotenv import load_dotenv


load_dotenv()


class FlaskAssistants:
    def __init__(self, app=None, system_admin_model=None, admin_model=None, admin_team_model=None, admin_team_user_model=None,
                customer_model=None, customer_team_model=None, customer_team_user_model=None,
                affiliate_model=None, affiliate_team_model=None, affiliate_team_user_model=None,
                end_user_model=None, end_user_passport_model=None, solution_model=None, system_assistant_model=None,
                admin_assistant_model=None, customer_assistant_model=None,
                affiliate_assistant_model=None, end_user_assistant_model=None,
                system_vector_store_model=None, admin_vector_store_model=None, customer_vector_store_model=None, 
                affiliate_vector_store_model=None, end_user_vector_store_model=None,
                system_thread_model=None, admin_thread_model=None, customer_thread_model=None, 
                affiliate_thread_model=None, end_user_thread_model=None, 
                system_run_model=None, admin_run_model=None, customer_run_model=None,
                affiliate_run_model=None, end_user_run_model=None,
                system_assistants_vector_stores_model=None, admin_assistants_vector_stores_model = None, customer_assistants_vector_stores_model = None, affiliate_assistants_vector_stores_model = None, end_user_assistants_vector_stores_model = None,
                system_assistants_system_admins_threads_model=None, system_assistants_system_admins_runs_model=None, system_assistants_system_admins_permissions_model=None, 
                admin_assistants_system_admins_threads_model = None, admin_assistants_system_admins_runs_model = None, admin_assistants_system_admins_permissions_model = None,
                customer_assistants_system_admins_threads_model = None, customer_assistants_system_admins_runs_model = None, customer_assistants_system_admins_permissions_model = None,
                affiliate_assistants_system_admins_threads_model = None, affiliate_assistants_system_admins_runs_model = None, affiliate_assistants_system_admins_permissions_model = None,
                end_user_assistants_system_admins_threads_model = None, end_user_assistants_system_admins_runs_model = None, end_user_assistants_system_admins_permissions_model = None,
                admin_assistants_admins_threads_model = None, admin_assistants_admins_runs_model = None, admin_assistants_admins_permissions_model = None,
                customer_assistants_admins_threads_model = None, customer_assistants_admins_runs_model = None, customer_assistants_admins_permissions_model = None,
                affiliate_assistants_admins_threads_model = None, affiliate_assistants_admins_runs_model = None, affiliate_assistants_admins_permissions_model = None,
                end_user_assistants_admins_threads_model = None, end_user_assistants_admins_runs_model = None, end_user_assistants_admins_permissions_model = None,
                customer_assistants_customers_threads_model = None, customer_assistants_customers_runs_model = None, customer_assistants_customers_permissions_model = None,
                affiliate_assistants_customers_threads_model = None, affiliate_assistants_customers_runs_model = None, affiliate_assistants_customers_permissions_model = None,
                end_user_assistants_customers_threads_model = None, end_user_assistants_customers_runs_model = None, end_user_assistants_customers_permissions_model = None,
                affiliate_assistants_affiliates_threads_model = None, affiliate_assistants_affiliates_runs_model = None, affiliate_assistants_affiliates_permissions_model = None,
                end_user_assistants_affiliates_threads_model = None, end_user_assistants_affiliates_runs_model = None, end_user_assistants_affiliates_permissions_model = None,
                end_user_assistants_end_users_threads_model = None, end_user_assistants_end_users_runs_model = None,
                system_file_model=None, admin_file_model=None, customer_file_model=None, affiliate_file_model=None, end_user_file_model=None,
                system_team_file_model=None, admin_team_file_model=None, customer_team_file_model=None, affiliate_team_file_model=None,
                system_files_vector_stores_model=None, admin_files_vector_stores_model=None, customer_files_vector_stores_model=None, affiliate_files_vector_stores_model=None,
                system_team_files_vector_stores_model=None, admin_team_files_vector_stores_model=None, customer_team_files_vector_stores_model=None, affiliate_team_files_vector_stores_model=None):
        
        self.system_admin_model = system_admin_model
        self.admin_model = admin_model
        self.admin_team_model = admin_team_model
        self.admin_team_user_model=admin_team_user_model
        self.customer_model = customer_model
        self.customer_team_model = customer_team_model
        self.customer_team_user_model = customer_team_user_model
        self.affiliate_model = affiliate_model
        self.affiliate_team_model = affiliate_team_model
        self.affiliate_team_user_model = affiliate_team_user_model
        self.end_user_model = end_user_model
        self.end_user_passport_model = end_user_passport_model
        self.solution_model = solution_model
        self.system_assistant_model = system_assistant_model
        self.admin_assistant_model = admin_assistant_model
        self.customer_assistant_model = customer_assistant_model
        self.affiliate_assistant_model = affiliate_assistant_model
        self.end_user_assistant_model = end_user_assistant_model
        self.system_vector_store_model = system_vector_store_model
        self.admin_vector_store_model = admin_vector_store_model
        self.customer_vector_store_model = customer_vector_store_model
        self.affiliate_vector_store_model = affiliate_vector_store_model
        self.end_user_vector_store_model = end_user_vector_store_model
        self.system_thread_model = system_thread_model
        self.admin_thread_model = admin_thread_model
        self.customer_thread_model = customer_thread_model
        self.affiliate_thread_model = affiliate_thread_model
        self.end_user_thread_model = end_user_thread_model
        self.system_run_model = system_run_model
        self.admin_run_model = admin_run_model
        self.customer_run_model = customer_run_model
        self.affiliate_run_model = affiliate_run_model
        self.end_user_run_model = end_user_run_model
        self.system_assistants_vector_stores_model = system_assistants_vector_stores_model
        self.admin_assistants_vector_stores_model = admin_assistants_vector_stores_model
        self.customer_assistants_vector_stores_model = customer_assistants_vector_stores_model
        self.affiliate_assistants_vector_stores_model = affiliate_assistants_vector_stores_model
        self.end_user_assistants_vector_stores_model = end_user_assistants_vector_stores_model
        self.system_assistants_system_admins_threads_model = system_assistants_system_admins_threads_model
        self.system_assistants_system_admins_runs_model = system_assistants_system_admins_runs_model
        self.system_assistants_system_admins_permissions_model = system_assistants_system_admins_permissions_model
        self.admin_assistants_system_admins_threads_model = admin_assistants_system_admins_threads_model
        self.admin_assistants_system_admins_runs_model = admin_assistants_system_admins_runs_model
        self.admin_assistants_system_admins_permissions_model = admin_assistants_system_admins_permissions_model
        self.customer_assistants_system_admins_threads_model = customer_assistants_system_admins_threads_model
        self.customer_assistants_system_admins_runs_model = customer_assistants_system_admins_runs_model
        self.customer_assistants_system_admins_permissions_model = customer_assistants_system_admins_permissions_model
        self.affiliate_assistants_system_admins_threads_model = affiliate_assistants_system_admins_threads_model
        self.affiliate_assistants_system_admins_runs_model = affiliate_assistants_system_admins_runs_model
        self.affiliate_assistants_system_admins_permissions_model = affiliate_assistants_system_admins_permissions_model
        self.end_user_assistants_system_admins_threads_model = end_user_assistants_system_admins_threads_model
        self.end_user_assistants_system_admins_runs_model = end_user_assistants_system_admins_runs_model
        self.end_user_assistants_system_admins_permissions_model = end_user_assistants_system_admins_permissions_model
        self.admin_assistants_admins_threads_model = admin_assistants_admins_threads_model
        self.admin_assistants_admins_runs_model = admin_assistants_admins_runs_model
        self.admin_assistants_admins_permissions_model = admin_assistants_admins_permissions_model
        self.customer_assistants_admins_threads_model = customer_assistants_admins_threads_model
        self.customer_assistants_admins_runs_model = customer_assistants_admins_runs_model
        self.customer_assistants_admins_permissions_model = customer_assistants_admins_permissions_model
        self.affiliate_assistants_admins_threads_model = affiliate_assistants_admins_threads_model
        self.affiliate_assistants_admins_runs_model = affiliate_assistants_admins_runs_model
        self.affiliate_assistants_admins_permissions_model = affiliate_assistants_admins_permissions_model
        self.end_user_assistants_admins_threads_model = end_user_assistants_admins_threads_model
        self.end_user_assistants_admins_runs_model = end_user_assistants_admins_runs_model
        self.end_user_assistants_admins_permissions_model = end_user_assistants_admins_permissions_model
        self.customer_assistants_customers_threads_model = customer_assistants_customers_threads_model
        self.customer_assistants_customers_runs_model = customer_assistants_customers_runs_model
        self.customer_assistants_customers_permissions_model = customer_assistants_customers_permissions_model
        self.affiliate_assistants_customers_threads_model = affiliate_assistants_customers_threads_model
        self.affiliate_assistants_customers_runs_model = affiliate_assistants_customers_runs_model
        self.affiliate_assistants_customers_permissions_model = affiliate_assistants_customers_permissions_model
        self.end_user_assistants_customers_threads_model = end_user_assistants_customers_threads_model
        self.end_user_assistants_customers_runs_model = end_user_assistants_customers_runs_model
        self.end_user_assistants_customers_permissions_model = end_user_assistants_customers_permissions_model
        self.affiliate_assistants_affiliates_threads_model = affiliate_assistants_affiliates_threads_model
        self.affiliate_assistants_affiliates_runs_model = affiliate_assistants_affiliates_runs_model
        self.affiliate_assistants_affiliates_permissions_model = affiliate_assistants_affiliates_permissions_model
        self.end_user_assistants_affiliates_threads_model = end_user_assistants_affiliates_threads_model
        self.end_user_assistants_affiliates_runs_model = end_user_assistants_affiliates_runs_model
        self.end_user_assistants_affiliates_permissions_model = end_user_assistants_affiliates_permissions_model
        self.end_user_assistants_end_users_threads_model = end_user_assistants_end_users_threads_model
        self.end_user_assistants_end_users_runs_model = end_user_assistants_end_users_runs_model
        self.system_file_model = system_file_model
        self.admin_file_model = admin_file_model
        self.customer_file_model = customer_file_model
        self.affiliate_file_model = affiliate_file_model
        self.end_user_file_model = end_user_file_model
        self.system_team_file_model = system_team_file_model
        self.admin_team_file_model = admin_team_file_model
        self.customer_team_file_model = customer_team_file_model
        self.affiliate_team_file_model = affiliate_team_file_model
        self.system_files_vector_stores_model = system_files_vector_stores_model
        self.admin_files_vector_stores_model = admin_files_vector_stores_model
        self.customer_files_vector_stores_model = customer_files_vector_stores_model
        self.affiliate_files_vector_stores_model = affiliate_files_vector_stores_model
        self.system_team_files_vector_stores_model = system_team_files_vector_stores_model
        self.admin_team_files_vector_stores_model = admin_team_files_vector_stores_model
        self.customer_team_files_vector_stores_model = customer_team_files_vector_stores_model
        self.affiliate_team_files_vector_stores_model = affiliate_team_files_vector_stores_model

        self.client = OpenAI()
        if app is not None:
            self.init_app(app)


    def init_app(self, app: Flask):
        """In __init__.py of the actual flask application, 
        flask-sqlalchemy models will be passed to the extension like this:
        app.config['USER_MODEL'] = User
        app.config['TRANSACTION_MODEL'] = Transaction
        etc...

        And then will be initiated like this (immediately after, NOT before):
        assistant = Assistant.init_app(app)
        
        """

        self.app = app
    # After creating the db object fully...
    def _create(self, assistant_dict:dict):
        """This function creates an assistant in OpenAI from inside the db object"""
        
        assistant = self.client.beta.assistants.create(
            **assistant_dict
        )

        return assistant

    # Before (fix this function after getting _create() to work, so that
    # this function correctly makes the db object which uses _create())
    def create_assistant(self, assistant_dict: dict, meta_dict: dict):
        """ Creates a new assistant on OpenAI servers synchronously. assistant_dict passes all arguments directly to OpenAI. 
        See https://platform.openai.com/docs/api-reference/assistants/createAssistant for more information. 
        meta_dict helps construct the assistant inside the applicable databases in an autonomous way, and looks like this:
        {'passport_id': str(uuid),'external_ui': True, 'internal_ui': False, 'user_type': 'end_user',
        managing_teams: [{'type': 'admin', 'team_id': str(uuid), 'privileges': ['edit'], 'users': ['all' or {'admin_id': str(uuid), 'privileges': ['edit_instructions']}]}, 
        {'type: 'customer', 'team_id': str(uuid), 'privileges': ['owner'], 'users': ['all']}]}
        """
        if meta_dict['internal_ui'] is False:
            if meta_dict['user_type'] != 'end_user':
                raise ValueError("Internal UI is required based on user_type.")
        
        assistant = self.client.beta.assistants.create(
            **assistant_dict
        )

        if meta_dict['user_type'] == "system":
            self.system_assistant_model(assistant.id, json.dumps(meta_dict))

        elif meta_dict['user_type'] == 'admin':
            instance = self.admin_assistant_model(assistant.id, meta_dict['passport_id'], json.dumps(meta_dict))
            managing_teams = meta_dict['managing_teams']
            for team in managing_teams:
                for user in managing_teams['users']:
                    if team['type'] == "admin":
                        if user == "all":
                            all_team_user_links = self.admin_team_user_model.query.filter_by(admin_passport_id=team.admin_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.admin_assistants_admins_model(user_link.admin_id, assistant.id, team['privileges'])
                        else:
                            self.admin_assistants_admins_model(user['admin_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    else:
                        raise ValueError("admin assistant may only have admin teams as managing teams.")

        elif meta_dict['user_type'] == "customer":
            instance = self.customer_assistant_model(assistant.id, meta_dict['passport_id'], json.dumps(meta_dict))

            managing_teams = meta_dict['managing_teams']
            for team in managing_teams:
                for user in managing_teams['users']:
                    if team['type'] == "admin":
                        if user == "all":
                            all_team_user_links = self.admin_team_user_model.query.filter_by(admin_passport_id=team.admin_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.customer_assistants_admins_model(user_link.admin_id, assistant.id, team['privileges'])
                        else:
                            self.customer_assistants_admins_model(user['admin_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    elif team['type'] == "customer":
                        if user == "all":
                            all_team_user_links = self.customer_team_user_model.query.filter_by(admin_passport_id=team.admin_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.customer_assistants_admins_model(user_link.admin_id, assistant.id, team['privileges'])
                        else:
                            self.customer_assistants_admins_model(user['admin_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    else:
                        raise ValueError("customer assistant may only have admin teams and customer teams as managing teams.")
        
        elif meta_dict['user_type'] == "affiliate":
            instance = self.affiliate_assistant_model(assistant.id, meta_dict['passport_id'], json.dumps(meta_dict))

            managing_teams = meta_dict['managing_teams']
            for team in managing_teams:
                for user in managing_teams['users']:
                    if team['type'] == "admin":
                        if user == "all":
                            all_team_user_links = self.admin_team_user_model.query.filter_by(admin_passport_id=team.admin_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.affiliate_assistants_admins_model(user_link.admin_id, assistant.id, team['privileges'])
                        else:
                            self.affiliate_assistants_admins_model(user['admin_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    elif team['type'] == "customer":
                        if user == "all":
                            all_team_user_links = self.customer_team_user_model.query.filter_by(customer_passport_id=team.customer_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.affiliate_assistants_affiliates_model(user_link.cusotmer_id, assistant.id, team['privileges'])
                        else:
                            self.affiliate_assistants_customers_model(user['customer_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    elif team['type'] == "affiliate":
                        if user == "all":
                            all_team_user_links = self.affiliate_team_user_model.query.filter_by(affiliate_passport_id=team.affiliate_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.affiliate_assistants_affiliates_model(user_link.affiliate_id, assistant.id, team['privileges'])
                        else:
                            self.affiliate_assistants_affiliates_model(user['affiliate_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    else:
                        raise ValueError("affiliate assistant may only have admin teams, customer teams, and affiliate teams as managing teams.")
                    
        
        elif meta_dict['user_type'] == "end_user":
            instance = self.end_user_assistant_model(assistant_dict, meta_dict['passport_id'], json.dumps(meta_dict))

            managing_teams = meta_dict['managing_teams']
            for team in managing_teams:
                for user in managing_teams['users']:
                    if team['type'] == "admin":
                        if user == "all":
                            all_team_user_links = self.admin_team_user_model.query.filter_by(admin_passport_id=team.admin_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.end_user_assistants_admins_model(user_link.admin_id, assistant.id, team['privileges'])
                        else:
                            self.end_user_assistants_admins_model(user['admin_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    elif team['type'] == "customer":
                        if user == "all":
                            all_team_user_links = self.customer_team_user_model.query.filter_by(customer_passport_id=team.customer_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.end_user_assistants_customers_model(user_link.customer_id, assistant.id, team['privileges'])
                        else:
                            self.end_user_assistants_customers_model(user['customer_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    elif team['type'] == "affiliate":
                        if user == "all":
                            all_team_user_links = self.affiliate_team_user_model.query.filter_by(affiliate_passport_id=team.affiliate_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.end_user_assistants_affiliates_model(user_link.affiliate_id, assistant.id, team['privileges'])
                        else:
                            self.end_user_assistants_affiliates_model(user['affiliate_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])

                    elif team['type'] == "end_user":
                        if user == "all":
                            all_team_user_links = self.end_user_passport_model.query.filter_by(end_user_passport_id=team.end_user_passport_id)
                            for user_link in all_team_user_links:
                                user_assistant_link = self.end_user_assistants_end_users_model(user_link.end_user_id, assistant.id, team['privileges'])
                        else:
                            self.end_user_assistants_end_users_model(user['end_user_id'], assistant.id, user['privileges'] if len(user['privileges']) > 0 else team['privileges'])
                    else:
                        raise ValueError("end_user assistant may only have admin teams, customer teams, affiliate teams and end_users as managing teams.")

        return {'assistant': assistant, 'instance': instance, 'user_link': user_assistant_link}
    
    def list_assistants(self, order: Optional[str] = None, limit: Optional[int] = None):
        if order is not None:
            if limit is not None:
                limit_str = str(limit)
                my_assistants = self.client.beta.assistants.list(
                    order=order, limit=limit_str
                )
            else:
                my_assistants = self.client.beta.assistants.list(
                    order=order
                )
        else:
            if limit is not None:
                limit_str = str(limit)
                my_assistants = self.client.beta.assistants.list(
                    limit=limit_str
                )
            else:
                my_assistants = self.client.beta.assistants.list()
        
        return my_assistants

    def retrieve_assistant(self, assistant_id:str):
        assistant = self.client.beta.assistants.retrieve(assistant_id)

        return assistant

    def modify_assistant(self, assistant_id: str, name: Optional[str] = None, instructions: Optional[str] = None, tools_list: Optional[List[Any]] = None):
        model="gpt-4-turbo"
        assistant = self.client.beta.assistants.update(
            assistant_id,
            name=name,
            instructions=instructions,
            model=model,
            tools=tools_list,
        )

        return assistant


    def delete_assistant(self, assistant_id:str):
        assistant = self.client.beta.assistants.delete(assistant_id)

        return assistant


    def create_vector_store(self, name:str, expires_after: Optional[str] = None, metadata: Optional[str] = None, file_ids: Optional[List[Any]] = None):
        if expires_after is not None:
            if metadata is not None:
                if file_ids is not None:
                    vector_store = self.client.beta.vector_stores.create(name=name, expires_after=expires_after, metadata=metadata, file_ids=file_ids)
                else:
                    vector_store = self.client.beta.vector_stores.create(name=name, expires_after=expires_after, metadata=metadata)
            else:
                if file_ids is not None:
                    vector_store = self.client.beta.vector_stores.create(name=name, expires_after=expires_after, file_ids=file_ids)
                else:
                    vector_store = self.client.beta.vector_stores.create(name=name, expires_after=expires_after)
        else:
            if metadata is not None:
                if file_ids is not None:
                    vector_store = self.client.beta.vector_stores.create(name=name, metadata=metadata, file_ids=file_ids)
                else:
                    vector_store = self.client.beta.vector_stores.create(name=name, metadata=metadata)
            else:
                if file_ids is not None:
                    vector_store = self.client.beta.vector_stores.create(name=name, file_ids=file_ids)
                else:
                    vector_store = self.client.beta.vector_stores.create(name=name)

        return vector_store


    def create_vector_store_and_upload_file_completion(self, name:str, file_paths:list):
        # Create a vector store caled "Financial Statements"
        vector_store = self.create_vector_store(name=name)

        # Ready the files for upload to OpenAI 
        file_streams = [open(path, "rb") for path in file_paths]
        
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )
        
        # You can print the status and the file counts of the batch to see the result of this operation. 
        print(file_batch.status)
        print(file_batch.file_counts)

        return vector_store


    def list_vector_stores(self):
        vector_stores = self.client.beta.vector_stores.list()

        return vector_stores


    def retrieve_vector_store(self, vector_store_id):
        vector_store = self.client.beta.vector_stores.retrieve(vector_store_id=vector_store_id)
        
        return vector_store


    def modify_vector_store(self, vector_store_id: str, expires_after: Optional[str] = None, metadata: Optional[str] = None):
        if expires_after is not None:
            if metadata is not None:
                vector_store = self.client.beta.vector_stores.update(vector_store_id=vector_store_id, expires_after=expires_after, metadata=metadata)
            else:
                vector_store = self.client.beta.vector_stores.update(vector_store_id=vector_store_id, expires_after=expires_after)
        else:
            if metadata is not None:
                vector_store = self.client.beta.vector_stores.update(vector_store_id=vector_store_id, metadata=metadata)

        return vector_store


    def delete_vector_store(self, vector_store_id):
        vector_store = self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
        
        return vector_store


    def create_file(self, filename: str):
        extension = filename.split('.')[-1]
        if extension == "jsonl":
            openai_file = self.client.files.create(
                file=open(filename, "rb"),
                purpose="fine-tune"
            )
        else:
            openai_file = self.client.files.create(
                file=open(filename, "rb"), 
                purpose="assistants"
            )
        
        return openai_file

    def list_files(self, purpose: Optional[str] = None):
        if purpose is not None and (purpose == "assistants" or purpose == "fine_tuning"):
            all_files = self.client.files.list(purpose=purpose)
        else:
            all_files = self.client.files.list()

        return all_files

    def retrieve_file(self, file_id):
        openai_file = self.client.files.retrieve(file_id)

        return openai_file

    def retrieve_file_content(self, file_id):
        content = self.client.files.content(file_id)
        
        return content


    def delete_file(self, file_id):
        openai_file = self.client.files.delete(file_id)

        return openai_file


    def create_vector_store_file(self, vector_store_id: str, file_id: str):
        vector_store_file = self.client.beta.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id
        )

        return vector_store_file

    def list_vector_store_files(self, vector_store_id: str):
        vector_store_files = self.client.beta.vector_stores.files.list(
            vector_store_id=vector_store_id
        )

        return vector_store_files

    def retrieve_vector_store_file(self, vector_store_id: str, file_id: str):
        vector_store_file = self.client.beta.vector_stores.files.retrieve(
            vector_store_id=vector_store_id,
            file_id=file_id
        )

        return vector_store_file


    def delete_vector_store_file(self, vector_store_id: str, file_id: str):
        vector_store_file = self.client.beta.vector_stores.files.delete(
            vector_store_id=vector_store_id,
            file_id=file_id
        )

        return vector_store_file


    def create_vector_store_file_batch(self, vector_store_id: str, file_ids: list):
        vector_store_file_batch = self.client.beta.vector_stores.file_batches.create(
            vector_store_id=vector_store_id,
            file_ids=file_ids
        )

        return vector_store_file_batch

    def retrieve_vector_store_file_batch(self, vector_store_id: str, batch_id: str):
        vector_store_file_batch = self.client.beta.vector_stores.file_batches.retrieve(
            vector_store_id=vector_store_id,
            batch_id=batch_id
        )

        return vector_store_file_batch


    def cancel_vector_store_file_batch(self, vector_store_id: str, batch_id: str):
        deleted_vector_store_file_batch = self.client.beta.vector_stores.file_batches.cancel(
            vector_store_id=vector_store_id,
            file_batch_id=batch_id
        )

        return deleted_vector_store_file_batch

    def list_files_in_vector_store_as_batch(self, vector_store_id: str, batch_id: str):
        vector_store_files = self.client.beta.vector_stores.file_batches.list_files(
            vector_store_id=vector_store_id,
            batch_id=batch_id
        )

        return vector_store_files

    def create_thread(self, messages: Optional[List[Any]], metadata: Optional[str] = None, tool_resources: Optional[dict] = None):
        if messages is not None:
            if tool_resources is not None:
                thread = self.client.beta.threads.create(messages=messages, tool_resources=tool_resources)
            else:
                thread = self.client.beta.threads.create(messages=messages)
        else:
            if tool_resources is not None:
                thread = self.client.beta.threads.create(tool_resources=tool_resources)
            else:
                thread = self.client.beta.threads.create()

        return thread




    def retrieve_thread(self, thread_id: str):
        thread = self.client.beta.threads.retrieve(thread_id=thread_id)

        return thread


    def modify_thread(self, thread_id: str, metadata: Optional[str] = None, tool_resources: Optional[str] = None):
        if metadata is not None:
            if tool_resources is not None:
                thread = self.client.beta.threads.update(
                    thread_id, metadata=metadata, tool_resources=tool_resources
                )
            else:
                thread = self.client.beta.threads.update(
                    thread_id, metadata=metadata
                )

        else:
            if tool_resources is not None:
                thread = self.client.beta.threads.update(
                    thread_id, tool_resources=tool_resources
                )


        return thread


    def delete_thread(self, thread_id: str):
        response = self.client.beta.threads.delete(thread_id=thread_id)

        return response


    def create_message_in_thread(self, thread_id: str, role: str, content: str, attachments: Optional[List[Any]], metadata: Optional[str] = None):
        if attachments is not None:
            if metadata is not None:
                thread_message = self.client.beta.threads.messages.create(
                    thread_id, role=role, content=content, attachments=attachments, metadata=metadata
                )
            else:
                thread_message = self.client.beta.threads.messages.create(
                    thread_id, role=role, content=content, attachments=attachments
                )
        else:
            if metadata is not None:
                thread_message = self.client.beta.threads.messages.create(
                    thread_id, role=role, content=content, metadata=metadata
                )
            else:
                thread_message = self.client.beta.threads.messages.create(
                    thread_id, role=role, content=content
                )
        
        return thread_message

    def list_messages_in_thread(self,thread_id:str, limit: Optional[int] = None, order: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, run_id: Optional[str] = None):
        if limit is not None:
            if order is not None:
                if before is not None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before, after=after)
                elif before is not None and after is None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before)
                elif before is None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order, after=after)
                else:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, order=order)
            else:
                if before is not None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, before=before, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, before=before, after=after)
                elif before is not None and after is None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, before=before, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, before=before)
                elif before is None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, after=after)
                else:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, limit=limit)
        else:
            if order is not None:
                if before is not None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order, before=before, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order, before=before, after=after)
                elif before is not None and after is None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order, before=before, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order, before=before)
                elif before is None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order, after=after)
                else:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, order=order)
            else:
                if before is not None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, before=before, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, before=before, after=after)
                elif before is not None and after is None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, before=before, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, before=before)
                elif before is None and after is not None:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, after=after, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id, after=after)
                else:
                    if run_id is not None:
                        messages_list = self.client.beta.threads.messages.list(thread_id, run_id=run_id)
                    else:
                        messages_list = self.client.beta.threads.messages.list(thread_id)

        return messages_list


    def retrieve_message_in_thread(self, thread_id: str, message_id: str):
        message = self.client.beta.threads.messages.retrieve(
            thread_id=thread_id,
            message_id=message_id
        )

        return message

    def modify_message_in_thread(self, thread_id: str, message_id: str, metadata: str):
        # only allowed to update metadata for now.
        message = self.client.beta.threads.messages.update(
            thread_id=thread_id,
            message_id=message_id,
            metadata=metadata,
        )

        return message

    def create_run(self, assistant_id: str, thread_id: str, run_dict: Optional[str] = None):
        run = self.client.beta.threads.runs.create(
            **run_dict, assistant_id=assistant_id, thread_id=thread_id, 
        )

        return run

    def create_thread_and_run(self, assistant_id: str, run_dict: Optional[str] = None):
        run = self.client.beta.threads.create_and_run(
            **run_dict,
            assistant_id=assistant_id
        )

        return run

    def create_run_stream(self, assistant_id: str, thread_id: str, run_dict: Optional[str] = None):
        if run_dict is not None:
            with self.client.beta.threads.runs.stream(**run_dict, assistant_id=assistant_id, thread_id=thread_id, 
                                                event_handler=SSEAssistantEventHandler()) as stream:
                stream.until_done()
        else:
            with self.client.beta.threads.runs.stream(assistant_id=assistant_id, thread_id=thread_id, 
                                                event_handler=SSEAssistantEventHandler()) as stream:
                stream.until_done()


    def list_runs_from_thread(self, thread_id: str, limit: Optional[int] = None, order: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None):
        if limit is not None:
            if order is not None:
                if before is not None:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit, order=order, before=before, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit, order=order, before=before
                        )
                else:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit, order=order, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit, order=order
                        )
            else:
                if before is not None:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit, before=before, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit, before=before
                        )
                else:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, limit=limit
                        )
        else:
            if order is not None:
                if before is not None:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, order=order, before=before, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, order=order, before=before
                        )
                else:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, order=order, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, order=order
                        )
            else:
                if before is not None:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, before=before, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, before=before
                        )
                else:
                    if after is not None:
                        runs = self.client.beta.threads.runs.list(
                            thread_id, after=after
                        )
                    else:
                        runs = self.client.beta.threads.runs.list(
                            thread_id
                        )

        return runs

    def retrieve_run_from_thread(self, thread_id: str, run_id: str):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        return run


    def modify_run_from_thread(self, thread_id: str, run_id: str, metadata: dict):
        run = self.client.beta.threads.runs.update(
            thread_id=thread_id,
            run_id=run_id,
            metadata=metadata,
        )

        return run

    def submit_finalized_tool_outputs_to_run(self, thread_id: str, run_id: str, tool_outputs: list):
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

        return run


    def cancel_run(self, thread_id: str, run_id: str):
        run = self.client.beta.threads.runs.cancel(
            thread_id=thread_id,
            run_id=run_id
        )

        return run


    def list_run_steps(self, thread_id: str, run_id: str):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=thread_id,
            run_id=run_id
        )

        return run_steps


    def retrieve_run_step(self, thread_id: str, run_id: str, step_id: str):
        run_steps = self.client.beta.threads.runs.steps.retrieve(
            thread_id=thread_id,
            run_id=run_id,
            step_id=step_id
        )

        return run_steps
    

    def stream_assistant_responses(self, thread_id, assistant_id, event_handler):
        """ Generator function to stream responses from OpenAI Assistant. """
        with self.client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler
        ) as stream:
            stream.until_done()
            for event in event_handler.get_events():
                yield event



class SSEAssistantEventHandler(AssistantEventHandler):
    def __init__(self):
        self.buffer = []

    def on_text_created(self, text) -> None:
        self.buffer.append(f"data: {text}\n\n")

    def on_text_delta(self, delta, snapshot):
        self.buffer.append(f"data: {delta.value}\n\n")

    def get_events(self):
        return self.buffer
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
 
# from flask import Response, stream_with_context

# assistants = FlaskAssistants(app)

# @app.route('/stream_response')
# def stream_response():
#     # Example thread and assistant IDs, these should be dynamically determined as needed
#     thread_id = "your_thread_id"
#     assistant_id = "your_assistant_id"
#     event_handler = SSEAssistantEventHandler()

#     return Response(
#         stream_with_context(assistants.stream_assistant_responses(thread_id, assistant_id, event_handler)),
#         mimetype='text/event-stream'
#     )