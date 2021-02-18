from typing import List, Dict
from PPPForgivenessSDK.client import Client

def submit_forgiveness_request(client: Client,
                               bank_notional_amount: float,
                               etran_notional_amount: float,
                               sba_number: str,
                               entity_name: str,
                               ein: str,
                               funding_date: str,
                               documents: List[Dict] = [],
                              ) -> str:
    """
    This method will create a forgiveness request and upload any relevant documents if provided.
    :param client: A client object
    :param bank_notional_amount: The PPP loan amount
    :param etran_notional_amount:
    :param sba_number: The SBA loan number
    :param entity_name: The entity name of the borrower
    :param ein: The SSN or Business TIN of the borrower
    :param funding_date: PPP loan Disbursement date in YYYY-MM-DD
    :param documents: A list of dictionaries representing files to be uploaded with the forgiveness request. Each dictionary
        should contain a name, document type, and document path.
        name: The name of document
        document_type: The type of document uploaded
        document_path: File path of the file to be uploaded
    :return: The data contained in the creation response received as well as an error message if one occurred.
    """
    forgiveness_api = client.forgiveness_requests
    loan_documents_api = client.loan_documents

    creation_result = forgiveness_api.create(
        bank_notional_amount=bank_notional_amount,
        etran_notional_amount=etran_notional_amount,
        sba_number=sba_number,
        entity_name=entity_name,
        ein=ein,
        funding_date=funding_date,
        ez_form= False,
        s_form=True,
    )

    if creation_result['status'] == 201:
        slug = creation_result['data']['etran_loan']['slug']
        for doc in documents:
            assert "name" in doc, "Missing name from document {}".format(doc)
            assert "document_type" in doc, "Missing document_type from document {}".format(doc)
            assert "document_path" in doc, "Missing document_path from document {}".format(doc)

            doc_result = loan_documents_api.create(doc["name"], doc["document_type"], slug, doc["document_path"])

            if doc_result['status'] != 201:
                return "An error occurred while uploading {}. Status: {}\n{}".format(doc["name"], doc_result["status"], doc_result['data'])
    else:
        return "An error occurred during creation. {}\n{}".format(str(creation_result['status']), creation_result['data'])
    return creation_result["data"]


def view_disbursed_loans(client: Client, sba_number: str = None) -> str:
    """
    This method will return data on disbursed loans, or the data of a specific loan if sba_number is provided
    :param client: A client object
    :param sba_number: The SBA loan number
    :return: The data contained in the lookup request as well as an error message if one occurred.
    """

    lookup_api = client.validations
    result = lookup_api.list(sba_number=sba_number)
    if result['status'] == 200:
        return result['data']
    else:
        return "An error occurred. {}\n{}".format(str(result['status']), result['data'])