var upatedBtns = document.getElementsByClassName('cart-update')

for(var i =0 ; i <upatedBtns.length; i++ ){
    upatedBtns[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productID:',productID , 'action:',action  )

        console.log('user:',user)
        if(user === 'AnonymousUser'){
            console.log('login failed')
        }else{
            updateUserOrder(productID,action)
        }
    })
}


function updateUserOrder(productID,action){
    console.log('You are now logged in, sending information')

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