*** Settings ***
Documentation    公共关键字库 - 可复用的测试关键字
Library           SeleniumLibrary


*** Keywords ***
Wait For Element
    [Arguments]    ${locator}    ${timeout}=10
    Wait Until Element Is Visible    ${locator}    ${timeout}


Wait For Element Clickable
    [Arguments]    ${locator}    ${timeout}=10
    Wait Until Element Is Enabled    ${locator}    ${timeout}
    Wait Until Element Is Visible    ${locator}    ${timeout}


Take Screenshot
    [Arguments]    ${filename}
    Capture Page Screenshot    ${filename}


Wait For Page Load
    [Documentation]    等待页面加载完成
    Sleep    2s


Verify Page Title
    [Arguments]    ${expected_title}
    Title Should Be    ${expected_title}


Verify URL
    [Arguments]    ${expected_url}
    Location Should Be    ${expected_url}


Verify Text Present
    [Arguments]    ${text}
    Page Should Contain    ${text}


Verify Element Present
    [Arguments]    ${locator}
    Element Should Be Visible    ${locator}


Clear Field
    [Arguments]    ${locator}
    Clear Element Text    ${locator}


Scroll To Element
    [Arguments]    ${locator}
    Execute JavaScript    arguments[0].scrollIntoView(true);    ${locator}


Highlight Element
    [Arguments]    ${locator}
    Execute JavaScript    arguments[0].style.border='3px solid red'    ${locator}


Wait And Click
    [Arguments]    ${locator}    ${timeout}=10
    Wait For Element Clickable    ${locator}    ${timeout}
    Click Element    ${locator}


Wait And Input
    [Arguments]    ${locator}    ${text}    ${timeout}=10
    Wait For Element    ${locator}    ${timeout}
    Clear Field    ${locator}
    Input Text    ${locator}    ${text}