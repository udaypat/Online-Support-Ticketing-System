# Online Ticketing System

This project aims to create an online support ticket system, which will help the support team manage student queries and concerns efficiently. The system will allow students to create support tickets for their specific concerns or queries, and before creating a ticket, they will be shown a list of similar tickets to avoid duplicity. Additionally, the system will enable students to like or +1 an existing support ticket, allowing popular concerns or queries to be prioritized by the support team. After addressing the concern, the support team can mark the ticket as resolved, and concerned users will receive appropriate notifications.

The system will also feature dynamic FAQ updation, where student concerns that can serve as FAQs will be added to the FAQ section by support admins, along with categorization for easy access by future students. The platform will allow users to enroll as students, support staff, and admins, with additional features to add value to users.


### Features

- 🖥️ Standalone Flask API Server
- 🌐 Single Page APP(SPA) using Vue
- 📲 Can be installed as PWA on Android or iOS
- 🔐 JWT Auth
- 🔔 Email Notifications when closing and assigning tickets
- 👤 Three Different types of dashboard for Admin, Support and Student
- 📄 Swagger UI Documentation for API

## Steps to start Backend server  
Step 1:  
• CD to `code/backend/smartSupport` directory.

Step 2:  
• Run `pip install requirements.txt` or  
`pip3 install requirements.txt` to install all dependencies  

Step 3:  
• Run `python main.py` or `python3 main.py`  

 
### Mailhog installation guide  

####  To start MailHog server run:  
• `~/go/bin/MailHog`  
or  
• `go/bin/MailHog` 

Refer: https://github.com/mailhog/MailHog


## Steps to start Frontend server  
For project setup run:  
`npm install`  

To start Server run:  
`npm run serve`  

To compile and minify for production run:  
`npm run build`
