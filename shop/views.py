from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product,Contact,Order,OrderUpdate
import json

def index(request):
    products=Product.objects.all()
    n=len(products)
    nSlides=n//4+ceil((n/4)-(n//4))
    #params={'product':products,'no_of_slides':n,'range':range(1,nSlides)}
    #allProd=[[products,n,range(1,nSlides)],[products,nSlides,range(1,nSlides)]]
    allProd=[]
    catprod=Product.objects.values('category','id')
    cats={item['category'] for item in catprod}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        allProd.append([prod,nSlides,range(1,nSlides)])
    params={"allProd":allProd}
    return render(request,'shop/index.html',params)
def aboutus(request):
    return render(request,'shop/about.html')
def contactus(request):
    if(request.method=="POST"):
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        msg=request.POST.get('msg','')
        contact=Contact(name=name,email=email,phone=phone,desc=msg)
        contact.save()
        thanks=True
        return render(request,'shop/contact.html',{"thanks":thanks})

    return render(request,'shop/contact.html')
def tracker(request):
    if(request.method=="POST"):
        orderid=request.POST.get('orderid','')
        email=request.POST.get('email','')
        try:
            order=Order.objects.filter(order_id=orderid,email=email)
            if(len(order)>0):
                    update=OrderUpdate.objects.filter(orderid=orderid)
                    updates=[]
                    for item in update:
                        updates.append({'text':item.updatedesc,'time':item.timestamp})
                        response=json.dumps([updates,order[0].item_json],default=str)
                    return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request,'shop/tracker.html')
def checkout(request):
    if(request.method=="POST"):
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        item_json=request.POST.get('item_json','')
        zipcode=request.POST.get('zipcode','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address','')+request.POST.get('address2','')
        order=Order(amount=amount,item_json=item_json,name=name,email=email,address=address,city=city,state=state,zipcode=zipcode,phone=phone)
        order.save()
        ids=order.order_id
        orderupdate=OrderUpdate(orderid=ids,updatedesc="Your order has been places")
        orderupdate.save()
        thanks=True
        
        return render(request,'shop/checkout.html',{'thanks':thanks,"ids":ids})
    return render(request,'shop/checkout.html')

def productview(request,myid):
    product=Product.objects.get(id=myid)
    params={"product":product}
    return render(request,'shop/productview.html',params)
    # {% for i in product|slice:"1:" %}
def searchMatch(query,item):
    if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False
def search(request):
    query=request.GET.get('search')
    allProd=[]
    catprod=Product.objects.values('category','id')
    cats={item['category'] for item in catprod}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nSlides=n//4 + ceil((n/4)-(n//4))
        if(len(prod)>0):
            allProd.append([prod,nSlides,range(1,nSlides)])
    params={"allProd":allProd,'msg':""}
    if len(allProd)==0 or len(query)<4:
        params={'msg':'Please make sure to enter relevant search query'}
    return render(request,'shop/search.html',params)