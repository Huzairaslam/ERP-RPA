*** Settings ***
Library    JSONLibrary
Library    Collections

*** Variables ***
${API_RESPONSE}=    {"document_type": "Purchase Bill", "company_name": "THE FLEX SHOP", "company_address": ["INDUSTRIAL ESTAE", "MULTAN"], "bill_date": "02-09-2025", "po_number": "40", "customer_info": {"invoice_number": "12", "customer_name": "THE FLEX SHOP", "customer_address": "Industrial est area Multan"}, "line_items": [{"product": "BAG SHADMAN TS", "policy": "/", "batch_number": null, "quantity": "1000 Piece", "rate": 80, "gross_amount": 80000, "discount_amount": 0, "net_amount": 80000, "cartons_bags_drums": null, "packs": null}, {"product": "CABLE TIE", "policy": "/", "batch_number": null, "quantity": "1000 Piece", "rate": 2.5, "gross_amount": 2500, "discount_amount": 0, "net_amount": 2500, "cartons_bags_drums": null, "packs": null}, {"product": "INNER 24X43 (50KG)", "policy": "/", "batch_number": null, "quantity": "50 Kg", "rate": 430, "gross_amount": 21500, "discount_amount": 0, "net_amount": 21500, "cartons_bags_drums": null, "packs": null}], "summary": {"total_gross_amount": 104000, "total_discount_amount": 0, "total_net_amount": 104000}, "footer": {"created_by": "Malik Safdar"}, "other_info": {"extraction_timestamp": "9/13/25, 6:02 PM", "print_date": null, "store": null, "su": null, "tm_contact": null}, "arabic_text_present": false}

*** Keywords ***
Parse API Response
    ${json}=    Evaluate    json.loads('''${API_RESPONSE}''')    json

    ${document_type}=    Get Value From Json    ${json}    $.document_type
    Set Global Variable    ${document_type}    ${document_type[0]}

    ${company_name}=     Get Value From Json    ${json}    $.company_name
    Set Global Variable    ${company_name}    ${company_name[0]}

    ${doc_date}=        Get Value From Json    ${json}    $.bill_date
    Set Global Variable    ${doc_date}    ${doc_date[0]}

    ${vendor_number}=        Get Value From Json    ${json}    $.po_number
    Set Global Variable    ${vendor_number}    ${vendor_number[0]}

    ${invoice_number}=   Get Value From Json    ${json}    $.customer_info.invoice_number
    Set Global Variable    ${invoice_number}    ${invoice_number[0]}

    ${vendor_name}=    Get Value From Json    ${json}    $.customer_info.customer_name
    Set Global Variable    ${vendor_name}    ${vendor_name[0]}

    ${delivery_address}=    Get Value From Json    ${json}    $.customer_info.customer_address
    Set Global Variable    ${delivery_address}    ${delivery_address[0]}
    
    ${first_item_product}=    Get Value From Json    ${json}    $.line_items[0].product
    Set Global Variable    ${first_item_product}    ${first_item_product[0]}
    
    ${first_item_quantity}=   Get Value From Json    ${json}    $.line_items[0].quantity
    Set Global Variable    ${first_item_quantity}    ${first_item_quantity[0]}
    
    ${first_item_rate}=       Get Value From Json    ${json}    $.line_items[0].rate
    Set Global Variable    ${first_item_rate}    ${first_item_rate[0]}
    
    ${first_item_net}=        Get Value From Json    ${json}    $.line_items[0].net_amount
    Set Global Variable    ${first_item_net}    ${first_item_net[0]}
    
    ${total_net_amount}=  Get Value From Json    ${json}    $.summary.total_net_amount
    Set Global Variable    ${total_net_amount}    ${total_net_amount[0]}
    
    ${created_by}=        Get Value From Json    ${json}    $.footer.created_by
    Set Global Variable    ${created_by}    ${created_by[0]}

    Log To Console    📌 Parsed Values:
    Log To Console    Document: ${document_type}
    Log To Console    Vendor: ${company_name}
    Log To Console    Invoice #: ${invoice_number}
    Log To Console    DocDate: ${doc_date}
    Log To Console    First Item: ${first_item_product} - ${first_item_quantity} - ${first_item_rate}
    Log To Console    Total Net: ${total_net_amount}
    Log To Console    Created By: ${created_by}
