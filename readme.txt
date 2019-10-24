FEATURES LAYOUT:
  [✔] 0 MongoDB integration
  [✔] 1 Login cabability
  [✘] 1.1 Login Form
  [✘] 1.2 Make the relationship users->accounts->cases
  [✔] 2 List accounts
  [✘] 3 Register new accounts (form)
  [✔] 4 See all my cases
  [✘] 5 Run case scripts
  [✘] 5.1 Import scripts and configs
  [✘] 5.2 Broadcast output
  [✘] 6 Run scheduled case scripts


VIEWS LAYOUT:\r\n
  [✔] Flow: debug view
  [✘] Login
  [✔] Main page: list of users for admin or redirect to own Profile
  [✔] Account
  [✔] Case channel - live output
  [✔] About
  [✘] Extendable Base Page for {% extends %}



The dashboard controls a database of accounts on various platforms. 
Scripts are run on a schedule for each account, with output channeled live to the dashboard.



Python 3.6
Django 2.2
Djongo
MongoDB
Redis for messaging