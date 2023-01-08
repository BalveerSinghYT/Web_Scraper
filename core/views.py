from django.shortcuts import render
import requests
import bs4

def home(request):
    context = {}
    if request.method == "POST":
        search = request.POST['search']
        amz = get_product_details_amz(search)
        flip = get_product_details_flipkart(search)
        context = {
            'amz':amz,
            'flip':flip
        }
    return render(request, "core/home.html", context=context)

def get_product_details_amz(product_name):
    url = f'https://www.amazon.in/s?k={product_name}'
    params = {'k':product_name}
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2',
    }
    data = requests.get(url, headers=headers)
    
    soup = bs4.BeautifulSoup(data.content, 'lxml')
    products = []
    for i in soup.select('.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.AdHolder.sg-col.s-widget-spacing-small.sg-col-12-of-16'):
        product_img = i.select_one('.s-image').get('src'),
        product_name = i.select_one('.a-size-medium.a-color-base.a-text-normal').text.strip()
        product_price = i.select_one('.a-price-whole').text.strip()
        rating = i.select_one('.a-section.a-spacing-none.a-spacing-top-micro').text.strip()[:3]
        if '₹' in rating:
            rating = '-'

        href = i.select_one('.a-link-normal.a-text-normal').get('href')

        products.append({
            'product_img':product_img,
            'product_name':product_name,
            'product_price':product_price,
            'rating':rating,
            'href':href,
        })
    print(products)
    return products

def get_product_details_flipkart(product_name):
    url = f'https://www.flipkart.com/search?q={product_name}'
    params = {'q':product_name}
    headers = {
        'User-Agent': 'PostmanRuntime/7.29.2',
    }
    data = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(data.content, 'lxml')

    products = []
    for i in soup.select('._2kHMtA'):
        product_img = i.select_one('._396cs4').get('src'),
        product_name = i.select_one('._4rR01T').text.strip()
        product_price = i.select_one('._30jeq3._1_WHN1').text.strip()
        rating = soup.find('div',class_="_3LWZlK").text.strip()
        href = i.select_one('._1fQZEK').get('href')

        products.append({
            'product_img':product_img,
            'product_name':product_name,
            'product_price':product_price,
            'rating':rating,
            'href':href,
        })

    return products
    