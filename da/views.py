from http.client import HTTPResponse
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Artist, Buyer,Feedback


# Artist views
def artist_home(request):
    portrait = Portraits.objects.all()
    print("ggtt",portrait)
    return render(request, 'home.html',{'portraits':portrait}) 

def artist_profile(request):
    if 'email' in request.session:
        email = request.session['email']
        artist = Artist.objects.get(email=email)
    return render(request, 'profile.html', {'artist': artist})

def artist_edit_profile(request, uid):
    artist = Artist.objects.get(id=uid)
    if request.method == "POST":
        artist.username = request.POST.get('name')
        artist.email = request.POST.get('email')
        artist.gender = request.POST.get('gender')
        artist.phonenumber = request.POST.get('phonenumber')
        artist.dob = request.POST.get('dob')
        image = request.FILES.get('image')
        if image:
            artist.image = image
        artist.save()
        return redirect('profile')
    return render(request, 'profile.html', {'artist': artist})

def artist_register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        dob = request.POST.get('dob')
        
        
        artist = Artist(username=username, email=email, password=password, image=image, gender=gender, phonenumber=phonenumber, dob=dob)
        artist.save()
        return redirect('index')
    return render(request, 'registration.html')

def artist_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            artist = Artist.objects.get(email=email, password=password)
            request.session['email'] = artist.email
            
            return redirect('home')
        except Artist.DoesNotExist:
            msg = "Invalid credentials"
        return render(request,'login.html', {"msg": msg})
    return render(request,'login.html')

# Buyer views
def buyer_home(request):
    portrait = Portraits.objects.all()
    return render(request, 'buyerhome.html',{ 'portraits':portrait })

def buyer_profile(request):
    if 'email' in request.session:
        email = request.session['email']
        buyer = Buyer.objects.get(email=email)
    return render(request, 'buyerprofile.html', {'buyer': buyer})
def buyer_edit_profile(request, uid):
    buyer = Buyer.objects.get(id=uid)
    if request.method == "POST":
        buyer.username = request.POST.get('name')
        buyer.email = request.POST.get('email')
        buyer.gender = request.POST.get('gender')
        buyer.phonenumber = request.POST.get('phonenumber')
        buyer.dob = request.POST.get('dob')
        image = request.FILES.get('image')
        if image:
            buyer.image = image
        buyer.save()
        return redirect('buyer_profile')
    return render(request, 'buyerprofile.html', {'buyer': buyer})
def buyer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        dob = request.POST.get('dob')
      
        
        buyer = Buyer(username=username, email=email, password=password, image=image, gender=gender, phonenumber=phonenumber, dob=dob)
        buyer.save()
        return redirect('index')
    return render(request, 'buyer_register.html')

def buyer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            buyer = Buyer.objects.get(email=email, password=password)
            request.session['email'] = buyer.email
            return redirect('buyer_home')
        except Buyer.DoesNotExist:
            msg = "Invalid credentials"
        return render(request, 'buyer_login.html', {"msg": msg})
    return render(request, 'buyer_login.html')

# Admin views
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            return redirect('admin_dashboard')
    return render(request, 'adminlogin.html')

def admin_dashboard(request):
    total_artists = Artist.objects.count()
    total_buyers = Buyer.objects.count()
    total_users = total_artists + total_buyers  # Total users = Artists + Buyers
    total_portraits = Portraits.objects.count()
    total_feedbacks = Feedback.objects.count()

    context = {
        'total_users': total_users,
        'total_artists': total_artists,
        'total_buyers': total_buyers,
        'total_portraits': total_portraits,
        'total_feedbacks': total_feedbacks,
    }

    return render(request, 'admindash.html', context)
def terms(request):
    return render(request,'terms.html')

def buyer_list(request):
    buyers = Buyer.objects.all()
    return render(request, 'buyerlist.html', {'buyers': buyers})

def delete_buyer(request, buyer_id):
    buyer = Buyer.objects.get(id=buyer_id)
    buyer.delete()
    return redirect('buyerlist')
def artistlist(req):
    artists = Artist.objects.all()
    return render(req, 'artistlist.html', {'artists': artists})
def delete_artist(request,id):
    artist = Artist.objects.get(id=id)
    subject = "Account Removal Notification"
    message = f"Dear {artist.username},\n\nYour account has been removed due to suspicious activity. If you think this is a mistake, please contact support.\n\nBest regards,\nAdmin Team"
    recipient_email = artist.email  # Assuming Artist model has an email field

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Ensure this is set in settings.py
        [recipient_email],
        fail_silently=False,
    )
    artist.delete()
    
    return redirect('artistlist')


def logout(request):
    request.session.flush()  
    return redirect('index')  


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')

def logo_gallery(request):
    if 'email' not in request.session:
        return redirect('login')  
    email = request.session['email']
    user = Artist.objects.get(email=email)

    # List all logos for the logged-in user
    logos = Logo.objects.filter(user=user)
    print('vgdgee',logos)
    for i in logos:
        print(i.logo_data)
    return render(request, 'logogallery.html', {'logos': logos})
    
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .models import Logo
import base64
from io import BytesIO

# def logo_creation(request):
#     if 'email' in request.session:
#         email = request.session['email']
#         user = Artist.objects.get(email=email)
    
#         if request.method == 'POST':
#             # Handling for saving logo as JSON

#             logo_data = request.POST.get('logo_data') 
           
            
#             if logo_data:

#                 logo_json = logo_data
#                   # saving the canvas data in JSON format for future edits
#                 logo = Logo(user=user, name="Custom Logo", logo_data=logo_json)
#                 logo.save()
#                 return redirect('logo_gallery')  # Redirecting to the gallery after saving logo
            
#             # Handling for saving logo image (optional)
#             logo_image_data = request.POST.get('logo_image')  # This will be the base64 image string
#             if logo_image_data:
#                 logo_image_data = base64.b64decode(logo_image_data.split(',')[1])  # Decode base64 to binary data
#                 image_name = f"logo_{request.user.id}.png"
#                 logo_image = ContentFile(logo_image_data, name=image_name)  # Save the image to the file system
#                 logo = Logo(user=request.user, name="Custom Logo", logo_image=logo_image)
#                 logo.save()
#                 return redirect('logo_gallery')  # Redirecting to the gallery page
        
#         return render(request, 'logo.html') 
#     return render(request, 'logo.html') # Render the logo creation page
 # Redirect to the login page or other appropriate action
import base64
import json
import time
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .models import Logo, Artist

def logo_creation(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = Artist.objects.get(email=email)
        except Artist.DoesNotExist:
            return redirect('login')

        if request.method == 'POST':
            # Retrieve both the base64 image data and canvas state (JSON)
            logo_data = request.POST.get('logo_data')  # base64 image data
            canvas_state = request.POST.get('canvasState')  # optional: canvas state (JSON)

            if not logo_data:
                return render(request, 'logo.html', {'error': 'Please create a logo before submitting!'})

            try:
                # Decode the base64 image string and save the image
                if logo_data:
                    format, imgstr = logo_data.split(';base64,')  # Extract format and base64 string
                    ext = format.split('/')[1]  # Get the image extension (e.g., png)
                    img_data = base64.b64decode(imgstr)  # Decode the base64 data to binary

                    # Generate a unique filename for the image
                    image_name = f"logo_{int(time.time())}.{ext}"
                    logo_image = ContentFile(img_data, name=image_name)

                    # Create and save the Logo object with the image
                    logo = Logo(user=user, name="Custom Logo", logo_image=logo_image, logo_data=canvas_state)
                    logo.save()

                # Redirect to the gallery or another page
                return redirect('logo_gallery')

            except Exception as e:
                print(f"Error saving logo or image: {e}")
                return render(request, 'logo.html', {'error': f"Error: {e}"})

        return render(request, 'logo.html')

    return redirect('login')

                                                                                                                                                                            




from django.shortcuts import render, get_object_or_404
from .models import Logo

def preview_logo(request, logo_id):
    # Get the logo from the database
    logo = get_object_or_404(Logo, id=logo_id)

    # Pass the logo data (base64) and optional JSON (canvas state) to the template
    logo_data = logo.logo_image.url if logo.logo_image else None  # The image URL
    canvas_state = logo.logo_data  # Optional: JSON state for editable elements

    # Render the 3D preview page and pass the logo data
    return render(request, 'preview.html', {
        'logo': logo,
        'logo_data': logo_data,
        'canvas_state': canvas_state,  # Only if you need the editable canvas state
    })



import json
import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from .models import Logo

# def edit_logo(request, logo_id):
#     logo = get_object_or_404(Logo, id=logo_id)

#     if request.method == 'POST':
#         logo_data = request.POST.get('logo_data')  # JSON data from canvas
#         logo_image_data = request.POST.get('logo_image')  # Base64 image string

#         # Handling the JSON logo data (logo configuration)
#         if logo_data:
#             try:
#                 # Attempt to parse and save the logo's design as JSON
#                 json_data = json.loads(logo_data)
#                 logo.logo_data = json.dumps(json_data)  # Save as a JSON string
#                 logo.save()
#             except json.JSONDecodeError:
#                 print("Error decoding JSON data")

#         # Handling the logo image (base64 string)
#         if logo_image_data:
#             try:
#                 # Split the base64 string and decode the image data
#                 format, imgstr = logo_image_data.split(';base64,')  # Extract image format and data
#                 ext = format.split('/')[1]  # Extract image extension (e.g., 'png', 'jpeg')
#                 img_data = base64.b64decode(imgstr)  # Decode to binary data

#                 # Create the image file and save it
#                 image_name = f"logo_{logo.id}.{ext}"
#                 logo_image = ContentFile(img_data, name=image_name)
#                 logo.logo_image = logo_image  # Save the image to the Logo model
#                 logo.save()
#             except Exception as e:
#                 print(f"Error saving the image: {e}")

#         # After saving, redirect to the gallery or another page
#         return redirect('logo_gallery')  # Or any other page you want to redirect to after saving

#     # Pre-populate the form with the current logo data
#     logo_data = logo.logo_data

#     return render(request, 'edit_logo.html', {'logo': logo, 'logo_data': logo_data})
def edit_logo(request, logo_id):
    logo = get_object_or_404(Logo, id=logo_id)

    if request.method == 'POST':
        logo_data = request.POST.get('logo_data')  # JSON data from canvas
        logo_image_data = request.POST.get('logo_image')  # Base64 image string

        if logo_data:
            try:
                # Attempt to save the logo's design as JSON
                json_data = json.loads(logo_data)
                logo.logo_data = json.dumps(json_data)  # Save as a JSON string
                logo.save()
            except json.JSONDecodeError:
                print("Error decoding JSON data")

        if logo_image_data:
            try:
                # Decode the base64 image string
                format, imgstr = logo_image_data.split(';base64,')  # Extract format and base64 string
                ext = format.split('/')[1]  # Get the image extension
                img_data = base64.b64decode(imgstr)  # Decode to binary data

                # Create the image file and save it
                image_name = f"logo_{logo.id}.{ext}"
                logo_image = ContentFile(img_data, name=image_name)
                logo.logo_image = logo_image  # Update the logo image field
                logo.save()
            except Exception as e:
                print(f"Error saving image: {e}")

        # After saving, redirect to the gallery or another page
        return redirect('logo_gallery')  # Or any other page

    # Pre-populate the form with the current logo data
    logo_data = logo.logo_data  # JSON data for the canvas
    logo_image = logo.logo_image.url if logo.logo_image else None  # Image URL for the logo

    return render(request, 'edit_logo.html', {'logo': logo, 'logo_data': logo_data, 'logo_image': logo_image})

def delete_logo(request, logo_id):
    logo = get_object_or_404(Logo, id=logo_id)
    logo.delete()
    return redirect('logo_gallery')



# from PIL import Image
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.conf import settings
# import os

# def add_portrait(request):
#     if request.method == 'POST':
#         email = request.session.get('email')
#         if email:
#             user = Artist.objects.get(email=email)
#             title = request.POST.get('title')
#             description = request.POST.get('description')
#             price = request.POST.get('price')
#             image = request.FILES.get('image')
#             watermark_image = request.FILES.get('watermark_image')
#             artist = user  

#             # Open the uploaded image
#             uploaded_image = Image.open(image).convert("RGBA")

#             # Open the uploaded watermark image
#             watermark = Image.open(watermark_image).convert("RGBA")

#             # Resize watermark to fit the original image
#             watermark_width = uploaded_image.width // 2  # Adjust the scale as needed
#             watermark_height = int(watermark.size[1] * (watermark_width / watermark.size[0]))
#             watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)

#             # Position the watermark at the bottom-right corner
#             position = (
#                 uploaded_image.width - watermark_width - 10,
#                 uploaded_image.height - watermark_height - 10
#             )
            

#             # Create a transparent layer the same size as the original image
#             transparent = Image.new('RGBA', uploaded_image.size, (0, 0, 0, 0))
#             transparent.paste(uploaded_image, (0, 0))
#             transparent.paste(watermark, position, mask=watermark)  # Use the watermark's alpha channel for transparency

#             # Save the watermarked image to a BytesIO object
#             output = BytesIO()
#             transparent.convert("RGB").save(output, format='JPEG')  # Convert to RGB for saving as JPEG
#             output.seek(0)

#             # Convert the BytesIO object into an InMemoryUploadedFile
#             watermarked_file = InMemoryUploadedFile(
#                 output, 'ImageField', image.name, 'image/jpeg', output.getbuffer().nbytes, None
#             )

#             # Create a new portrait entry with the watermarked image
#             portrait = Portraits.objects.create(
#                 title=title,
#                 description=description,
#                 price=price,
#                 image=watermarked_file,
#                 artist=artist
#             )

#             return redirect('portrait_gallery')  
#     return render(request, 'addportrait.html')

from django.shortcuts import render, redirect
from PIL import Image
from io import BytesIO
import os
from .models import Artist, Logo, Portraits  # Adjust import based on your app structure
from django.core.files.uploadedfile import InMemoryUploadedFile
def add_portrait(request):
    # Get artist email from session
    artist_email = request.session.get('email')
    if not artist_email:
        return render(request, 'addportrait.html', {'error': 'Please log in first.'})

    # Fetch artist and their logos
    try:
        artist = Artist.objects.get(email=artist_email)
        artist_logos = Logo.objects.filter(user=artist).exclude(logo_image__isnull=True)
    except Artist.DoesNotExist:
        return render(request, 'addportrait.html', {'error': 'Artist not found.'})

    if request.method != 'POST':
        return render(request, 'addportrait.html', {'artist_logos': artist_logos})

    # Handle POST request
    title = request.POST.get('title')
    description = request.POST.get('description', '')
    price = request.POST.get('price', '0')
    image = request.FILES.get('image')
    watermark_id = request.POST.get('watermark')

    # Validate inputs
    if not title:
        return render(request, 'addportrait.html', {'error': 'Title is required.', 'artist_logos': artist_logos})
    if not image:
        return render(request, 'addportrait.html', {'error': 'No image uploaded.', 'artist_logos': artist_logos})
    if not watermark_id:
        return render(request, 'addportrait.html', {'error': 'Please select a watermark.', 'artist_logos': artist_logos})

    # Validate price
    try:
        price_value = float(price)
    except ValueError:
        return render(request, 'addportrait.html', {'error': 'Invalid price format.', 'artist_logos': artist_logos})

    # Get selected watermark
    try:
        watermark = Logo.objects.get(id=watermark_id, user=artist)
        watermark_path = watermark.logo_image.path
        if not os.path.exists(watermark_path):
            return render(request, 'addportrait.html', {'error': 'Watermark file not found.', 'artist_logos': artist_logos})
    except Logo.DoesNotExist:
        return render(request, 'addportrait.html', {'error': 'Invalid watermark selected.', 'artist_logos': artist_logos})

    try:
        # Process image with watermark
        uploaded_image = Image.open(image).convert('RGBA')
        watermark_img = Image.open(watermark_path).convert('RGBA')

        watermark_width = uploaded_image.width // 2
        watermark_height = int(watermark_img.size[1] * (watermark_width / watermark_img.size[0]))
        watermark_img = watermark_img.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)

        position = (
            uploaded_image.width - watermark_width - 10,
            uploaded_image.height - watermark_height - 10
        )

        transparent = Image.new('RGBA', uploaded_image.size, (0, 0, 0, 0))
        transparent.paste(uploaded_image, (0, 0))
        transparent.paste(watermark_img, position, mask=watermark_img)

        # Convert to JPEG
        output = BytesIO()
        transparent.convert('RGB').save(output, format='JPEG')
        output.seek(0)

        watermarked_file = InMemoryUploadedFile(
            output, 'ImageField', image.name, 'image/jpeg', output.getbuffer().nbytes, None
        )

        # Save portrait
        portrait = Portraits(
            title=title,
            description=description,
            price=price_value,
            image=watermarked_file,
            artist=artist
        )
        portrait.save()

        return redirect('portrait_gallery')

    except Exception as e:
        return render(request, 'addportrait.html', {'error': f'Unexpected error: {str(e)}', 'artist_logos': artist_logos})

from django.shortcuts import render, redirect
from .models import Portraits, ProductFeedback
from django.db.models import Avg

def portrait_gallery(request):
    
    portrait = Portraits.objects.all()
    try:
        email = request.session['email']
        user = Artist.objects.filter(email=email).first() 
        is_artist = user is not None
    except KeyError:
        return render(request, 'portrait_gallery.html')

    # Calculate the average rating for each portrait
    for p in portrait:
        avg_rating = ProductFeedback.objects.filter(product=p).aggregate(Avg('rating'))['rating__avg']
        p.average_rating = avg_rating if avg_rating else 0  

    return render(request, 'portrait_gallery.html', {'portrait': portrait, 'em': email,'is_artist': is_artist})

from django.shortcuts import render, get_object_or_404
import razorpay
from django.conf import settings
from .models import Portraits, Buyer  # Assuming you have a Buyer model

client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def purchase(request, portrait_id):
    portrait = get_object_or_404(Portraits, id=portrait_id)

    if 'email' in request.session:
        email = request.session['email']
        buyer = Buyer.objects.filter(email=email).first()
        artist = Artist.objects.filter(email=email).first()

        if buyer:
            user = buyer
        elif artist:
            user = artist
        else:
            messages.error(request, "User not found. Please log in.")
            return redirect('login')

        amount = int(portrait.price * 100)  # Amount in paise
        currency = 'INR'

        razorpay_order = client.order.create(dict(amount=amount, currency=currency, payment_capture='1'))
        razorpay_order_id = razorpay_order['id']
        callback_url = '/payment_success/'  # This is the callback URL for Razorpay

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': callback_url,
            'portrait': portrait,
        }

        return render(request, 'payment.html', context)

    return redirect('portrait_gallery')

# Redirect to a fallback page if email is not found
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import razorpay
from datetime import datetime
from .models import Portraits, Payment, Buyer
from django.core.mail import send_mail
client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    portrait_id = request.GET.get('portrait_id')

    if payment_id and order_id and portrait_id:
        try:
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':  # Payment was successful
                portrait = get_object_or_404(Portraits, id=portrait_id)
                portrait.is_sold = True
                portrait.save()
                
                artist = portrait.artist  # Assuming portrait has a foreign key to artist
            
                

                buyer = Buyer.objects.get(email=request.session['email'])
                Payment.objects.create(
                    buyer=buyer,
                    portrait=portrait,
                    price=portrait.price,
                    transaction_id=payment['id'],
                    date=datetime.now(),
                )
                # Notification.objects.create(
                # artist=artist,
                # message=f"Your portrait '{portrait.title}' has been sold! to '{buyer.username}"
                # )
                subject = f'Your portrait {portrait.title} will arrive shortly!'
                message = (
                    f"Dear {buyer.username},\n\n"
                    f"Thank you for purchasing the portrait '{portrait.title}'! Your payment has been successfully processed, "
                    "and it will be delivered shortly.\n\n"
                    "We hope you enjoy your new artwork!\n\n"
                    "Best regards,\nThe Art Gallery Team"
                )
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [buyer.email]

                try:
                    send_mail(subject, message, from_email, recipient_list)
                except Exception as e:
                    print(f"Error sending email: {e}")

                return redirect('portrait_gallery')  
            else:
                return render(request, 'portrait_gallery.html', {'error': 'Payment not captured.'})

        except razorpay.errors.SignatureVerificationError:
            return render(request, 'portrait_gallery.html', {'error': 'Signature verification failed.'})
        
        except Exception as e:
            return render(request, 'portrait_gallery.html', {'error': f'Error: {e}'})
    return render(request, 'portrait_gallery.html', {'error': 'Invalid payment details.'})


  # Something went wrong


def payment_failed(request):
    return render(request, 'payment_failed.html')




from .models import *

# Create your views here.


def HomeView(request):
    email = request.session['email']
    user = Artist.objects.get(email=email)
    if request.method == "POST":
        username = request.POST["username"]
        room = request.POST["room"]
        try:
            existing_room = Room.objects.get(room_name__icontains=room)
        except Room.DoesNotExist:
            r = Room.objects.create(room_name=room)
        return redirect("room", room_name=room, username=username)
    return render(request, "chat.html",{'user': user})


def RoomView(request, room_name, username):
    try:
        existing_room = Room.objects.get(room_name__icontains=room_name)
    except Room.DoesNotExist:
        return redirect("login")
    get_messages = Message.objects.filter(room=existing_room)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": existing_room.room_name,
    }

    return render(request, "room.html", context)


def art_creation(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = Artist.objects.get(email=email)
        except Artist.DoesNotExist:
            return redirect('login')

        if request.method == 'POST':
            # Retrieve both the base64 image data and canvas state (JSON)
            logo_data = request.POST.get('logo_data')  # base64 image data
            canvas_state = request.POST.get('canvasState')  # optional: canvas state (JSON)

            if not logo_data:
                return render(request, 'logo.html', {'error': 'Please create a logo before submitting!'})

            try:
                # Decode the base64 image string and save the image
                if logo_data:
                    format, imgstr = logo_data.split(';base64,')  # Extract format and base64 string
                    ext = format.split('/')[1]  # Get the image extension (e.g., png)
                    img_data = base64.b64decode(imgstr)  # Decode the base64 data to binary

                    # Generate a unique filename for the image
                    image_name = f"logo_{int(time.time())}.{ext}"
                    logo_image = ContentFile(img_data, name=image_name)

                    # Create and save the Logo object with the image
                    logo = Logo(user=user, name="Custom Logo", logo_image=logo_image, logo_data=canvas_state)
                    logo.save()

                # Redirect to the gallery or another page
                return redirect('logo_gallery')

            except Exception as e:
                print(f"Error saving logo or image: {e}")
                return render(request, 'logo.html', {'error': f"Error: {e}"})

        return render(request, 'art.html')

    return redirect('login')




def feedback(request):
    email = request.session.get('email')
    if email:
        try:
            u = Buyer.objects.get(email=email)
        except Buyer.DoesNotExist:
            return HTTPResponse("<script>alert('User not found.'); window.location.href='/login';</script>")

        if request.method == "POST":
            feedback_text = request.POST.get('feedback_text')
            rating = request.POST.get('rating')

            if not feedback_text or not rating:
                alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/feedback';</script>"
                return HTTPResponse(alert_message)

            try:
                rating = int(rating)
                if rating not in [1, 2, 3, 4, 5]:
                    raise ValueError("Invalid rating value")
            except ValueError:
                alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/feedback';</script>"
                return HTTPResponse(alert_message)

            feedback_instance = Feedback(
                feedback_text=feedback_text,
                rating=rating,
                email=email
            )
            feedback_instance.save()

            return render(request, 'feedback.html', {'user': u})

        return render(request, 'feedback.html', {'user': u})
    else:
        return HTTPResponse("<script>alert('Session expired. Please log in again.'); window.location.href='/login';</script>")
  
  
    


def feedback_list(request):
    feed = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'feed': feed})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Portraits, ProductFeedback



# View to handle the feedback form submission
def submit_feedback(request, portrait_id):
    if request.method == 'POST':
        # Fetch the portrait using the given ID
        portrait = get_object_or_404(Portraits, id=portrait_id)

        # Get data from the form submission
        rating = request.POST['rating']
        feedback_text = request.POST['feedback_text']
        email = request.POST['email']

        # Create a new feedback entry and save it to the database
        ProductFeedback.objects.create(
            product=portrait,
            rating=rating,
            feedback_text=feedback_text,
            email=email
        )
        
   
        return redirect('portrait_gallery')  # Replace 'success' with the name of your success URL

    # If the form is not submitted using POST, redirect to the portrait details page (or any other fallback)
    return render(request,'submit_feedback.html')
def userfeedlist(request):
    feedback = ProductFeedback.objects.all()
    
    return render(request, 'userfeedlist.html', {'feedback': feedback})
def productlist(request):
    # Fetch all portraits from the database
    portraits = Portraits.objects.all() 
    year = datetime.now().year
    return render(request, 'productlist.html', {'portraits': portraits, 'year': year})

# def view_notifications(request):
#     email=request.session.get('email')
#     user=Artist.objects.filter(email=email).first()
#     notifications = Notification.objects.filter(artist=user).order_by('-id')

   
#     notifications.update(is_read=True)

#     return render(request, 'notification.html', {'notifications': notifications})

from django.shortcuts import render

def buyers_list(request):
    purchases = Payment.objects.select_related('buyer', 'portrait').all()
    return render(request, 'buyers_list.html', {'purchases': purchases})

#Algorithm Type: SSIM (Structural Similarity Index).
#Category: Classical image processing technique 

import cv2
from skimage.metrics import structural_similarity as ssim
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse
from .models import Logo

def compare_logo(request):
    result = None  # Initialize result variable

    if request.method == 'POST' and request.FILES.get('logo'):
        # Get the uploaded logo file
        input_logo = request.FILES['logo']

        # Save the uploaded image temporarily
        input_logo_path = default_storage.save(f"temp/{input_logo.name}", input_logo)
        input_logo_full_path = default_storage.path(input_logo_path)

        # Load the uploaded image in grayscale
        input_logo_image = cv2.imread(input_logo_full_path, cv2.IMREAD_GRAYSCALE)
        if input_logo_image is None:
            result = "Uploaded image is invalid."
        else:
            # Fetch all logos from the database
            logos = Logo.objects.all()
            matched = False

            # Compare the uploaded image with each logo
            for logo in logos:
                db_logo_path = logo.logo_image.path
                db_logo_image = cv2.imread(db_logo_path, cv2.IMREAD_GRAYSCALE)
                if db_logo_image is None:
                    continue

                # Resize if dimensions don't match
                if input_logo_image.shape != db_logo_image.shape:
                    db_logo_image = cv2.resize(db_logo_image, (input_logo_image.shape[1], input_logo_image.shape[0]))

                # Compute SSIM (Structural Similarity Index)
                similarity, _ = ssim(input_logo_image, db_logo_image, full=True)

                # Check similarity threshold (adjust as needed)
                if similarity > 0.9:
                    result = f"Logo matched with database logo: {logo.name}"
                    matched = True
                    break

            if not matched:
                result = "No matching logo found."

        # Cleanup temporary file
        default_storage.delete(input_logo_path)

    return render(request, 'compare_logo.html', {'result': result})



from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Artist, PostModel, CommentSectionModel, Buyer


def createPost(request):
    email = request.session.get('email')
    if email:
        user_dtls = get_object_or_404(Artist, email=email)
        if request.method == "POST":
            post_pic = request.FILES.get('post_pic')
            description = request.POST.get('description')
            like_count = 0

            PostModel(
                user=user_dtls,
                post_pic=post_pic,
                description=description,
                likes_count=like_count,
            ).save()
            return redirect('viewpost')
        return render(request, 'addpost.html')
    return redirect('home')


def displayPosts(request):
    posts = PostModel.objects.all()
    post_comments = {}
    try:
        email = request.session['email']  # Retrieve email from session
    except KeyError:
        return redirect('buyerlogin')  # Redirect to login if no email found in session
    
    if email:
        user = Buyer.objects.get(email=email) 

    for post in posts:
        comments = CommentSectionModel.objects.filter(post=post)
        post.comment_count = comments.count()

        if post.post_pic:
            post.is_video = post.post_pic.url.endswith(('.mp4', '.webm', '.ogg'))
            post.is_pdf = post.post_pic.url.endswith('.pdf')
            post.is_image = not (post.is_video or post.is_pdf)
        else:
            post.is_video = post.is_pdf = post.is_image = False

    return render(request, 'viewallposts.html', {'posts': posts, 'comments': comments,'us': user})


def likePost(request,id):
    
    print("hello")
    try:
        email = request.session.get('email')
        print("Session email:", email) 
        if not email:
            return redirect('buyerlogin')  # Redirect to login if no email in session

        post = get_object_or_404(PostModel, id=id)
        user = Buyer.objects.get(email=email)

        if post.liked_users.filter(email=email).exists():
            post.liked_users.remove(user)
            post.likes_count = max(0, post.likes_count - 1)
        else:
            post.liked_users.add(user)
            post.likes_count += 1

        post.save()
        return redirect('display_posts')
    except Exception as e:
        print("Error in liking post:", str(e))
        return redirect('display_posts')



def addComment(request, post_id):
    if request.method == 'POST':
        email = request.session.get('email')
        if not email:
            return redirect('buyerlogin')

        post = get_object_or_404(PostModel, id=post_id)
        user =Buyer.objects.get(email=email)
        comment_text = request.POST.get('comment')

        if comment_text:
            CommentSectionModel.objects.create(user=user, post=post, comment=comment_text)
        else:
            return HttpResponse("<script>alert('Comment cannot be empty.');window.location.href='/display_posts/';</script>")

    return redirect('display_posts')




def commentsDelete(request, cmt_id):
    comment = get_object_or_404(CommentSectionModel, id=cmt_id)
    email = request.session.get('email')
    user = get_object_or_404(Buyer, email=email)

    if user == comment.user:
        comment.delete()
        return redirect('display_posts')
    return HttpResponse("You are not allowed to delete this comment.")


def viewpost(request):
    email = request.session.get('email')
    if email:
        posts = PostModel.objects.filter(user__email=email)
        for post in posts:
             
            comments = CommentSectionModel.objects.filter(post=post)
            post.comment_count = comments.count()
            if post.post_pic:
                file_extension = post.post_pic.url.lower().split('.')[-1]
                if file_extension in ['jpg', 'jpeg', 'png']:
                    post.file_type = 'image'
                elif file_extension in ['mp4', 'mov']:
                    post.file_type = 'video'
                elif file_extension == 'pdf':
                    post.file_type = 'pdf'
                else:
                    post.file_type = 'other'
            else:
                post.file_type = 'other'
        
        return render(request, 'viewposts.html', {'post': posts, 'comments':comments})
    return redirect('viewpost')


def deletepost(request, id):
    post = PostModel.objects.get(id=id)
    post.delete()
    return redirect('viewpost')  



def editepost(request, id):
    post = PostModel.objects.get(id=id)
    if request.method == 'POST':
        description = request.POST.get('description')
        post_pic = request.FILES.get('image')
        post.description = description
        if post_pic:
            post.post_pic = post_pic
        post.save()
        return redirect('viewpost')
    return render(request, 'editpost.html', {'edit': post})

def u_likePost(request, post_id):
    email = request.session.get('email')
    if not email:
        return redirect('login')  # Redirect to login if no email in session

    user = get_object_or_404(Artist, email=email)
    post = get_object_or_404(PostModel, id=post_id)

    if post.liked_users.filter(email=email).exists():
        post.liked_users.remove(user)
        post.likes_count = max(0, post.likes_count - 1)
    else:
        post.liked_users.add(user)
        post.likes_count += 1

    post.save()
    return redirect('profile')  # Redirect back to the artist's profile
def u_addComment(request, post_id):
    if request.method == 'POST':
        email = request.session.get('email')
        if not email:
            return redirect('login')  # Redirect to login if no email in session

        user = get_object_or_404(Artist, email=email)
        post = get_object_or_404(PostModel, id=post_id)
        comment_text = request.POST.get('comment')

        if comment_text:
            CommentSectionModel.objects.create(user=user, post=post, comment=comment_text)
        else:
            return HttpResponse(
                "<script>alert('Comment cannot be empty.');window.location.href='/profile/';</script>"
            )
    return redirect('profile')



#artist scan
# import cv2
# from skimage.metrics import structural_similarity as ssim
# from django.core.files.storage import default_storage
# from django.shortcuts import render
# from .models import Logo, Portraits

# def artistscan(request):
#     result = None
#     portraits = []

#     if request.method == 'POST' and request.FILES.get('logo'):
#         # Get the uploaded logo file
#         input_logo = request.FILES['logo']

#         # Save the uploaded image temporarily
#         input_logo_path = default_storage.save(f"temp/{input_logo.name}", input_logo)
#         input_logo_full_path = default_storage.path(input_logo_path)

#         # Load the uploaded image in grayscale
#         input_logo_image = cv2.imread(input_logo_full_path, cv2.IMREAD_GRAYSCALE)
#         if input_logo_image is None:
#             result = "Uploaded image is invalid."
#         else:
#             # Fetch all logos from the database
#             logos = Logo.objects.all()
#             best_match = None
#             highest_similarity = -1  # Initialize with a low value

#             # Compare the uploaded image with each logo
#             for logo in logos:
#                 db_logo_path = logo.logo_image.path
#                 db_logo_image = cv2.imread(db_logo_path, cv2.IMREAD_GRAYSCALE)
#                 if db_logo_image is None:
#                     continue

#                 # Resize if dimensions don't match
#                 if input_logo_image.shape != db_logo_image.shape:
#                     db_logo_image = cv2.resize(db_logo_image, (input_logo_image.shape[1], input_logo_image.shape[0]))

#                 # Compute SSIM
#                 try:
#                     similarity, _ = ssim(input_logo_image, db_logo_image, full=True)
#                 except ValueError:
#                     continue  # Skip if SSIM computation fails (e.g., due to size mismatch)

#                 # Track the best match
#                 if similarity > highest_similarity:
#                     highest_similarity = similarity
#                     best_match = logo

#             # Define a reasonable threshold (e.g., 0.85) for a match
#             if highest_similarity > 0.90:
#                 result = f"Logo is created with ARTREON by: {best_match.user.username} (Similarity: {highest_similarity:.2f})"
#                 portraits = Portraits.objects.filter(artist=best_match.user)
#             else:
#                 result = f"No matching logo found. Best similarity: {highest_similarity:.2f}"

#         # Cleanup temporary file
#         default_storage.delete(input_logo_path)

#     return render(request, 'artistscanlogo.html', {'result': result, 'portraits': portraits})
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from scipy.spatial.distance import hamming
from django.core.files.storage import default_storage
from django.shortcuts import render
from .models import Logo, Portraits

def preprocess_logo(img_path):
    """Preprocess logo images for better comparison, handling transparency"""
    # Read image with alpha channel
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    
    # Handle different image formats
    if len(img.shape) == 3 and img.shape[2] == 4:  # RGBA image
        # Extract alpha channel
        alpha = img[:, :, 3]
        # Convert to RGB with white background
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # Create a white background
        white_bg = np.ones_like(img_rgb) * 255
        # Blend image with white background using alpha
        alpha_factor = alpha[:, :, np.newaxis] / 255.0
        img = (alpha_factor * img_rgb + (1 - alpha_factor) * white_bg).astype(np.uint8)
    elif len(img.shape) == 3 and img.shape[2] == 3:  # RGB/BGR image
        pass  # Already in correct format
    else:
        return None  # Invalid format
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to make it purely black and white
    _, binary = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
    
    # Resize to standard size for comparison
    binary = cv2.resize(binary, (300, 300))
    
    return binary

def extract_shape_descriptor(binary_img):
    """Extract shape context descriptor"""
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shape_descriptor = np.zeros(binary_img.shape, dtype=np.uint8)
    cv2.drawContours(shape_descriptor, contours, -1, 255, 1)
    return shape_descriptor

def compute_perceptual_hash(binary_img, hash_size=16):
    """Compute perceptual hash for the image"""
    resized = cv2.resize(binary_img, (hash_size, hash_size))
    avg_pixel = resized.mean()
    diff = resized > avg_pixel
    hash_value = 0
    for bit in diff.flatten():
        hash_value = (hash_value << 1) | bit
    return hash_value, diff

def compare_logos(query_img_path, threshold=0.85):
    """Compare query logo against all logos in database"""
    query_binary = preprocess_logo(query_img_path)
    if query_binary is None:
        return None, None
    
    query_shape = extract_shape_descriptor(query_binary)
    query_hash, query_hash_array = compute_perceptual_hash(query_binary)
    
    exact_match = None
    other_matches = []
    logos = Logo.objects.all()
    
    for logo in logos:
        try:
            db_logo_path = logo.logo_image.path
            comp_binary = preprocess_logo(db_logo_path)
            if comp_binary is None:
                continue
                
            comp_shape = extract_shape_descriptor(comp_binary)
            comp_hash, comp_hash_array = compute_perceptual_hash(comp_binary)
            
            # Calculate similarities
            hash_distance = hamming(query_hash_array.flatten(), comp_hash_array.flatten())
            hash_similarity = 1 - hash_distance
            shape_similarity, _ = ssim(query_shape, comp_shape, full=True)
            binary_similarity, _ = ssim(query_binary, comp_binary, full=True)
            
            combined_score = (0.4 * binary_similarity + 
                            0.4 * shape_similarity + 
                            0.2 * hash_similarity)
            
            if combined_score >= threshold:
                if exact_match is None or combined_score > exact_match['similarity']:
                    exact_match = {
                        'logo': logo,
                        'similarity': combined_score,
                        'shape_sim': shape_similarity,
                        'binary_sim': binary_similarity,
                        'hash_sim': hash_similarity
                    }
            elif combined_score >= 0.65:
                other_matches.append({
                    'logo': logo,
                    'similarity': combined_score,
                    'shape_sim': shape_similarity,
                    'binary_sim': binary_similarity,
                    'hash_sim': hash_similarity
                })
        except Exception as e:
            continue
    
    other_matches.sort(key=lambda x: x['similarity'], reverse=True)
    return exact_match, other_matches[:9]

def artistscan(request):
    result = None
    portraits = []
    exact_match = None
    other_matches = []

    if request.method == 'POST' and request.FILES.get('logo'):
        input_logo = request.FILES['logo']
        input_logo_path = default_storage.save(f"temp/{input_logo.name}", input_logo)
        input_logo_full_path = default_storage.path(input_logo_path)

        exact_result, other_results = compare_logos(input_logo_full_path)
        
        if exact_result is None and not other_results:
            result = "No matches found or invalid image format."
        else:
            if exact_result:
                result = (f"Exact match found! Logo created by: {exact_result['logo'].user.username} "
                         f"(Similarity: {exact_result['similarity']:.2f})")
                portraits = Portraits.objects.filter(artist=exact_result['logo'].user)
                exact_match = {
                    'username': exact_result['logo'].user.username,
                    'path': exact_result['logo'].logo_image.url,
                    'similarity': f"{exact_result['similarity']:.3f}",
                    'shape_sim': f"{exact_result['shape_sim']:.2f}",
                    'binary_sim': f"{exact_result['binary_sim']:.2f}",
                    'hash_sim': f"{exact_result['hash_sim']:.2f}"
                }
            
            if other_results:
                other_matches = [{
                    'username': r['logo'].user.username,
                    'path': r['logo'].logo_image.url,
                    'similarity': f"{r['similarity']:.3f}",
                    'shape_sim': f"{r['shape_sim']:.2f}",
                    'binary_sim': f"{r['binary_sim']:.2f}",
                    'hash_sim': f"{r['hash_sim']:.2f}"
                } for r in other_results]

        default_storage.delete(input_logo_path)

    return render(request, 'artistscanlogo.html', {
        'result': result,
        'portraits': portraits,
        'exact_match': exact_match,
        'other_matches': other_matches
    })


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order  # Adjust according to your models
from django.contrib import messages
def cod_payment(request,id):
    portrait = get_object_or_404(Portraits, id=id)
    portrait.is_sold = True
    portrait.save()
    if request.method == 'POST':
        email = request.session.get('email')
      
        user = Buyer.objects.get(email=email)  
        order = Order.objects.create(
            user=user,
            portrait=portrait,
            status='Pending',  
        )
        order.save()
        
        
        return redirect('ordersuccess')  
    return HttpResponse("Invalid request method.", status=405)
def order_success(request):
    return render(request, 'order_success.html')

def manage_orders(request):
    orders = Order.objects.all()  
    return render(request, 'orders.html', {'orders': orders})
def artorders(request):
    email = request.session.get('email')  # Get the email from session
    if not email:
        return redirect('login')  # Redirect to login if email is missing

    try:
        artist = Artist.objects.get(email=email)
        orders = Order.objects.filter(portrait__artist=artist)  # Fetch orders for the artist
        return render(request,'artorders.html', {'orders': orders})
    except Artist.DoesNotExist:
        return redirect('login') 

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):  # Ensure valid status
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
            
            subject = f"Your Order #{order.id} Status Update"
            message = f"Dear {order.user.username},\n\nYour order status has been updated to: {new_status}.\n\nThank you for shopping with us!"
            recipient_email = order.user.email  # Assuming Buyer model has an email field

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Ensure this is set in settings.py
                [recipient_email],
                fail_silently=False,
            )
        else:
            messages.error(request, "Invalid status update.")
    return redirect('manage_orders')

def my_orders(request):
    email = request.session.get('email')  # Fetch the email from session
    if not email:
        return redirect('login')  # Redirect to login if email is not in session
    
    orders = Order.objects.filter(user__email=email).order_by('status') 
    pays = Payment.objects.filter(buyer__email=email).order_by('date') 
    # Fetch orders for logged-in user
    return render(request, 'myorders.html', {'orders': orders,'pays': pays})

def chat_list(request):
    artists = Artist.objects.all()
    buyers = Buyer.objects.all()
    return render(request, 'chat_list.html', {'artists': artists, 'buyers': buyers})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Artist, Buyer, ChatMessage

def chat_detail(request, user_type, username):
    sender_email = request.session.get('email')  # Assuming email is stored in the session

    if not sender_email:
        return redirect('login')  # Redirect to login if email is not in session

    # Determine the sender user type (Artist or Buyer)
    sender = None
    if Artist.objects.filter(email=sender_email).exists():
        sender = Artist.objects.get(email=sender_email)
    elif Buyer.objects.filter(email=sender_email).exists():
        sender = Buyer.objects.get(email=sender_email)

    if not sender:
        return redirect('login')  # Redirect if sender cannot be identified

    # Determine the receiver
    if user_type == 'artist':
        receiver = get_object_or_404(Artist, username=username)
    else:
        receiver = get_object_or_404(Buyer, username=username)

    # Fetch chat messages between the sender and receiver
    messages = ChatMessage.objects.filter(
        sender__in=[sender.username, username],
        receiver__in=[sender.username, username]
    ).order_by('timestamp')

    # Handle sending a message
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')  # Fetch the media file from the form

        if content.strip() or media:
            # Create a new chat message
            chat_message = ChatMessage.objects.create(
                sender=sender.username,
                receiver=username,
                content=content,
                media=media if media else None
            )

        return redirect('chat_detail', user_type=user_type, username=username)

    # Process media types for display
    for message in messages:
        if message.media:
            # Classify the media type (image or video)
            if message.media.name.endswith(('.jpg', '.jpeg', '.png')):
                message.media_type = 'image'
            elif message.media.name.endswith(('.mp4', '.avi', '.mov')):
                message.media_type = 'video'
            else:
                message.media_type = 'unknown'

    return render(request, 'chat_detail.html', {
        'receiver': receiver,
        'messages': messages,
        'sender': sender
    })
    
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Spam, PostModel

def report_post(request, post_id):
    post = get_object_or_404(PostModel, id=post_id)
    artist = post.user  # The artist who created the post

    spam, created = Spam.objects.get_or_create(artist=artist)
    spam.increment_report()

    return HttpResponse(
        "<script>alert('Post reported successfully!'); window.location=document.referrer;</script>")
    
    
def spamlist(request):
    spammers = Spam.objects.all()
    return render(request, 'spamlist.html', {'spammers': spammers})

def report_portrait(request, portrait_id):
    portrait = get_object_or_404(Portraits, id=portrait_id)
    artist = portrait.artist  # The artist who created the portrait

    spam, created = Spam.objects.get_or_create(artist=artist)
    spam.increment_report()

    return HttpResponse(
        "<script>alert('Portrait reported successfully!'); window.location=document.referrer;</script>"
    )
    
    
