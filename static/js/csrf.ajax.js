$(document).ready(function(){
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
          }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

//  TODO: PayPal
//  if ( !! document.getElementById('paypal-block')) {
//    let csrftoken = getCookie('csrftoken');
//    let url = "/cart/create-paypal-transaction/";
//    let order_done = false;
//
//    paypal.Buttons({
//      style: {
//        color:  'blue',
//        shape:  'pill',
//        label:  'pay',
//        height: 50
//      },
//
//      createOrder: function() {
//        return fetch(url, {
//          method: 'post',
//          headers: {
//            'content-type': 'application/json',
//            "X-CSRFToken": csrftoken,
//          }
//        }).then(function(data) {
//          let orderID = data.url.split('/')[7];
//          order_done = data.url;
//          return orderID;
//        });
//      },
//
//      onError: function(error) {
//        order_done = false;
//        location.replace('/cart/');
//        console.log(error);
//      },
//
//      onCancel: function() {
//        order_done = false;
//        location.replace('/');
//      }
//    }).render('#paypal-button-container');
//
//    setInterval(function(){
//      if(order_done){
//        if(! document.querySelector("[id^='paypal-overlay-']")) {
//          location.replace(order_done);
//        }
//      }
//    }, 1000);
//  }
})