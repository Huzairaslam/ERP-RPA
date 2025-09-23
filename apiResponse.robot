*** Settings ***
Library    RequestsLibrary
Library    JSONLibrary
Library    BuiltIn
Library    Collections

*** Variables ***
${BASE_URL}    http://api.rabtai.3em.tech/api/ProcessFile
${FILE_ID}     68c97be022721536ab3f9bb2

*** Keywords ***
Fetch API Data
    Create Session    api    ${BASE_URL}
    ${resp}=    GET On Session    api    /${FILE_ID}
    Should Be Equal As Integers    ${resp.status_code}    200

    ${json_data}=    To Json    ${resp.text}
    ${llm_response}=    To Json    ${json_data["data"]["llmResponse"]}

    ${header}=    Get From Dictionary    ${llm_response}    header
    Set Global Variable    ${DOC_TYPE}       ${header["doc_type"]}
    Set Global Variable    ${DOC_DATE}       ${header["doc_date"]}
    Set Global Variable    ${COMPANY}        ${header["company_name"]}
    Set Global Variable    ${INVOICE}        ${header["invoice_number"]}

    ${items}=    Get From Dictionary    ${llm_response}    items
    Set Global Variable    @{ITEMS}          ${items}

PRODUCTS INFORMATION
    [Documentation]    Extracts SKU, Qty, Rate, Amount from first item
    ${first_item}=    Get From List    ${ITEMS}    0
    ${sku}=    Get From Dictionary    ${first_item}    sku
    ${qty}=    Get From Dictionary    ${first_item}    quantity
    ${rate}=   Get From Dictionary    ${first_item}    rate
    ${amount}= Get From Dictionary    ${first_item}    amount

    Set Global Variable    ${SKU}       ${sku}
    Set Global Variable    ${QUANTITY}  ${qty}
    Set Global Variable    ${RATE}      ${rate}
    Set Global Variable    ${AMOUNT}    ${amount}
