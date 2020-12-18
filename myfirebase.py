import requests
import json
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
import certifi

class MyFirebase():
    wak = "AIzaSyDaGpUCprO5OjKxSNR6-E325gadC5y-sAY"

    def sign_up(self,email,password):
        app = App.get_running_app()
        # Send email and password to Firebase
        # Firebase will return localId, authToken (idToken), refreshToken
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        signup_payload = {"email": email, "password": password, "returnSecureToken": True}
        sign_up_request = requests.post(signup_url, data= signup_payload)
        sign_up_data = json.loads(sign_up_request.content.decode())

        if sign_up_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # Save refreshToken to a file

            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in main app class
            # Save idToken to a variable in main app class
            app.local_id = localId
            app.id_token = idToken


            my_data='{"Order": "coka"}'

            post_request= requests.patch("https://foodmms-55bed.firebaseio.com/"+localId+".json?auth="+idToken,data=my_data)
            print(localId)
            print(post_request.ok)
            print(post_request.content.decode())
            app.change_screen("sandwiches")

        elif sign_up_request.ok == False:
            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]['message']
            if error_message == "EMAIL_EXISTS":
                self.sign_in_existing_user(email, password)
            else:
                app.root.ids['login'].ids['login_message'].text = error_message.replace("_", " ")


    def sign_in_existing_user(self, email, password):
        """Called if a user tried to sign up and their email already existed."""
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
        signin_payload = {"email": email, "password": password, "returnSecureToken": True}
        signin_request = requests.post(signin_url, data=signin_payload)
        sign_up_data = json.loads(signin_request.content.decode())
        app = App.get_running_app()
        print(signin_request.ok)
        print(signin_request.content.decode())

        if signin_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']

            # Save refreshToken to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in main app class
            # Save idToken to a variable in main app class
            app.local_id = localId
            app.id_token = idToken

            # Create new key in database from localI
            #app.change_screen("sandwiches")
            app.on_start()
        elif signin_request.ok == False:
            error_data = json.loads(signin_request.content.decode())
            error_message = error_data["error"]['message']
            app.root.ids['login'].ids['login_message'].text = "EMAIL EXISTS - " + error_message.replace("_", " ")

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        id_token = refresh_req.json()['id_token']
        local_id = refresh_req.json()['user_id']
        return id_token, local_id