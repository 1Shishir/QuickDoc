from django.shortcuts import render
import pyrebase 
from datetime import date
import os
import time
from django.http import JsonResponse


firebaseConfig = {
  "apiKey": "AIzaSyAINjjA3OA6rEblZNjglJzoIBd4kvhyzr4",
  "authDomain": "ldes-9020e.firebaseapp.com",
  "databaseURL": "https://ldes-9020e-default-rtdb.firebaseio.com",
  "projectId": "ldes-9020e",
  "storageBucket": "ldes-9020e.appspot.com",
  "messagingSenderId": "478028763205",
  "appId": "1:478028763205:web:03a6b965aad98dc862132c",
  "measurementId": "G-MFTZ78BB18"
};

firebase=pyrebase.initialize_app(firebaseConfig);
auth=firebase.auth()
db = firebase.database()
storage=firebase.storage()


def singIn(request):
    return render(request,"signIn.html")

def index(request):
    return render(request,"index.html")

def login(request):
    return render(request,"login.html")

def postsign(request):
    email=request.POST.get("email")
    password=request.POST.get("password")

    if email == "admin@admin.com" and password == "admin":
        all_users = db.child("users").get()

        user_objects = []
        if all_users is not None and all_users.val() is not None: 

            for user in all_users.each():
                user_data = user.val()
                user_object = {
                    'dob': user_data.get('dob'),
                    'email': user_data.get('email'),
                    'img': user_data.get('img'),
                    'name': user_data.get('name'),
                    'phone': user_data.get('phone'),
                    'pass':user_data.get('pass')
                }
                user_objects.append(user_object)  

            print(user_objects)

        else:
            user_objects = [{
                'dob':"",
                'email':"",
                'img':"",
                'name':"",
                'phone':"",
                'pass':""
                }
                 ]
            print("No data found in 'all_users'")

        return render(request,"admin.html",{'user_objects': user_objects})
        

    try:
            
            user=auth.sign_in_with_email_and_password(email,password)
            uid=user['localId']
            tkn=user['idToken']

            request.session['uid'] = uid
            request.session['pass'] = password


            tkn_data={"u_id":uid,"tkn":tkn}
            usertkn = db.child('tkn').child(uid).set(tkn_data) 
            
            users_info = db.child("users").child(uid).get()
            user=users_info.val()

            request.session['name'] = user.get('name')
            request.session['img']=user.get('img')
            # img=user.get('img')
            

    except:
        msg="Invalid Credentials"
        return render(request,"login.html",{"msg":msg})

    return render(request,"homepage.html")

def postsignup(request):
    email=request.POST.get("sign_email")
    name=request.POST.get("sign_name")
    phone=request.POST.get("phone")
    password=request.POST.get("sign_pass")
    try:
        user= auth.create_user_with_email_and_password(email, password)
        msg="User created"
        uid=user['localId']

        data={"name": name,"email":email,"phone":phone,"img":"#","dob":"#","pass":password}
        results = db.child('users').child(uid).set(data) 
    except:
        msg="unable to create user"
        
    return render(request,"login.html",{"msg":msg})

def upload_file(request):

    if request.method == 'POST':
        myfile = request.FILES['myfile']
        file_name=myfile.name
        file_size=round(myfile.size/1028, 3)
        file_type=myfile.content_type
        today = date.today().strftime("%d-%m-%Y")
        path="path"
        # add to realtime db
        try:
            if request.session.has_key('uid'):
                uid=request.session['uid']
            else:    
                user=auth.current_user
                uid=user['localId']

            if(uid==None):
               return render(request, "login.html") 
            else:
                print(uid)
                print(doc_id(uid))
                # filename="files/"+myfile.name
                print(file_name)
                f_n, file_ext = os.path.splitext(file_name) 
            
                t_stamp=round(time.time())
                filename="files/"+str(t_stamp)+str(file_ext)
                t_f_name=str(t_stamp)+str(file_ext)

                print(filename)
                storage.child(filename).put(myfile)
                img_ling=storage.child(filename).get_url(None)
                
                doc=doc_id(uid)
                file_data={"doc_id":doc,"file_name":file_name,"f_size":file_size,"f_type":file_type,"f_date":today,"f_link":img_ling,"f_path":path,"t_f_name":t_f_name}
                results = db.child('document').child(uid).child(doc).set(file_data) 
                user_objects="File successfully uploded"
        except:
            user_objects="Upload Failed"
            print('failed to up')

        return render(request,"homepage.html",{'user_objects': user_objects})
    else:
        return render(request,"homepage.html",{'user_objects': user_objects})
         

def doc_id(user_id):
    uid = user_id
    doc_id = 0  

    documents = db.child('document').child(uid).get()

    last_user_key = None  

    if documents.each():
        for user_data in documents.each():
            last_user_key = user_data.key()
        
        if last_user_key is not None:
            doc_id = int(last_user_key) + 1
        else:
            print("No user key found.")
    else:
        doc_id = 0
    
    return doc_id


def display_items(request):
    if request.session.has_key('uid'):
        uid = request.session['uid']
    else:
        user = auth.current_user
        uid = user['localId']

    all_users = db.child("document").child(uid).get()

    user_objects = []
    if all_users is not None and all_users.val() is not None:  # Check if all_users is not None and has a value

        for user in all_users.each():
            user_data = user.val()
            user_object = {
                "doc_id": user_data.get('doc_id'),
                'f_date': user_data.get('f_date'),
                'file_name': user_data.get('file_name'),
                'f_link': user_data.get('f_link'),
                'f_path': user_data.get('path'),
                'f_size': user_data.get('f_size'),
                'f_type': user_data.get('f_type'),
                't_f_name': user_data.get('t_f_name')
            }
            user_objects.append(user_object)  # This line should be inside the loop

        print(user_objects)
    else:
        user_objects = [{
            "doc_id": "",
            'f_date': "",
            'file_name': "",
            'f_link': "",
            'f_path': "",
            'f_size': "",
            'f_type': "",
            't_f_name': ""
        }]
        print("No data found in 'all_users'")

    return render(request, "uploads.html", {'user_objects': user_objects})

def test(request):
    # user=auth.current_user
    # file=storage.child("files/example3.jpg").put(r"C:\Users\Shishir-PC\Pictures\7.jpg", user['localId'])
    # print(storage.child("files/m.png").get_url(None))
    # filename="files/"+"upload.png"
    # link=storage.child(filename).get_url(None)
    # print(link)
    # filename = "abc.jpg"
    # file_name, file_extension = os.path.splitext(filename)
    # print(file_name)  # Output: abc
    # print(file_extension)
    # import time
    # Get the current timestamp
    # current_timestamp = time.time()
    # print("Current timestamp:", round(current_timestamp))
    # s="img/jpd"
    # if(s.find("img") != -1):
    #     print("ok")
    # else:
    #     print("not")
    
     if request.method == 'POST':
        try:
            if request.session.has_key('uid'):
                uid = request.session['uid']
            else:    
                user = auth.current_user
                uid = user['localId']

            if uid is None:
                return render(request, "login.html")
            else:
                
                doc_id = request.POST.get('doc_id')
                new_filename = request.POST.get('newFileName')
              
                db.child('document').child(uid).child(doc_id).update({"file_name": new_filename})

        except Exception as e:
            user_objects = "rename failed"
            print(f'Failed to rename: {str(e)}')

        return display_items(request)


def home(request):
    return render(request, "homepage.html")

# def download(request):
#     if request.method == 'POST':
#         t_fl=request.POST.get("t_file")
#         fname=request.POST.get("file_name")
#         storage=firebase.storage()
#         # storage.child("files/"+str(t_fl)).download(str(fname))
#         storage.child("files/"+str(t_fl)).download(filename=str(fname), path="C:/Users/Shishir-PC/Downloads")
#         # storage.child("files/"+str(t_fl)).download(str(fname))
#         print(str(t_fl)+str(fname))
#     return render(request, "uploads.html")


def view_profile(request):
    u_obj=[]

    if request.session.has_key('uid'):
        uid=request.session['uid']
        users_info = db.child("users").child(uid).get()
        user=users_info.val()

        user_obj = {
        "name":user.get('name') ,
        "email":user.get('email'),
        "phone":user.get('phone'),
        "dob":user.get('dob'), 
        "img":user.get('img'),
        "pass":user.get('pass')
        }

        u_obj.append(user_obj)

        print(u_obj)
        return render(request, "editProfile.html",{'u_obj':u_obj})

def update_profile(request):
    if request.session.has_key('uid'):
       uid=request.session['uid']

    email=request.POST.get("update_email")
    name=request.POST.get("update_name")
    phone=request.POST.get("update_phone")
    dob=request.POST.get("update_dob")
    password=request.POST.get("confirm_pass")

    try:
        myfile = request.FILES['img']
    except :
        myfile = None

    try:
        user=auth.sign_in_with_email_and_password(email,password)
        if myfile:
            im=upload_profile_img(uid, myfile)
        else:
            im=request.session['img']

        data={"name": name, "email": email, "phone": phone, "img": im, "dob": dob,"pass":request.session['pass']}
        results = db.child('users').child(uid).set(data) 

        request.session['name'] = name
        request.session['img'] = im
        msg="profile updated"
    except:
        msg="failed to update"
    
    print(msg)   
    return view_profile(request)


def upload_profile_img(uid,myfile):
        filename="profile/"+str(uid)
        storage.child(filename).put(myfile)
        img_ling=storage.child(filename).get_url(None)
        return img_ling



def logout(request):
    if request.session.has_key('uid'):
        del request.session['uid']
        del request.session['name']
        del request.session['img']
        del request.session['pass']


    return render(request, "login.html")


def admin(request):

    all_users = db.child("users").get()

    user_objects = []
    if all_users is not None and all_users.val() is not None:  # Check if all_users is not None and has a value

        for user in all_users.each():
            user_data = user.val()
            user_object = {
                'dob': user_data.get('dob'),
                'email': user_data.get('email'),
                'img': user_data.get('img'),
                'name': user_data.get('name'),
                'phone': user_data.get('phone'),
                'pass':user_data.get('pass')
            }
            user_objects.append(user_object)  # This line should be inside the loop

        print(user_objects)
    else:
        user_objects = [{
                'dob':"",
                'email':"",
                'img':"",
                'name':"",
                'phone':"",
                'pass':""
            }
        ]
        print("No data found in 'all_users'")

    return render(request,"admin.html",{'user_objects': user_objects})


def user_details(request):
    dob = request.GET.get('dob', '')
    email = request.GET.get('email', '')
    img = request.GET.get('img', '')
    name = request.GET.get('name', '')
    phone = request.GET.get('phone', '')

    user_details = {
        'dob': dob,
        'email': email,
        'img': img,
        'name': name,
        'phone': phone,
        
    }

    return render(request, "user_details.html", {'user_details': user_details})



def deleteUser(request):
  
    # try:
    #     auth.delete_user_account(user_uid_to_delete)
    #     print(f"User {user_uid_to_delete} deleted successfully.")
    # except Exception as e:
    #     print(f"Error deleting user: {e}")
    
    # auth = firebase.auth()
    # user = auth.sign_in_with_email_and_password("user1@gmail.com","123456")
    # auth.delete_user_account(user['idToken'])
    # pass=request.POST.get("user_uid")
    # print(u_tkn.get('tkn'))

    password=request.POST.get("pass")
    em=request.POST.get("em")
    user = auth.sign_in_with_email_and_password(em,password)
    uid=user['localId']
    auth.delete_user_account(user['idToken'])
    db.child("users").child(uid).remove()
    

    # 
    all_users = db.child("users").get()

    user_objects = []
    if all_users is not None and all_users.val() is not None: 

        for user in all_users.each():
            user_data = user.val()
            user_object = {
                    'dob': user_data.get('dob'),
                    'email': user_data.get('email'),
                    'img': user_data.get('img'),
                    'name': user_data.get('name'),
                    'phone': user_data.get('phone'),
                    'pass':user_data.get('pass')
            }
            user_objects.append(user_object)  

        print(user_objects)

    else:
            user_objects = [{
                'dob':"",
                'email':"",
                'img':"",
                'name':"",
                'phone':"",
                'pass':""
                }
                 ]
            print("No data found in 'all_users'")

    return render(request,"admin.html",{'user_objects': user_objects})


    