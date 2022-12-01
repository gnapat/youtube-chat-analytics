# Youtube-chat-analytics
The handling of data collection from social networks in different platforms is different. But good storage and categorization makes it easy to analyze data.
For a small project, it is an experiment to make a system to help manage data from YouTube chat, starting with data collecting, hot and cold storage, and preparing Datamart for data analytics.
- Data Collector.
- Data Management.
- GUI/Web base (Virtualization/Viewer).

Youtube link:https://youtu.be/Iv5k3dV1WTI
### Application Diagram
![image](https://user-images.githubusercontent.com/22583786/204675537-1e2309b0-b2c9-44c0-936f-978a01d8c6c6.png)

### Data Diagram
![image](https://user-images.githubusercontent.com/22583786/204730797-16e7b65a-1cc0-44cd-a386-5038715179ad.png)


## GUI/Web base (Virtualization/Viewer).

### YouTube Live Chat Viewer
![image](https://user-images.githubusercontent.com/22583786/204783912-8f6e7912-d57b-4788-8a6c-680721f9f45e.png)

## Feature
This application is developed in python language. So can understand the source code and can be easily tested.

Applications will be on
Graphice User interface (GUI) powered by PySimpleGUI Library.

Data storage and data manipulation using Create , Read ,Update, Delete (CRUD Oparation) uses MongoDB as the core.

### Required libraries
- Pandas
- numpy
- matplotlib
- pymongo
- PySimpleGUI
- Need install Anaconda3

### **Source code**
- src
  - viewer.py [GUI]
  - include
    - ychat_db.py [data management]

  
### **Step Installation and Run**

1. Python.exe –m venv \youtube-chat-analytics\
2. cd \youtube-chat-analytics\ 
3. Script\activate
4. Install pandas lib   -> pip install pandas
5. Install matplotlib   -> pip install matplotlib
6. Install pymongo lib -> pip install pymongo
7. Install PySimpleGUI lib -> pip install PySimpleGUI
8. Run python.exe .\src\viewer.py






