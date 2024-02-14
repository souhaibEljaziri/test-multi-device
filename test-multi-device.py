from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
import time 
import re
import requests
from datetime import datetime
def currentact():
    current_activity = driver.current_activity
    current_package = driver.current_package
    print(current_activity)

# time.sleep(10)

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['deviceName'] = 'sdk_gphone64_x86_64'
desired_caps['udid'] = 'emulator-5554'  # Device ID
desired_caps['appPackage'] = 'com.logistics.rider.talabat'
desired_caps['appActivity'] = 'com.roadrunner.login.presentation.router.RouterActivity'
desired_caps['autoGrantPermissions'] = True  # auto grant permissions
desired_caps['noReset'] = True  # don't stop the app between sessions
# desired_caps["headless"]= True  # Enable headless mode
# desired_caps['fullReset'] = True  # enable full reset if needed
desired_caps['newCommandTimeout'] = 3600 * 24 * 7
desired_caps["automationName"]= "uiautomator2"
driver = webdriver.Remote('http://localhost:4723', desired_caps)
worker={"name":"", "balance":"","distance":"","nb DDeliveries":"","tips":"","stat":""}
#####################################################################""""""""""
token_url = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/get-token'
token_params = {'secret': '5b6856c4126d155f1412d68bfed01058'}
delete_url = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/deleteworker'

#####################################################################""""""""""

# data = [
#     {'email': 'naba7128@talabat.com', 'password': 'Temp@123'},
#     {'email': '96557550499@deliveryhero.com', 'password': 'Shabeer@4452'}
# ]
###################################### Your test code here

time.sleep(11)
y=-1
m=0
sq=0
while True:
   y=y+1
   oki = True
   while oki:
    try:
        token_response = requests.post(token_url, params=token_params)
        token_data = token_response.json()

        access_token = token_data['data']['access_token']
#
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        api_url = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/getworkers'
        response = requests.get(api_url, headers=headers)
        
        workers_data = response.json()
        data = []

        for worker in workers_data["data"]:
            email = worker['email']
            password = worker['passmail']
            version = worker["version"]
            id_company = worker["id_company"]
            id_a = worker["id"]
            if (version == '2'):
                data.append({'email': email, 'password': password, 'id_company':id_company,"id":id_a})
        oki= False 
    except:
        pass
   print("data : ")
   print(data)

   for p in data:
    ok=True
    while ok :
        try:
                if m>10:
                    try:
                    ##refresh 
                        driver.quit()
                        driver = webdriver.Remote('http://localhost:4723', desired_caps)
                        time.sleep(11)
                        m=0
                    except:
                        driver = webdriver.Remote('http://localhost:4723', desired_caps)
                        time.sleep(11)
                        m=0
                if y==0:
                    time.sleep(5)
                elif y<3:
                    time.sleep(3)
                else:
                    time.sleep(0.5)
                worker = {}
                worker["id"]=p["id"]
                worker['email'] = p['email']
                worker['passmail'] = p['password']
                worker["id_company"]  = p["id_company"]
                # Wait for the element to be visible
                email_field = driver.find_element(MobileBy.ID, 'com.logistics.rider.talabat:id/text_input_edit_text')
                # Clear the existing input
                email_field.clear()
                # Enter a new input
                email_field.send_keys(worker['email'])
                # Identify the password field and enter the passwordandroid.widget.EditText
                password_field = driver.find_elements(MobileBy.ID, "com.logistics.rider.talabat:id/text_input_edit_text")[1]
                # Let's assume the first field is the username and the second one is the password
                password_field.clear()
                
                password_field.send_keys(worker['passmail']) 

                # Find the button login button 
                button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Sign in"]')
                # Click the button
                button.click()

                print(str(y)+"==================================")

                try:
                        time.sleep(1)
                        button = driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='OK']")
                        # Click the button
                        button.click()
                        print("login error not passed ")
                        ###
                        delete_params = {'email': worker['email']}
                        delete_response = requests.get(delete_url, params=delete_params, headers=headers)
                        if delete_response.status_code == 200:
                            print("Worker with email "+str(worker["email"])+" deleted successfully.")
                            notification_url = "http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/notification"
                            notificationobj = {
                                "content":"Worker with email "+str(worker["email"])+" deleted successfully.",
                                "id_company":worker['id_company'],
                                "is_read":0,
                                "url":"http://thedriv1.wwwaz1-ts109.a2hosted.com/public/admin/worker17"
                            }
                            token_response = requests.post(notification_url, params=notificationobj, headers=headers)
                            token_data = token_response.json()
                            print("company with id "+str(worker['email'])+"notifyd")
                        else:
                            print("Failed to delete worker with email "+str(worker["email"])+". Status code: "+str(delete_response.status_code))
                        
                        ###
                        data = [item for item in data if item != p]
                        print(data)
                        break
                except:
                        print('i passed login')

                if y==0 :
                    time.sleep(15)
                elif y<3:
                    time.sleep(5)
                else:
                    time.sleep(3)
                #################steeep1  search for the balance 
                #############update 
                try:
                    button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='Skip for later']")
                    # Click the button
                    button.click()
                    print("there is an update ")
                except:
                    print("there is no update")
                ########################
                
                # Find the button login button 
                button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Wallet"]')
                # Click the button
                button.click()
                if y==0:
                    time.sleep(10)
                elif y<3:
                    time.sleep(3)
                else:
                    time.sleep(1)

                # Wait for the element to be visible
                element = driver.find_element(MobileBy.ID, 'com.logistics.rider.talabat:id/tvBalance')

                # Extract the text from the element
                text = element.text
                worker['balance']=text

                ##STATUS
                button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Home"]')
                # Click the button
                button.click()

                time.sleep(1)

                size = driver.get_window_size()
                start_x = size['width'] // 2
                start_y = int(size['height'] * 0.8)
                end_y = int(size['height'] * 0.2)
                actions = TouchAction(driver)
                actions.press(x=start_x, y=start_y)
                actions.wait(500)  # wait for 1 second
                actions.move_to(x=start_x, y=end_y)
                actions.release()
                actions.perform()
                if y==0:
                    time.sleep(3)
                
                text_views = driver.find_elements(MobileBy.CLASS_NAME, "android.widget.TextView")
                worker["stat"]=""
                for text_view in text_views:
                    text = text_view.text
                    if text == "Orders paused":
                        # Do something when text is "Orders paused"
                        worker["stat"]='<div style="width: 65%; height: 20px; border-radius: 10%; margin: 10px; background-color: #ff9900; text-align: center;">Orders paused</div>'
                        break
                    elif text == "Working" or text == "Ready" or text == "Online":
                        # Do something when text is "Working"
                        worker["stat"]='<div style="width: 65%; height: 20px; border-radius: 10%; margin: 10px; background-color: #2ecc71; text-align: center;">working</div>'
                        break
                    elif text == "On paid pause":
                        worker["stat"]='<div style="width: 65%; height: 20px; border-radius: 10%; margin: 10px; background-color: #ff9900; text-align: center;">On paid pause</div>'
                        # Do something when text is "On paid pause"
                        break
                    elif text == "Not Working" or text =="Offline":
                        worker["stat"]='<div style="width: 65%; height: 20px; border-radius: 10%; margin: 10px; background-color: #ff6347; text-align: center;">not working</div>'
                        # Do something when text is "Not working"
                        break
                


                #################steeep2 search for the numbre of delvrs and other data
                # Find the button login button 
                button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="History"]')
                # Click the button
                button.click()

                if y==0:
                    time.sleep(10)
                elif y<3:
                    time.sleep(3)
                else:
                    time.sleep(1)

                # Wait for the elements to be visible
                elements = driver.find_elements(MobileBy.ID, 'com.logistics.rider.talabat:id/layout_tile_title')

                # Iterate over the elements and extract their text values
                i=0
                for element in elements:
                    i+=1
                    text = element.text
                    if len(elements)==4:
                        if i==1:
                            worker['distance']=text
                        elif i==2:
                            worker['nb DDeliveries']=text
                        elif i==3:
                            worker['tips']=text
                        else:
                            worker['collected']= text
                    elif len(elements)==3:
                        if i==1:
                            worker['distance']=text
                        elif i==2:
                            worker['nb DDeliveries']=text
                        else:
                            text=text.replace('kd', '')
                            try:
                                text=float(text.replace(' ',''))
                            except:
                                worker['tips']="0"
                                worker['collected']= "0"
                                pass
                            if text<2:
                                worker['tips']= str(text)
                                worker['collected']="0"
                            else:
                                worker['collected']= str(text)
                                worker['tips']= "0"

                    else:
                        if i==1:
                            worker['distance']=text
                        else:
                            worker['nb DDeliveries']=text
                            worker['collected']= "0"
                            worker['tips']="0"


                # Find the menu button |||
                element = driver.find_element(MobileBy.ID,'com.logistics.rider.talabat:id/imageViewStartIcon')
                # Click the element
                element.click()

                time.sleep(1)
                # Find the menu button |||
                element = driver.find_elements(MobileBy.CLASS_NAME, 'android.widget.TextView')
                vff=0
                for el in element:
                    if el.text.isnumeric():
                        if 0<=int(el.text)<=6:
                            vff=1
                            element=el
                            break
                if vff == 0 :
                    element=0
                print("LV : "+str(element.text))
                worker["lv"]=str(element.text)
                ############################################ the worker seasons durition and number of seasons
                if False :
                    time.sleep(1)
                    button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Your sessions"]')
                    # Click the button
                    button.click()

                    if y==0:
                        time.sleep(15)
                    else:
                        time.sleep(6)

                    elements = driver.find_elements(MobileBy.CLASS_NAME, 'android.widget.TextView')
                    ok1=False
                    ok2=False
                    worker["sessions"]=""
                    worker["duration"]=""
                    for element in elements:
                        if "Sessions" in str(element.text) and worker["sessions"]=="":
                            ok1=True
                        if ok1==True and str(element.text).isdigit() :
                            if str(element.text).isdigit() <16 :
                                ok1=False
                                print("sessions : "+str(element.text))
                                worker["sessions"]=str(element.text)
                        if "Duration" in str(element.text) and worker["duration"]=="":
                            ok2=True
                        if ok2==True and "h" in str(element.text) :
                                ok2=False
                                print("duration : "+str(element.text))
                                worker["duration"]=str(element.text)
                    element = driver.find_element(MobileBy.ID,'com.logistics.rider.talabat:id/imageViewStartIcon')
                    # Click the element
                    element.click()
                    # Find the menu button |||
                    element = driver.find_element(MobileBy.ID,'com.logistics.rider.talabat:id/imageViewStartIcon')
                    # Click the element
                    element.click()
                else:
                    worker["sessions"]=""
                    worker["duration"]=""                    
                ############################################
                if y==0:
                    time.sleep(10)
                else:
                    time.sleep(2)


                # # Wait for the element to be visible
                # element = driver.find_element(MobileBy.ID, 'com.logistics.rider.talabat:id/tvUsername')

                # # Extract the text from the element
                # text = element.text
                # worker['name']=text

                
                try:
                    # Find the menu button 
                    element = driver.find_element(MobileBy.XPATH,'//android.widget.TextView[@text="Logout"]')
                    # Click the element
                    element.click()
                except:
                    if y==0:
                        time.sleep(5)
                    else:
                        time.sleep(2)
                    size = driver.get_window_size()
                    start_x = size['width'] // 2
                    start_y = int(size['height'] * 0.8)
                    end_y = int(size['height'] * 0.2)
                    actions = TouchAction(driver)
                    actions.press(x=start_x, y=start_y)
                    actions.wait(500)  # wait for 1 second
                    actions.move_to(x=start_x, y=end_y)
                    actions.release()
                    actions.perform()

                    # Find the menu button 
                    element = driver.find_element(MobileBy.XPATH,'//android.widget.TextView[@text="Logout"]')
                    # Click the element
                    element.click()
                
                if y==0:
                    time.sleep(4)
                else:
                    time.sleep(0.4)
                # Find the button logout button
                try: 
                    button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='LOGOUT']")
                except:
                    button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='Logout']")
                # Click the button
                button.click()
                print("hello1")
                try:
                    print(worker)
                except:
                    print('hello2')
                print('hello3')
                ###########################################

                # API endpoint URL
                api_postwallet = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/postwallet'
                random_string = worker['balance']
                # Data to send in the request body
                # Define a regular expression pattern to match the prices
                price_pattern = r'\b\d+(?:\.\d+)? '
                # Find all matches of the pattern in the string
                if random_string!="0":
                    prices = re.findall(price_pattern, random_string)
                else:
                    prices =["0"] 
                if "-" in worker['balance']:
                    wllt = {
                    "id_worker": worker["id"],
                    "amount": 0.0-float(prices[0]),
                    }
                else:
                    wllt = {
                    "id_worker": worker["id"],
                    "amount": float(prices[0]),
                    }

                # Send the POST request
                response = requests.post(api_postwallet, json=wllt, headers=headers)



                # API endpoint URL & sending the sessions and duration 
                api_posttips = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/updateweekstats'
                s1 = {
                    "id_worker": worker["id"],
                    "numberofsection": worker["sessions"],
                    "duration": worker["duration"],
                }
                # Send the POST request
                response = requests.post(api_posttips, json=s1, headers=headers)
                print("updated week status")
                # API endpoint URL
                api_posttips = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/updatelvl'
                s2 = {
                    "id": worker["id"],
                    "level": worker["lv"],
                }
                # Send the POST request
                response = requests.post(api_posttips, json=s2, headers=headers)
                print("updated lvl")

                # API endpoint URL
                api_posttips = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/posttips'
                tps = {
                    "id_worker": worker["id"],
                    "amount": worker["tips"],
                }
                # Send the POST request
                response = requests.post(api_posttips, json=tps, headers=headers)

                ##update delevry numbre and amount and km and status

                current_date = datetime.now()
                # Format the date as yyyy/mm/dd
                formatted_date = f"{current_date.year}/{current_date.month}/{current_date.day}"

                api_url = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/getdeliveries'
                worker_data = {
                    
                    "date": formatted_date,         
                    "id_worker": worker["id"]  

                }
                response = requests.get(api_url, json=worker_data, headers=headers)
                print(formatted_date)
                if response.status_code == 200:
                    donnees = response.json()  # Convert the response to JSON
                    print(donnees)
                    delivery_data = donnees.get('data')
                    
                    if len(delivery_data)==0:
                        print("creating data numbre and amount and km and status ")
                        api_url = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/postdeleveryscrapping'
                        worker_data = {
                            "date": formatted_date,         
                            "id_worker": int(worker["id"])  ,
                            "kilometrage":worker["distance"],
                            "number":worker["nb DDeliveries"],
                            "status":worker["stat"]
                        }
                        response = requests.post(api_url, json=worker_data, headers=headers)
                        if response.status_code!= 200 :
                            print("sending errour post scrapping")
                    else:
                        print("updating data numbre and amount and km and status ")
                        api_url = 'http://thedriv1.wwwaz1-ts109.a2hosted.com/public/api/putdeliveryscrapping'
                        worker_data = {
                            "amount":worker["collected"],
                            "date": formatted_date, 
                            "id": int(delivery_data[0]["id"]) ,  
                            "id_worker": int(worker["id"])  ,
                            "kilometrage":worker["distance"],
                            "number":worker["nb DDeliveries"],
                            "status":worker['stat']
                        }
                        response = requests.post(api_url, json=worker_data, headers=headers)
                        if response.status_code!= 200 :
                            print("sending errour put scrapping")



                ###########################################
                ok=False  
                sq=sq+1
                print(str(sq)+" sq nember \n")
                if sq==2:
                    driver.quit()
                    driver = webdriver.Remote('http://localhost:4723', desired_caps)
                    sq=0


        except Exception as e:
                # print(f"An error occurred: {str(e)}")
                try:
                    # Find the button login button 
                    button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Wallet"]')
                    # Click the button
                    button.click()
                    time.sleep(4)
                    # Find the menu button |||
                    element = driver.find_element(MobileBy.ID,'com.logistics.rider.talabat:id/imageViewStartIcon')
                    # Click the element
                    element.click()

                    if y==0:
                        time.sleep(20)
                    else:
                        time.sleep(2)


                    size = driver.get_window_size()
                    start_x = size['width'] // 2
                    start_y = int(size['height'] * 0.8)
                    end_y = int(size['height'] * 0.2)
                    actions = TouchAction(driver)
                    actions.press(x=start_x, y=start_y)
                    actions.wait(500)  # wait for 1 second
                    actions.move_to(x=start_x, y=end_y)
                    actions.release()
                    actions.perform()
                    if y==0:
                        time.sleep(3)
                    
                    # Find the menu button 
                    element = driver.find_element(MobileBy.XPATH,'//android.widget.TextView[@text="Logout"]')
                    # Click the element
                    element.click()
                    if y==0:
                        time.sleep(4)
                    else:
                        time.sleep(1)
                    # Find the button logout button 
                    try: 
                        button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='LOGOUT']")
                    except:
                        button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='Logout']")
                    # Click the button
                    button.click()
                except:
                    try:
                        button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='Skip for later']")
                            # Click the button
                        button.click()
                        # Find the button login button 
                        button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Wallet"]')
                        # Click the button
                        button.click()
                        time.sleep(4)
                        # Find the menu button |||
                        element = driver.find_element(MobileBy.ID,'com.logistics.rider.talabat:id/imageViewStartIcon')
                        # Click the element
                        element.click()

                        if y==0:
                            time.sleep(20)
                        else:
                            time.sleep(2)

                        size = driver.get_window_size()
                        start_x = size['width'] // 2
                        start_y = int(size['height'] * 0.8)
                        end_y = int(size['height'] * 0.2)
                        actions = TouchAction(driver)
                        actions.press(x=start_x, y=start_y)
                        actions.wait(500)  # wait for 1 second
                        actions.move_to(x=start_x, y=end_y)
                        actions.release()
                        actions.perform()
                        if y==0:
                            time.sleep(3)
                        
                        # Find the menu button 
                        element = driver.find_element(MobileBy.XPATH,'//android.widget.TextView[@text="Logout"]')
                        # Click the element
                        element.click()
                        if y==0:
                            time.sleep(4)
                        else:
                            time.sleep(1)
                        # Find the button logout button 
                        button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='LOGOUT']")
                        # Click the button
                        button.click()
                    except:
                        try:
                            # Find the menu button 
                            element = driver.find_element(MobileBy.ID,'com.logistics.rider.talabat:id/imageViewStartIcon')
                            # Click the element
                            element.click()
                        except:
                            try:
                                #add 15 min wait 
                                button = driver.find_element(MobileBy.XPATH, '//android.widget.Button[@text="Remaining time"]')
                                button.click()
                                time.sleep(1)
                                button = driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="20+ minutes"]')
                                button.click()
                                time.sleep(1)
                                button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='Confirm']")
                                button.click()
                            except:
                                try:
                                    button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='OK']")
                                    # Click the button
                                    button.click()
                                except:

                                    m=m+1
                                    print(str(m)+" m nmber error")
                                    pass
   
   

time.sleep(20)

driver.quit()
