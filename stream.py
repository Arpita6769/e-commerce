import streamlit as st
import requests

BASE_URL = 'http://127.0.0.1:5000'

st.title('🛒 Ecommerce App')

menu = st.sidebar.selectbox('Menu', [
    'Register',
    'Login',
    'Products',
    'Place Order',
    'Order History',
    'Reviews'
])

if menu == 'Register':
    st.header('Register')
    name     = st.text_input('Name')
    email    = st.text_input('Email')
    password = st.text_input('Password', type='password')
    role     = st.selectbox('Role', ['user', 'seller', 'admin'])

    if st.button('Register'):
        res = requests.post(f'{BASE_URL}/auth/register',
                            json={'name': name, 'email': email,
                                  'password': password, 'role': role})
        if res.status_code == 201:
            st.success(res.json().get('message'))
        else:
            st.error(res.json().get('error'))

elif menu == 'Login':
    st.header('Login')
    email    = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        res = requests.post(f'{BASE_URL}/auth/login',
                            json={'email': email, 'password': password})
        if res.status_code == 200:
            st.success(f"Welcome! User ID: {res.json()['user_id']}, Role: {res.json()['role']}")
        else:
            st.error(res.json().get('error'))



elif menu == 'Products':
    st.header('All Products')
    res = requests.get(f'{BASE_URL}/products/')
    if res.status_code == 200:
        st.dataframe(res.json())

    st.divider()
    st.subheader('Add a Product')
    seller_id   = st.number_input('Seller ID',   min_value=1)
    category_id = st.number_input('Category ID', min_value=1)
    name        = st.text_input('Product Name')
    description = st.text_area('Description')
    price       = st.number_input('Price',     min_value=0.0, format='%f')
    stock_qty   = st.number_input('Stock Qty', min_value=1)

    if st.button('Add Product'):
        res = requests.post(f'{BASE_URL}/products/add',
                            json={'seller_id': int(seller_id), 'category_id': int(category_id),
                                  'name': name, 'description': description,
                                  'price': price, 'stock_qty': int(stock_qty)})
        if res.status_code == 201:
            st.success(res.json().get('message'))
        else:
            st.error(res.json().get('error'))


elif menu == 'Place Order':
    st.header('Place Order')
    user_id    = st.number_input('User ID',    min_value=1)
    product_id = st.number_input('Product ID', min_value=1)
    quantity   = st.number_input('Quantity',   min_value=1)
    method     = st.selectbox('Payment Method', ['cash', 'card', 'upi'])

    if st.button('Place Order'):
        res = requests.post(f'{BASE_URL}/orders/place',
                            json={'user_id': int(user_id), 'product_id': int(product_id),
                                  'quantity': int(quantity), 'method': method})
        if res.status_code == 201:
            st.success(res.json().get('message'))
        else:
            st.error(res.json().get('error'))


elif menu == 'Order History':
    st.header('Order History')
    user_id = st.number_input('User ID', min_value=1)

    if st.button('Fetch Orders'):
        res = requests.get(f'{BASE_URL}/orders/history/{int(user_id)}')
        if res.status_code == 200:
            data = res.json()
            if data:
                st.dataframe(data)
            else:
                st.warning('No orders found for this user')
        else:
            st.error(res.json().get('error'))


elif menu == 'Reviews':
    st.header('Product Reviews')
    product_id = st.number_input('Product ID', min_value=1)

    if st.button('Get Ratings'):
        res = requests.get(f'{BASE_URL}/reviews/{int(product_id)}')
        if res.status_code == 200:
            data = res.json()
            if data:
                st.metric('Average Rating', f"{data['avg_rating']} ⭐")
                st.metric('Total Reviews',  data['TOTAL_REVIEWS'])
            else:
                st.warning('No reviews yet for this product')
        else:
            st.error(res.json().get('error'))

    st.divider()
    st.subheader('Add a Review')
    st.info(f'Adding review for Product ID: {int(product_id)}') 
    user_id = st.number_input('Your User ID', min_value=1)
    rating  = st.slider('Rating', 1, 5)
    comment = st.text_area('Comment')

    if st.button('Submit Review'):
        res = requests.post(f'{BASE_URL}/reviews/add',
                            json={'product_id': int(product_id), 'user_id': int(user_id),
                                  'rating': rating, 'comment': comment})
        if res.status_code == 201:
            st.success(res.json().get('message'))
        else:
            st.error(res.json().get('error'))