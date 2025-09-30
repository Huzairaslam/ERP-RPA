*** Settings ***
Library    RequestsLibrary
# Library    JSONLibrary   <-- REMOVED
Library    BuiltIn
Library    Collections

*** Variables ***
${BASE_URL}           http://api.rabtai.3em.tech/api/Feed
${TEMPLATE_NAME}      Purchase Bill Form

*** Keywords ***

Fetch Latest Record
    [Documentation]    Fetch latest unposted record dynamically for given template
    # Ensures 'json' module is available for Evaluate
    Import Library    json

    Create Session    api    ${BASE_URL}

    # # Step 1: Get Summarized Records
    # ${resp}=    GET On Session    api    /SummarizeRecords
    # Should Be Equal As Integers    ${resp.status_code}    200
    # # FIX: Replaced deprecated 'To Json'
    # ${summary}=    Set Variable    ${resp.json()}

    # ${templates}=    Get From Dictionary    ${summary}    data

    # ${template_id}=    Set Variable    None
    # FOR    ${tpl}    IN    @{templates}
    #     ${name}=    Get From Dictionary    ${tpl}    templateName
        
    #     # FIX: Robust case-insensitive template match
    #     ${is_match}=    Evaluate    '${name}'.lower() == '${TEMPLATE_NAME}'.lower()
        
    #     # FIX: Use Exit For Loop to reliably set and exit
    #     Run Keyword If    ${is_match}    Set Variable    ${template_id}    ${tpl["templateId"]}    
    #     Run Keyword If    '${template_id}' != 'None'    Exit For Loop
    # END

    # # Add the explicit Failure check back (it was commented out)
    # Run Keyword If    '${template_id}' == 'None'    Fail    Template ${TEMPLATE_NAME} not found in summary response

    # Step 2: Fetch records for this template
    ${resp2}=    GET On Session    api    /GetByTemplateId/68db9fa01f47f0b154b80c31
    Should Be Equal As Integers    ${resp2.status_code}    200
    ${record}=    Set Variable    ${resp2.json()}

    # Get the single record from the 'data' dictionary field
    ${first_record}=    Get From Dictionary    ${record}    data 

    ${FILE_ID}=    Get From Dictionary    ${first_record}    id
    Set Global Variable    ${FILE_ID}

    # FIX: Use Evaluate to parse stringified JSON fields
    ${llm_response}=    Evaluate    json.loads('''${first_record["llmResponse"]}''')    json
    Set Global Variable    ${LLM_RESPONSE}    ${llm_response}

    ${form_data}=    Evaluate    json.loads('''${first_record["formData"]}''')    json
    Set Global Variable    ${FORM_DATA}    ${form_data}

    # Extract Header Info (Header is the root of the formData)
    ${header}=    Set Variable    ${FORM_DATA}
    
    Set Global Variable    ${DOC_DATE}       ${header["docDate"]}
    Set Global Variable    ${VENDOR}         ${header["vendor"]}
    Set Global Variable    ${PURCHASEORDER}        ${header["purchaseOrder"]}
    # FIX: Corrected typo 'vedorOrderNumber' -> 'vendorOrderNumber'
    Set Global Variable    ${VendorOrderNumber}         ${header["vendorOrderNumber"]}
    Set Global Variable    ${DeliveryAddress}         ${header["deliveryAddress"]}


    # Extract Items (using LLM_RESPONSE since it contains the quantity/rate keys you are using below)
    ${items}=    Get From Dictionary    ${LLM_RESPONSE}    items
    Set Global Variable    ${ITEMS}          ${items}

    ${first_item}=    Get From List    ${ITEMS}    0 
    
    # Keys matched to the LLM response structure you provided
    ${sku}=    Get From Dictionary    ${first_item}    item_name  
    ${qty}=    Get From Dictionary    ${first_item}    quantity
    ${rate}=   Get From Dictionary    ${first_item}    unit_price 
    ${amount}=   Get From Dictionary    ${first_item}    line_total 

    Set Global Variable    ${SKU}       ${sku}
    Set Global Variable    ${QUANTITY}  ${qty}
    Set Global Variable    ${RATE}      ${rate}
    Set Global Variable    ${AMOUNT}    ${amount}






