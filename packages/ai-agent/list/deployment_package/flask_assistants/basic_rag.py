from openai import OpenAI
from typing import Optional, List, Any
import os
import mimetypes
from dotenv import load_dotenv

from streaming import EventHandler



def create_assistant(assistant_dict: dict):
    
    assistant = client.beta.assistants.create(
        **assistant_dict
    )

    return assistant

def list_assistants(order: Optional[str] = None, limit: Optional[int] = None):
    if order is not None:
        if limit is not None:
            limit_str = str(limit)
            my_assistants = client.beta.assistants.list(
                order=order, limit=limit_str
            )
        else:
            my_assistants = client.beta.assistants.list(
                order=order
            )
    else:
        my_assistants = client.beta.assistants.list()
    
    return my_assistants

def retrieve_assistant(assistant_id:str):
    assistant = client.beta.assistants.retrieve(assistant_id)

    return assistant

def modify_assistant(assistant_id: str, name: Optional[str] = None, instructions: Optional[str] = None, tools_list: Optional[List[Any]] = None):
    model="gpt-4-turbo"
    assistant = client.beta.assistants.update(
        assistant_id,
        name=name,
        instructions=instructions,
        model=model,
        tools=tools_list,
    )

    return assistant


def delete_assistant(assistant_id:str):
    assistant = client.beta.assistants.delete(assistant_id)

    return assistant


def create_vector_store(name:str, expires_after: Optional[str] = None, metadata: Optional[str] = None, file_ids: Optional[List[Any]] = None):
    if expires_after is not None:
        if metadata is not None:
            if file_ids is not None:
                vector_store = client.beta.vector_stores.create(name=name, expires_after=expires_after, metadata=metadata, file_ids=file_ids)
            else:
                vector_store = client.beta.vector_stores.create(name=name, expires_after=expires_after, metadata=metadata)
        else:
            if file_ids is not None:
                vector_store = client.beta.vector_stores.create(name=name, expires_after=expires_after, file_ids=file_ids)
            else:
                vector_store = client.beta.vector_stores.create(name=name, expires_after=expires_after)
    else:
        if metadata is not None:
            if file_ids is not None:
                vector_store = client.beta.vector_stores.create(name=name, metadata=metadata, file_ids=file_ids)
            else:
                vector_store = client.beta.vector_stores.create(name=name, metadata=metadata)
        else:
            if file_ids is not None:
                vector_store = client.beta.vector_stores.create(name=name, file_ids=file_ids)
            else:
                vector_store = client.beta.vector_stores.create(name=name)

    return vector_store


def create_vector_store_and_upload_file_completion(name:str, file_paths:list):
    # Create a vector store caled "Financial Statements"
    vector_store = create_vector_store(name=name)

    # Ready the files for upload to OpenAI 
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
    )
    
    # You can print the status and the file counts of the batch to see the result of this operation. 
    print(file_batch.status)
    print(file_batch.file_counts)

    return vector_store


def list_vector_stores():
    vector_stores = client.beta.vector_stores.list()

    return vector_stores


def retrieve_vector_store(vector_store_id):
    vector_store = client.beta.vector_stores.retrieve(vector_store_id=vector_store_id)
    
    return vector_store


def modify_vector_store(vector_store_id: str, expires_after: Optional[str] = None, metadata: Optional[str] = None):
    if expires_after is not None:
        if metadata is not None:
            vector_store = client.beta.vector_stores.update(vector_store_id=vector_store_id, expires_after=expires_after, metadata=metadata)
        else:
            vector_store = client.beta.vector_stores.update(vector_store_id=vector_store_id, expires_after=expires_after)
    else:
        if metadata is not None:
            vector_store = client.beta.vector_stores.update(vector_store_id=vector_store_id, metadata=metadata)

    return vector_store


def delete_vector_store(vector_store_id):
    vector_store = client.beta.vector_stores.delete(vector_store_id=vector_store_id)
    
    return vector_store


def create_file(filename: str):
    extension = filename.split('.')[-1]
    if extension == "jsonl":
        openai_file = client.files.create(
            file=open(filename, "rb"),
            purpose="fine-tune"
        )
    else:
        openai_file = client.files.create(
            file=open(filename, "rb"), 
            purpose="assistants"
        )
    
    return openai_file

def list_files(purpose: Optional[str] = None):
    if purpose is not None and (purpose == "assistants" or purpose == "fine_tuning"):
        all_files = client.files.list(purpose=purpose)
    else:
        all_files = client.files.list()

    return all_files

def retrieve_file(file_id):
    openai_file = client.files.retrieve(file_id)

    return openai_file

def retrieve_file_content(file_id):
    content = client.files.content(file_id)
    
    return content


def delete_file(file_id):
    openai_file = client.files.delete(file_id)

    return openai_file


def create_vector_store_file(vector_store_id: str, file_id: str):
    vector_store_file = client.beta.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=file_id
    )

    return vector_store_file

def list_vector_store_files(vector_store_id: str):
    vector_store_files = client.beta.vector_stores.files.list(
        vector_store_id=vector_store_id
    )

    return vector_store_files

def retrieve_vector_store_file(vector_store_id: str, file_id: str):
    vector_store_file = client.beta.vector_stores.files.retrieve(
        vector_store_id=vector_store_id,
        file_id=file_id
    )

    return vector_store_file


def delete_vector_store_file(vector_store_id: str, file_id: str):
    vector_store_file = client.beta.vector_stores.files.delete(
        vector_store_id=vector_store_id,
        file_id=file_id
    )

    return vector_store_file


def create_vector_store_file_batch(vector_store_id: str, file_ids: list):
    vector_store_file_batch = client.beta.vector_stores.file_batches.create(
        vector_store_id=vector_store_id,
        file_ids=file_ids
    )

    return vector_store_file_batch

def retrieve_vector_store_file_batch(vector_store_id: str, batch_id: str):
    vector_store_file_batch = client.beta.vector_stores.file_batches.retrieve(
        vector_store_id=vector_store_id,
        batch_id=batch_id
    )

    return vector_store_file_batch


def cancel_vector_store_file_batch(vector_store_id: str, batch_id: str):
    deleted_vector_store_file_batch = client.beta.vector_stores.file_batches.cancel(
        vector_store_id=vector_store_id,
        file_batch_id=batch_id
    )

    return deleted_vector_store_file_batch

def list_files_in_vector_store_as_batch(vector_store_id: str, batch_id: str):
    vector_store_files = client.beta.vector_stores.file_batches.list_files(
        vector_store_id=vector_store_id,
        batch_id=batch_id
    )

    return vector_store_files

def create_thread(messages: Optional[List[Any]], metadata: Optional[str] = None, tool_resources: Optional[dict] = None):
    if messages is not None:
        if tool_resources is not None:
            thread = client.beta.threads.create(messages=messages, tool_resources=tool_resources)
        else:
            thread = client.beta.threads.create(messages=messages)
    else:
        if tool_resources is not None:
            thread = client.beta.threads.create(tool_resources=tool_resources)
        else:
            thread = client.beta.threads.create()

    return thread




def retrieve_thread(thread_id: str):
    thread = client.beta.threads.retrieve(thread_id=thread_id)

    return thread


def modify_thread(thread_id: str, metadata: Optional[str] = None, tool_resources: Optional[str] = None):
    if metadata is not None:
        if tool_resources is not None:
            thread = client.beta.threads.update(
                thread_id, metadata=metadata, tool_resources=tool_resources
            )
        else:
            thread = client.beta.threads.update(
                thread_id, metadata=metadata
            )

    else:
        if tool_resources is not None:
            thread = client.beta.threads.update(
                thread_id, tool_resources=tool_resources
            )


    return thread


def delete_thread(thread_id: str):
    response = client.beta.threads.delete(thread_id=thread_id)

    return response


def create_message_in_thread(thread_id: str, role: str, content: str, attachments: Optional[List[Any]], metadata: Optional[str] = None):
    if attachments is not None:
        if metadata is not None:
            thread_message = client.beta.threads.messages.create(
                thread_id, role=role, content=content, attachments=attachments, metadata=metadata
            )
        else:
            thread_message = client.beta.threads.messages.create(
                thread_id, role=role, content=content, attachments=attachments
            )
    else:
        if metadata is not None:
            thread_message = client.beta.threads.messages.create(
                thread_id, role=role, content=content, metadata=metadata
            )
        else:
            thread_message = client.beta.threads.messages.create(
                thread_id, role=role, content=content
            )
    
    return thread_message

def list_messages_in_thread(thread_id:str, limit: Optional[int] = None, order: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, run_id: Optional[str] = None):
    if limit is not None:
        if order is not None:
            if before is not None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before, after=after)
            elif before is not None and after is None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order, before=before)
            elif before is None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order, after=after)
            else:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, order=order)
        else:
            if before is not None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, before=before, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, before=before, after=after)
            elif before is not None and after is None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, before=before, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, before=before)
            elif before is None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, after=after)
            else:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, limit=limit)
    else:
        if order is not None:
            if before is not None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order, before=before, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order, before=before, after=after)
            elif before is not None and after is None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order, before=before, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order, before=before)
            elif before is None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order, after=after)
            else:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, order=order)
        else:
            if before is not None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, before=before, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, before=before, after=after)
            elif before is not None and after is None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, before=before, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, before=before)
            elif before is None and after is not None:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, after=after, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id, after=after)
            else:
                if run_id is not None:
                    messages_list = client.beta.threads.messages.list(thread_id, run_id=run_id)
                else:
                    messages_list = client.beta.threads.messages.list(thread_id)

    return messages_list


def retrieve_message_in_thread(thread_id: str, message_id: str):
    message = client.beta.threads.messages.retrieve(
        thread_id=thread_id,
        message_id=message_id
    )

    return message

def modify_message_in_thread(thread_id: str, message_id: str, metadata: str):
    # only allowed to update metadata for now.
    message = client.beta.threads.messages.update(
        thread_id=thread_id,
        message_id=message_id,
        metadata=metadata,
    )

    return message

def create_run(assistant_id: str, thread_id: str, run_dict: Optional[str] = None):
    run = client.beta.threads.runs.create(
        **run_dict, assistant_id=assistant_id, thread_id=thread_id, 
    )

    return run

def create_thread_and_run(assistant_id: str, run_dict: Optional[str] = None):
    run = client.beta.threads.create_and_run(
        **run_dict,
        assistant_id=assistant_id
    )

    return run

def create_run_stream(assistant_id: str, thread_id: str, run_dict: Optional[str] = None):
    if run_dict is not None:
        with client.beta.threads.runs.stream(**run_dict, assistant_id=assistant_id, thread_id=thread_id, 
                                            event_handler=EventHandler()) as stream:
            stream.until_done()
    else:
        with client.beta.threads.runs.stream(assistant_id=assistant_id, thread_id=thread_id, 
                                            event_handler=EventHandler()) as stream:
            stream.until_done()


def list_runs_from_thread(thread_id: str, limit: Optional[int] = None, order: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None):
    if limit is not None:
        if order is not None:
            if before is not None:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit, order=order, before=before, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit, order=order, before=before
                    )
            else:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit, order=order, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit, order=order
                    )
        else:
            if before is not None:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit, before=before, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit, before=before
                    )
            else:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id, limit=limit
                    )
    else:
        if order is not None:
            if before is not None:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, order=order, before=before, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id, order=order, before=before
                    )
            else:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, order=order, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id, order=order
                    )
        else:
            if before is not None:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, before=before, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id, before=before
                    )
            else:
                if after is not None:
                    runs = client.beta.threads.runs.list(
                        thread_id, after=after
                    )
                else:
                    runs = client.beta.threads.runs.list(
                        thread_id
                    )

    return runs

def retrieve_run_from_thread(thread_id: str, run_id: str):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )

    return run


def modify_run_from_thread(thread_id: str, run_id: str, metadata: dict):
    run = client.beta.threads.runs.update(
        thread_id=thread_id,
        run_id=run_id,
        metadata=metadata,
    )

    return run

def submit_finalized_tool_outputs_to_run(thread_id: str, run_id: str, tool_outputs: list):
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )

    return run


def cancel_run(thread_id: str, run_id: str):
    run = client.beta.threads.runs.cancel(
        thread_id=thread_id,
        run_id=run_id
    )

    return run


def list_run_steps(thread_id: str, run_id: str):
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id
    )

    return run_steps


def retrieve_run_step(thread_id: str, run_id: str, step_id: str):
    run_steps = client.beta.threads.runs.steps.retrieve(
        thread_id=thread_id,
        run_id=run_id,
        step_id=step_id
    )

    return run_steps


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()

    # file_paths = ['exercise_sales_data.pdf']
    # create_vector_store_and_upload_file_completion("Sales Data", file_paths)

    assistants = list_assistants()
    print(assistants)
