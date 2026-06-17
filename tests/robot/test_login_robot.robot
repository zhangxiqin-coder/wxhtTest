*** Settings ***
Documentation    登录功能测试 - Robot Framework 示例
Library           SeleniumLibrary
Resource          ../resources/common_keywords.robot


*** Variables ***
${LOGIN_URL}      https://fangdong.fun/login
${DASHBOARD_URL}  https://fangdong.fun/rooms
${BROWSER}        Chrome
${TIMEOUT}        10


*** Test Cases ***
TC001_CorrectCredentials
    [Documentation]    正确用户名密码登录
    Open Browser To Login Page
    Input Username     testuser3
    Input Password     123456
    Click Login Button
    Wait Until Dashboard Displayed
    [Teardown]    Close Browser


TC002_WrongPassword
    [Documentation]    错误密码登录
    Open Browser To Login Page
    Input Username     testuser3
    Input Password     wrongpassword
    Click Login Button
    Wait Until Error Displayed    用户名或密码错误
    [Teardown]    Close Browser


TC003_EmptyUsername
    [Documentation]    空用户名时登录按钮不可点击
    Open Browser To Login Page
    Input Username
    Input Password     123456
    # 验证登录按钮不可点击（disabled状态）
    Element Should Be Disabled    xpath=//button[contains(text(), '登录')]
    [Teardown]    Close Browser


*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN_URL}    ${BROWSER}
    Set Selenium Implicit Wait    10s
    Set Selenium Speed    0.5s
    Maximize Browser Window


Input Username
    [Arguments]    ${username}=${EMPTY}
    Input Text    //input[@id='username']    ${username}


Input Password
    [Arguments]    ${password}=${EMPTY}
    Input Text    //input[@id='password']    ${password}


Click Login Button
    Click Button    //button[contains(text(), '登录')]


Wait Until Dashboard Displayed
    Wait Until Page Contains    房间管理
    Wait Until Element Is Visible    xpath=//*[contains(@class, 'el-table')]


Wait Until Error Displayed
    [Arguments]    ${expected_error}
    Wait Until Element Is Visible    xpath=//div[contains(@class, 'form-error')]
    Page Should Contain    ${expected_error}


Close Browser
    Close All Browsers