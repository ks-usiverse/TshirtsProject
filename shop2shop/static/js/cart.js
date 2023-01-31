var upatedBtns = document.getElementsByClassName('cart-update')

for(var i =0 ; i <upatedBtns.length; i++ ){
    upatedBtns[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productID:',productID , 'action:',action  )

        console.log('user:',user)
        if(user == 'AnonymousUser'){
            addCookieItem(productID,action)

        }else{
            updateUserOrder(productID,action)
        }
    })
}

function addCookieItem(productID,action){
    console.log('login failed!!')
    if (action == 'add'){
        if (cart[productID] == undefined){
            cart[productID] = {'quantity':1}
        }else {
            cart[productID]['quantity'] += 1
        }

    }
    if (action == 'remove'){
        cart[productID]['quantity'] -= 1
        if (cart[productID]['quantity'] <= 0){
            console.log('product deleted')
            delete cart[productID];
        }
    }
    console.log('Cart:', cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}

function updateUserOrder(productID,action){
    console.log('send info after login')

    var url ='/update_item/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken

        },
        body:JSON.stringify({'productID': productID,'action' : action})

    })

    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()

    })

}