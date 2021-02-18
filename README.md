# Coding Example Assignment

This python module is intended to handle Use Cases 1 and 6 of 
the US SBA PPP Loan Forgiveness API found [here](https://ussbaforgiveness.github.io/).

## Requirements

The module requires the [PPPForgivenessSDK](https://github.com/UsSbaForgiveness/sba-python-client).

## Usage

The `submit_forgiveness_request` method submits a forgiveness request for SBA decisioning.
Documents can be submitted with the forgiveness request using the `documents` argument.

The `view_disbursed_loans` method fetches and returns the data of a single SBA loan.