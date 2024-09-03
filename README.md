# CAMS Biometric Integration with ERPNext

## Introduction

Integrating the CAMS biometric system with ERPNext enables real-time attendance tracking and automated data synchronization. This integration allows you to efficiently capture and manage punch logs directly from your biometric devices, ensuring accurate and up-to-date attendance records.

By setting up this integration, you can streamline your attendance processes, minimize manual data entry, and enhance overall accuracy in tracking employee time. The integration ensures that punch data from CAMS biometric devices is seamlessly transferred to ERPNext, where it is recorded in real-time, helping you maintain a reliable attendance management system.

## 1. Setup and Configuration

### 1.1 CAMS Biometric Settings

1.  **Service Tag ID and Auth Token:**
    
    -   After acquiring an account with CAMS, you will receive a `Service Tag ID` and `Auth Token`.
    -   These credentials are crucial for configuring the CAMS unit and integrating it with ERPNext.
    - Fill those details in the respective field in the cams biometric settings doctype.


### 1.2 CAMS Unit Configuration

1.  **Callback URL Setup:**
    
    -   CAMS operates there own server, where punches are recorded, and to ensure proper integration, you need to provide a callback URL.
    -   In our app, we have a function called attendance ,for handling attendance data. Our URL will generally follow this format:     
        `/api/method/navari_cams_biometric.cams_biometric.controllers.cams_call.attendance` 
        
    -   Example URL:      
        `https://banadir.erpnext.com/api/method/navari_cams_biometric.cams_biometric.controllers.cams_call.attendance` 
        
    -   Copy this API endpoint.
2.  **API Configuration in CAMS:**
    Log into your [cams unit](https://camsunit.com/#) account
    -   Access the CAMS unit’s API settings.
    -   Paste the copied API URL into the Callback Url field to configure the callback URL.
    
3.  **Punching Data:**
    -   Once the callback API is set up, you can use the biometric device to record employee punches.
    -   Each punch event will be sent to ERPNext, where it will be logged in the Employee Check-in records.

### 1.3 Employee Configuration

1.  **Biometric ID Mapping:**
    -   Each employee must be assigned a unique biometric ID in the ERPNext system.
    -   It is recommended that this ID closely resembles the employee’s system ID for consistency.
    -   Ensure that each employee’s biometric ID is accurately mapped to their profile in ERPNext.
    
2.  **Shift Assignment:**
    -   Assign appropriate shifts to each employee to facilitate automatic attendance marking.
    -   This step is crucial for ensuring that the attendance system functions correctly, as it relies on shift data to log employee punch times accurately.

## 2. Key Points to Remember

-   **Attendance Marking:**
    -   The biometric punch data will update the Employee Check-in records.
    -   The date of the last synchronization from the attached shift will be updated with the latest punch log.
-   **Regular Syncing:**
    -   Regularly verify and synchronize punch logs to ensure accurate attendance records.
-   **Employee Records:**
    -   Accurate mapping of biometric IDs and shift assignments is vital for correct attendance tracking and reporting.
    
    2.  **Fetching Punch Logs:**
    - INcase whewre you want to retrieve old/historical punchlogs, we have a feature on cams biometric settings. 
    -  To retrieve punch logs, navigate to the CAMS Biometric Settings in ERPNext.
    -   Enter the `Start Date` and `End Date` fields to specify the range for the punch logs.
    -   Click on `Load Punchlog` to fetch the attendance records. Note that this feature is available depending on your CAMS subscription plan.