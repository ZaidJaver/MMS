from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from myfirebase import MyFirebase
import requests
import json

global order_list
global my_data
my_data =''
order_list = []

class LoginScreen(Screen):
    pass

class SandwichesScreen(Screen):
    def checkbox_click(self, instance, value):
        if value is True:
            print("Checkbox_1 Checked")
            order_list.append(str(item_1))
        else:
            print("Checkbox_1 Unchecked")
            order_list.remove(str(item_1))
    def checkbox_click2(self, instance, value):
        if value is True:
            print("Checkbox_2 Checked")
            order_list.append(str(item_2))
        else:
            print("Checkbox_2 Unchecked")
            order_list.remove(str(item_2))
    def checkbox_click3(self, instance, value):
        if value is True:
            print("Checkbox_3 Checked")
            order_list.append(str(item_3))
            print(order_list)
        else:
            print("Checkbox_3 Unchecked")
            order_list.remove(str(item_3))
    def checkbox_click4(self, instance, value):
        if value is True:
            print("Checkbox_4 Checked")
            order_list.append(str(item_4))
        else:
            print("Checkbox_4 Unchecked")
            order_list.remove(str(item_4))


class DrinksScreen(Screen):
    def checkbox_click(self, instance, value):
        if value is True:
            print("Checkbox_1 Checked")
            order_list.append(str(item_11))
        else:
            print("Checkbox_1 Unchecked")
            order_list.remove(str(item_11))
    def checkbox_click22(self, instance, value):
        if value is True:
            print("Checkbox_2 Checked")
            order_list.append(str(item_22))
        else:
            print("Checkbox_2 Unchecked")
            order_list.remove(str(item_22))
    def checkbox_click33(self, instance, value):
        if value is True:
            print("Checkbox_3 Checked")
            order_list.append(str(item_33))
        else:
            print("Checkbox_3 Unchecked")
            order_list.remove(str(item_33))
    def checkbox_click44(self, instance, value):
        if value is True:
            print("Checkbox_4 Checked")
            order_list.append(str(item_44))
        else:
            print("Checkbox_4 Unchecked")
            order_list.remove(str(item_44))



class CheckoutScreen(Screen):
    def on_enter(self, *args):
        label = self.ids['order']
        label.text = str(order_list)

    def send_order(instance):
        print("Order Sent now")
        post_request = requests.delete("https://foodmms-55bed.firebaseio.com/" + LOCALID + ".json?auth=" + IDTOKEN)
        print(post_request.ok)
        print(post_request.content.decode())
        my_data= ''
        for index in range (len(order_list)):
            my_data = my_data + '"Order' +str(index+1)+'":"' + order_list[index] +'"'
            if index < len(order_list)-1:
                my_data = my_data +','
        my_data = '{'+ my_data +'}'
        print(my_data)
        post_request = requests.patch("https://foodmms-55bed.firebaseio.com/" + LOCALID + ".json?auth=" + IDTOKEN, data= my_data)
        print(post_request.ok)
        print(post_request.content.decode())
        print(str(order_list))






class ImageButton(ButtonBehavior, Image):
    pass

class LabelButton(ButtonBehavior,Label):
    pass

GUI = Builder.load_file("main.kv")
class MainApp(App):
    food_id =1
    def build(self):
        self.my_firebase = MyFirebase()
        return GUI
    def on_start(self):
        try:
            # Try to read the persistent signin credentials (refresh token)
            with open("refresh_token.txt", 'r') as f:
                refresh_token = f.read()
            # Use refresh token to get a new idToken
            id_token, local_id = self.my_firebase.exchange_refresh_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            global LOCALID
            LOCALID =  local_id
            global IDTOKEN
            IDTOKEN = id_token
            #Get the database
            result = requests.get("https://foodmms-55bed.firebaseio.com/.json")
            print("was it ok?" , result.ok)
            data = json.loads(result.content.decode())
            print(data)
            print(data['Drinks '])
            print(data['Food'])
            drinks = data['Drinks ']
            global item_11, item_22, item_33, item_44
            global item_1, item_2, item_3, item_4
            item_11 = drinks['D1']
            item_22 = drinks['D2 ']
            item_33 = drinks['D3 ']
            item_44 = drinks['D4']
            sandwiches = data['Food']
            item_1 =sandwiches['F1']
            item_2 = sandwiches['F2']
            item_3 = sandwiches['F3 ']
            item_4 = sandwiches['F4 ']
            label1= self.root.ids['sandwiches'].ids['item_1']
            label1.text = item_1
            label2= self.root.ids['sandwiches'].ids['item_2']
            label2.text = item_2
            label3= self.root.ids['sandwiches'].ids['item_3']
            label3.text = item_3
            label4= self.root.ids['sandwiches'].ids['item_4']
            label4.text = item_4
            ###########################################################
            label11= self.root.ids['drinks'].ids['item_11']
            label11.text = item_11
            label22= self.root.ids['drinks'].ids['item_22']
            label22.text = item_22
            label33= self.root.ids['drinks'].ids['item_33']
            label33.text = item_33
            label44= self.root.ids['drinks'].ids['item_44']
            label44.text = item_44
            self.change_screen("sandwiches")

        except:

            print("Pass")
            result = requests.get("https://foodmms-55bed.firebaseio.com/.json")
            print("was it ok?" , result.ok)
            data = json.loads(result.content.decode())
            print(data['Drinks '])
            print(data['Food'])
            drinks = data['Drinks ']

            item_11 = drinks['D1']
            item_22 = drinks['D2 ']
            item_33 = drinks['D3 ']
            item_44 = drinks['D4']
            sandwiches = data['Food']
            item_1 =sandwiches['F1']
            item_2 = sandwiches['F2']
            item_3 = sandwiches['F3 ']
            item_4 = sandwiches['F4 ']
            label1= self.root.ids['sandwiches'].ids['item_1']
            label1.text = item_1
            label2= self.root.ids['sandwiches'].ids['item_2']
            label2.text = item_2
            label3= self.root.ids['sandwiches'].ids['item_3']
            label3.text = item_3
            label4= self.root.ids['sandwiches'].ids['item_4']
            label4.text = item_4
            ###########################################################
            label11= self.root.ids['drinks'].ids['item_11']
            label11.text = item_11
            label22= self.root.ids['drinks'].ids['item_22']
            label22.text = item_22
            label33= self.root.ids['drinks'].ids['item_33']
            label33.text = item_33
            label44= self.root.ids['drinks'].ids['item_44']
            label44.text = item_44
            pass

    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name



MainApp().run()