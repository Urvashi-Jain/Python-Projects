from getpass import getpass
import os
import shelve
import sys
import time

def clear_screen():
  os.system('cls')
  
def menu():
  clear_screen()
  print("\n1. Login \n2. Signup \n3. Remove Account \n4. Admin \n5. Exit")
  user_input = int(input("\nSelect option: "))
  if user_input == 1:
    login()
  elif user_input == 2:
    signup()
  elif user_input == 3:
    remove_account()
  elif user_input == 4:
    admin()
  elif user_input == 5:
    exit()

def login():
  clear_screen()
  acc_no = input("\nEnter account no: ")
  username = input("\nEnter username: ")
  password = getpass("\nEnter password: ")
  with shelve.open('users.db') as db:
    if acc_no in db:
      if db[acc_no]['Username'] == username:
        if db[acc_no]['Password'] == password:
          print("\n\n",db[acc_no])
          submenu(acc_no)
        else:
          print("\nPassword Incorrect. Please try again")
          time.sleep(2)
          menu()
      else:
        print("\nUsername is incorrect")
        time.sleep(2)
        menu()
    else:
      print("\nNo such account exists")
      time.sleep(2)
      menu()
  db.close()
  
def submenu(acc_no):
  print("\n1. Debit balance \n2. Credit balance \n3. Show balance \n4. Update account details \n5. Logout")
  login_input = int(input("\nSelect option: "))
  if login_input == 1:
    debit_balance(acc_no)
  elif login_input == 2:
    credit_balance(acc_no)
  elif login_input == 3:
    show_balance(acc_no)
  elif login_input == 4:
    update_account(acc_no)
  elif login_input == 5:
    menu()
    
def debit_balance(acc_no):
  with shelve.open('users.db', writeback=True) as db:
    print(f"\nCurrent balance: {db[acc_no]['Balance']}")
    debit_balance = int(input("\nEnter debit balance: "))
    if db[acc_no]['Balance']>debit_balance:
      db[acc_no]['Balance'] = db[acc_no]['Balance'] - debit_balance
      print(f"\nBalance successfully updated --> {db[acc_no]['Balance']}")
      time.sleep(2)
    else:
      print("\nOOPS! You have insufficient balance.")
      time.sleep(2)
  db.close()
  clear_screen()
  submenu(acc_no)
      
def credit_balance(acc_no):
  with shelve.open('users.db', writeback=True) as db:
    print(f"\nCurrent balance: {db[acc_no]['Balance']}")
    credit_balance = int(input("\nEnter credit balance: "))
    db[acc_no]['Balance'] = db[acc_no]['Balance'] + credit_balance
    print(f"\nBalance successfully updated --> {db[acc_no]['Balance']}")
  time.sleep(2)
  db.close()
  clear_screen()
  submenu(acc_no)
      
def show_balance(acc_no):
  with shelve.open('users.db') as db:
      print(f"\nCurrent account balance --> {db[acc_no]['Balance']}")
      time.sleep(2)
  db.close()
  clear_screen()
  submenu(acc_no)
  
def update_account(acc_no):
  clear_screen()
  print("\nWhat do you want to update?  \n\n1. Username \n2. Password \n3. Email ID \n4. Mobile No \n5. Back to previous menu")
  update_input = int(input("\nSelect option: "))
  with shelve.open('users.db',writeback=True) as db:
    if update_input == 1:
      username = input("\nEnter username: ")
      db[acc_no]['Username'] = username
      print("\nUsername updated successfully")
    elif update_input == 2:
      password = getpass("\nEnter password: ")
      db[acc_no]['Password'] = password
      print("\nPassword updated successfully")
    elif update_input == 3:
      eid = input("\nEnter email id: ")
      db[acc_no]['Email ID'] = eid
      print("\nEmail ID updated successfully")
    elif update_input == 4:
      mobile_no = input("\nEnter mobile number: ")
      db[acc_no]['Mobile No'] = mobile_no
      print("\nMobile Number updated successfully")
    elif update_input == 5:
      clear_screen()
      submenu(acc_no)
  time.sleep(2)
  db.close()
  clear_screen()
  submenu(acc_no)
  
def signup():
  clear_screen()
  username = input("\nEnter username: ")
  password = getpass("\nEnter password: ")
  eid = input("\nEnter email id: ")
  balance = eval(input("\nEnter initial amount: "))
  mobile_no = input("\nEnter 10 digit mobile number: ")
  if len(mobile_no)==10:
    pass
  else:
    mobile_no = input("\nPlease enter 10 digit mobile number: ")
  with shelve.open('users.db',writeback=True) as db:
    account_no = list(map(int,db.keys()))
    account_no.sort(reverse=True)
    try:
      new_account_no = str(account_no[0]+1)
    except:
      new_account_no = '1001'
    db[new_account_no] = {
    'Username' : username,
    'Password' : password,
    'Email ID' : eid,
    'Balance' : balance,
    'Mobile No' : mobile_no
    }
    db.close()
    print(f"\n{username} added successfully with Account No : {new_account_no} \n\nLogin again with your credentials.")
    time.sleep(2)
    menu()
    
def remove_account():
  clear_screen()
  acc_no = input("\nEnter account number: ")
  with shelve.open('users.db', writeback = True) as db:
    if acc_no in db:
      del db[acc_no]
      print(f"\nAccount removed successfully")
    else:
      print("\nNo such account exists!!")
  db.close()
  time.sleep(2)
  menu()
  
def admin():
  clear_screen()
  with shelve.open('users.db') as db:
    for key, value in db.items():
      print()
      print(f"{key}\n")
      for k,v in value.items():
        print(f"{k} : {v}")
  db.close()
  print("\n\n1. Update details \n2. Back to main menu")
  a_input = int(input("\nSelect option: "))
  if a_input == 1:
    admin_input()
  elif a_input == 2:
    menu()
  
def admin_input():
  clear_screen()
  print("\n\n1. Update account \n2. Remove Account \n3. Back to admin page")
  admin_input = int(input("\nSelect any option: "))
  if admin_input == 1:
    update_account_admin()
  elif admin_input == 2:
    remove_account_admin()
  elif admin_input == 3:
    admin()
    
    
def update_account_admin():
  clear_screen()
  print("\nWhat do you want to update?  \n\n1. Username \n2. Password \n3. Email ID \n4. Mobile No \n5. Balance")
  update_input = int(input("\nSelect option: "))
  with shelve.open('users.db',writeback=True) as db:
    acc_no = input("\nEnter account number: ")
    if update_input == 1:
      username = input("\nEnter username: ")
      db[acc_no]['Username'] = username
      print("\nUsername updated successfully")
    elif update_input == 2:
      password = getpass("\nEnter password: ")
      db[acc_no]['Password'] = password
      print("\nPassword updated successfully")
    elif update_input == 3:
      eid = input("\nEnter email id: ")
      db[acc_no]['Email ID'] = eid
      print("\nEmail ID updated successfully")
    elif update_input == 4:
      mobile_no = input("\nEnter mobile number: ")
      db[acc_no]['Mobile No'] = mobile_no
      print("\nMobile Number updated successfully")
    elif update_input == 5:
      balance = eval(input("\nEnter balance: "))
      db[acc_no]['Balance'] = balance
      print("\nBalance updated successfully")
  db.close()
  admin_input()
  
def remove_account_admin():
  clear_screen()
  acc_no = input("\nEnter account number: ")
  with shelve.open('users.db', writeback = True) as db:
    if acc_no in db:
      del db[acc_no]
      print(f"\nAccount removed successfully")
    else:
      print("\nNo such account exists!!")
  db.close()
  time.sleep(2)
  admin()
  
    
def exit():
  clear_screen()
  sys.exit()
    
clear_screen()
menu()
