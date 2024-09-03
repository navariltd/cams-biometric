# CAMS Biometric Integration with FrappeHR

## Introduction
![checkin](https://github.com/user-attachments/assets/57857c26-a164-4f28-8c60-e7a4bcb4a67e)

Integrating the [CAMS biometric system](https://camsunit.com/application/biometric-web-api.html) with FrappeHR enables real-time attendance tracking and automated data synchronization. This integration allows you to efficiently capture and manage punch logs directly from your biometric devices, ensuring accurate and up-to-date attendance records.

By setting up this integration, you can streamline your attendance processes, minimize manual data entry, and enhance overall accuracy in tracking employee time. The integration ensures that punch data from CAMS biometric devices is seamlessly transferred to FrappeHR, where it is recorded in real-time, helping you maintain a reliable attendance management system.

## 1. Setup and Configuration

### 1.1 CAMS Biometric Settings

1.  **Service Tag ID and Auth Token:**
    
    -   After acquiring an account with CAMS, you will receive a `Service Tag ID` and `Auth Token`.
    -   These credentials are crucial for configuring the CAMS unit and integrating it with FrappeHR.
    - Fill those details in the respective field in the cams biometric settings doctype.
![cams biometric setting](https://github.com/user-attachments/assets/66520601-edfa-49bf-9af6-2f9602f57256)


### 1.2 CAMS Unit Configuration

1.  **Callback URL Setup:**
    
    -   CAMS operates there own server, where punches are recorded, and to ensure proper integration, you need to provide a callback URL.
    -   In our app, we have a function called attendance ,for handling attendance data. Our URL will generally follow this format:     
        `{site}/api/method/navari_cams_biometric.cams_biometric.controllers.cams_call.attendance` 
  
    -   Copy this API endpoint and remember to replace the {site} with your subdomain.     
      For Example if your site is https://example.erpnext.com then the link will be:      
        `https://example.erpnext.com/api/method/navari_cams_biometric.cams_biometric.controllers.cams_call.attendance` 
      
2.  **API Configuration in CAMS:**
    Log into your [cams unit](https://camsunit.com/#) account
    -   Access the CAMS unit’s API settings.
    -   Paste the copied API URL into the Callback Url field.
    ![cam sunit](https://github.com/user-attachments/assets/a34b2f24-e3fd-4bf8-a710-4bc5db522630)

3.  **Punching Data:**
    -   Once the callback API is set up, you can use the biometric device to record employee punches.
    -   Each punch event will be sent to FrappeHR, where it will be recorded in the Employee Check-in records.

### 1.3 Employee Configuration

1.  **Employee Biometric ID Mapping:**
    -   Each employee must be assigned a unique biometric ID in the FrappeHR system, similar to the one registered in the cams device.
    -   It is recommended that this ID closely resembles the employee’s system ID for consistency.
    -   Since you have registered the employee on cam device, get the same id and fill it in the Attendance/biometric ID field on Employee doctype
    ![shifts](https://github.com/user-attachments/assets/0118e33f-dad1-4027-92da-694ab162d69a)

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

**Fetching Historical Punch Logs:**
    - In case where you want to retrieve old/historical punch logs, we have a feature on cams biometric settings doctype. 
    -  To retrieve punch logs, navigate to the CAMS Biometric Settings in FrappeHR.
    -   Enter the `Start Date` and `End Date` fields to specify the range for the punch logs.
    -   Click on `Load Punchlog` to fetch the attendance records. So that you know, this feature is available depending on your CAMS subscription plan.

## Installation Process
### Manual/Self-Hosted Installation

1. [Install bench](https://github.com/frappe/bench)


2. [Install ERPNext](https://github.com/frappe/erpnext#installation)

3. [Intsall FrappeHr](https://github.com/frappe/hrms#installation)

    

4. Once bench, ERPNext and FrappeHR are installed, add navari_cams_biometric to your bench by running:

  
```sh


$  bench  get-app  --branch  {branch-name}  https://github.com/navariltd/navari_cams_biometric.git

```


Replace `{branch-name}` with the desired branch name from the repository. Ensure compatibility with your installed versions of Frappe, ERPNext and Frappe HR.


5. Install the navari_cams_biometric app on your site by running:


```sh

$  bench  --site  {sitename}  install-app navari_cams_biometric

```

Replace `{sitename}` with the name of your site.

  

### Frappe Cloud Installation

- Sign up with Frappe Cloud.

- Setup a [bench](https://frappecloud.com/docs/benches/create-new).

- Create a new site.

- Choose Frappe Version-14/Version-15 or above, and select ERPNext, Frappe HR, and Cams Biometric from the available Apps to Install.

- Within minutes, the site will be up and running with a fresh install, ready to explore the app's simple and impressive features.
  

If assistance is needed to get started, reach out for consultation and support from: [Navari](https://navari.co.ke/).
