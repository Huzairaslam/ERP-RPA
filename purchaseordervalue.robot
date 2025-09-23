*** Settings ***
Library    JSONLibrary
Library    Collections
Library    RequestsLibrary

*** Variables ***
${BASE_URL}    http://0.0.0.0:8000/purchase_order

*** Keywords ***
Fetch Purchase Order Data
    [Documentation]    Call FastAPI endpoint and parse purchase order JSON
    Create Session    purchase    ${BASE_URL}
    ${response}=    GET On Session    purchase    /purchase_order
    ${status}=    Convert To String    ${response.status_code}
    Should Be Equal As Strings    ${status}    200

    ${json}=    To JSON    ${response.text}

    ${vendorname}=    Get Value From Json    ${json}    $.vendorname
    Set Global Variable    ${vendorname}    ${vendorname[0]}

    ${doc_date}=    Get Value From Json    ${json}    $.doc_date
    Set Global Variable    ${doc_date}    ${doc_date[0]}

    ${delivery_address}=    Get Value From Json    ${json}    $.delivery_address
    Set Global Variable    ${delivery_address}    ${delivery_address[0]}

    ${mobile_number}=    Get Value From Json    ${json}    $.mobile_number
    Set Global Variable    ${mobile_number}    ${mobile_number[0]}

    ${person_full_name}=    Get Value From Json    ${json}    $.person_full_name
    Set Global Variable    ${person_full_name}    ${person_full_name[0]}

    ${expected_date}=    Get Value From Json    ${json}    $.expected_date
    Set Global Variable    ${expected_date}    ${expected_date[0]}

    ${special_instruction}=    Get Value From Json    ${json}    $.special_instruction
    Set Global Variable    ${special_instruction}    ${special_instruction[0]}

    Log To Console    ✅ Vendor: ${vendorname}, Date: ${doc_date}, Address: ${delivery_address}
    Log To Console    📱 ${person_full_name} (${mobile_number})
    Log To Console    Expected: ${expected_date}, Note: ${special_instruction}
