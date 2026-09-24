*** Settings ***
Documentation    Test cases for lunar-client snap
Resource         kvm.resource


*** Test Cases ***
Lunar Client Launches And Renders
    [Documentation]    Verify lunar-client snap launches and renders a UI on Mir
    [Tags]    smoke    yarf:certification_status: blocker
    Log Screenshot
