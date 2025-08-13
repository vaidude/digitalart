from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    path('home/', views.artist_home, name='home'),
    path('profile/', views.artist_profile, name='profile'),
    path('edit_profile/<int:uid>/', views.artist_edit_profile, name='edit_profile'),
    path('register/', views.artist_register, name='register'),
    path('login/', views.artist_login, name='login'),
    # path('view_notifications/',views.view_notifications, name='view_notifications'),
    path('buyers-list/', views.buyers_list, name='buyers_list'),
    path('terms/',views.terms,name='terms'),
    path('buyer_home/', views.buyer_home, name='buyer_home'),
    path('buyer_profile/', views.buyer_profile, name='buyer_profile'),
    path('buyer/profile/edit/<int:uid>/', views.buyer_edit_profile, name='buyer_edit_profile'),
    path('buyerregister/', views.buyer_register, name='buyerregister'),
    path('buyerlogin/', views.buyer_login, name='buyerlogin'),

    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('artistlist/', views.artistlist, name='artistlist'),
    path('artistdelete/<int:id>/', views.delete_artist, name='delete_artist'),
    path('buyerlist/', views.buyer_list, name='buyerlist'),
    path('delete_buyer/<int:buyer_id>/', views.delete_buyer, name='delete_buyer'),

    path('logout/', views.logout, name='logout'),
    path('art/', views.art_creation, name='art'),

    path('logo_gallery/',views.logo_gallery,name='logo_gallery'),
    path('logo_creation/',views.logo_creation,name='logo_creation'),
    path('edit_logo/<int:logo_id>/', views.edit_logo, name='edit_logo'),
    path('preview_logo/<int:logo_id>/', views.preview_logo, name='preview_logo'),
    path('delete_logo/<int:logo_id>/',views.delete_logo,name='delete_logo'),

    path('add_portrait/',views.add_portrait,name='add_portrait'),
    path('portrait_gallery/',views.portrait_gallery,name='portrait_gallery'),
    path('productlist/',views.productlist,name='productlist'),
    
    
    path('purchase/<int:portrait_id>/',views.purchase,name='purchase'),
    path('paymentsuccess/',views.payment_success,name='paymentsuccess'),
    
    
    path('feedback/', views.feedback, name="feedback"),
  
    path('feedback_list/',views.feedback_list, name='feedback_list'),
    path('submit_feedback/<int:portrait_id>/', views.submit_feedback, name='submit_feedback'),
    path('userfeedlist/',views.userfeedlist,name='userfeedlist'),
    
    
    path('compare_logo/',views.compare_logo, name="compare_logo"),
    path('artistscan/',views.artistscan,name='artistscan'),
    
    path('create_post/',views.createPost,name='create_post'),
    path('display_posts/',views.displayPosts,name='display_posts'),
    path('likePost/<int:id>/',views.likePost,name='likePost'),
    path('add_comment/<int:post_id>/',views.addComment,name='add_comment'),
    path('u_like_post/<int:post_id>/',views.u_likePost,name='u_like_post'),
    path('u_add_comment/<int:post_id>/',views.u_addComment,name='u_add_comment'),
    
    path('report/<int:post_id>/', views.report_post, name='report_post'),
    path('report-portrait/<int:portrait_id>/', views.report_portrait, name='report_portrait'),
    
    path('spams/', views.spamlist, name='spams'),
    
    path('viewpost/',views.viewpost,name='viewpost'),
    path('deletepost/<int:id>',views.deletepost,name='deletepost'),
    path('comments_delete/<int:cmt_id>/',views.commentsDelete,name='comments_delete'),
    path('editepost/<int:id>/',views.editepost,name='editepost'),
    
    path('codpayment/<int:id>', views.cod_payment, name='codpayment'),
    path('ordersuccess/',views.order_success,name='ordersuccess'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('artorders/', views.artorders, name='artorders'),
    path('myorders/', views.my_orders, name='myorders'),
    path('update/<int:order_id>/', views.update_order_status, name='update'),
    
    
    
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<str:user_type>/<str:username>/', views.chat_detail, name='chat_detail'),
    
    
]
