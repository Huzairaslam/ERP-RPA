*** Settings ***
Library    JSONLibrary
Library    Collections

*** Variables ***
${API_RESPONSE}=    {"document_type": "Purchase Bill", "company_name": "THE FLEX SHOP", "company_address": ["INDUSTRIAL ESTAE", "MULTAN"], "bill_date": "02-09-2025", "po_number": "40", "customer_info": {"invoice_number": "12", "customer_name": "", "customer_address": "Industrial est area Multan"}, "line_items": [{"product": "BAG SHADMAN TS", "policy": "/", "batch_number": null, "quantity": "1000 Piece", "rate": 80, "gross_amount": 80000, "discount_amount": 0, "net_amount": 80000, "cartons_bags_drums": null, "packs": null}, {"product": "CABLE TIE", "policy": "/", "batch_number": null, "quantity": "1000 Piece", "rate": 2.5, "gross_amount": 2500, "discount_amount": 0, "net_amount": 2500, "cartons_bags_drums": null, "packs": null}, {"product": "INNER 24X43 (50KG)", "policy": "/", "batch_number": null, "quantity": "50 Kg", "rate": 430, "gross_amount": 21500, "discount_amount": 0, "net_amount": 21500, "cartons_bags_drums": null, "packs": null}], "summary": {"total_gross_amount": 104000, "total_discount_amount": 0, "total_net_amount": 104000}, "footer": {"created_by": "Malik Safdar"}, "other_info": {"extraction_timestamp": "9/13/25, 6:02 PM", "print_date": null, "store": null, "su": null, "tm_contact": null}, "arabic_text_present": false}

*** Keywords ***
Parse API Response
    ${json}=    Load JSON From String    ${API_RESPONSE}

    ${document_type}=    Get Value From Json    ${json}    $.document_type
    ${company_name}=     Get Value From Json    ${json}    $.company_name
    ${bill_date}=        Get Value From Json    ${json}    $.bill_date
    ${po_number}=        Get Value From Json    ${json}    $.po_number

    ${invoice_number}=   Get Value From Json    ${json}    $.customer_info.invoice_number
    ${customer_name}=    Get Value From Json    ${json}    $.customer_info.customer_name
    ${customer_address}= Get Value From Json    ${json}    $.customer_info.customer_address

    ${first_item_product}=    Get Value From Json    ${json}    $.line_items[0].product
    ${first_item_quantity}=   Get Value From Json    ${json}    $.line_items[0].quantity
    ${first_item_rate}=       Get Value From Json    ${json}    $.line_items[0].rate
    ${first_item_net}=        Get Value From Json    ${json}    $.line_items[0].net_amount

    ${total_net_amount}=  Get Value From Json    ${json}    $.summary.total_net_amount
    ${created_by}=        Get Value From Json    ${json}    $.footer.created_by

    Log To Console    Document: ${document_type}
    Log To Console    Vendor: ${company_name}
    Log To Console    Invoice #: ${invoice_number}
    Log To Console    First Item: ${first_item_product} - ${first_item_quantity} - ${first_item_rate}
    Log To Console    Total Net: ${total_net_amount}
    Log To Console    Created By: ${created_by}