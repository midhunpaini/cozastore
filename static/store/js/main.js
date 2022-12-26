

(function ($) {
    "use strict";

    /*[ Load page ]
    ===========================================================*/
    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<div class="loader05"></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: [ 'animation-duration', '-webkit-animation-duration'],
        overlay : false,
        overlayClass : 'animsition-overlay-slide',
        overlayParentElement : 'html',
        transition: function(url){ window.location.href = url; }
    });
    
    /*[ Back to top ]
    ===========================================================*/
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display','flex');
        } else {
            $("#myBtn").css('display','none');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });


    /*==================================================================
    [ Fixed Header ]*/
    var headerDesktop = $('.container-menu-desktop');
    var wrapMenu = $('.wrap-menu-desktop');

    if($('.top-bar').length > 0) {
        var posWrapHeader = $('.top-bar').height();
    }
    else {
        var posWrapHeader = 0;
    }
    

    if($(window).scrollTop() > posWrapHeader) {
        $(headerDesktop).addClass('fix-menu-desktop');
        $(wrapMenu).css('top',0); 
    }  
    else {
        $(headerDesktop).removeClass('fix-menu-desktop');
        $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
    }

    $(window).on('scroll',function(){
        if($(this).scrollTop() > posWrapHeader) {
            $(headerDesktop).addClass('fix-menu-desktop');
            $(wrapMenu).css('top',0); 
        }  
        else {
            $(headerDesktop).removeClass('fix-menu-desktop');
            $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
        } 
    });


    /*==================================================================
    [ Menu mobile ]*/
    $('.btn-show-menu-mobile').on('click', function(){
        $(this).toggleClass('is-active');
        $('.menu-mobile').slideToggle();
    });

    var arrowMainMenu = $('.arrow-main-menu-m');

    for(var i=0; i<arrowMainMenu.length; i++){
        $(arrowMainMenu[i]).on('click', function(){
            $(this).parent().find('.sub-menu-m').slideToggle();
            $(this).toggleClass('turn-arrow-main-menu-m');
        })
    }

    $(window).resize(function(){
        if($(window).width() >= 992){
            if($('.menu-mobile').css('display') == 'block') {
                $('.menu-mobile').css('display','none');
                $('.btn-show-menu-mobile').toggleClass('is-active');
            }

            $('.sub-menu-m').each(function(){
                if($(this).css('display') == 'block') { console.log('hello');
                    $(this).css('display','none');
                    $(arrowMainMenu).removeClass('turn-arrow-main-menu-m');
                }
            });
                
        }
    });


    /*==================================================================
    [ Show / hide modal search ]*/
    $('.js-show-modal-search').on('click', function(){
        $('.modal-search-header').addClass('show-modal-search');
        $(this).css('opacity','0');
    });

    $('.js-hide-modal-search').on('click', function(){
        $('.modal-search-header').removeClass('show-modal-search');
        $('.js-show-modal-search').css('opacity','1');
    });

    $('.container-search-header').on('click', function(e){
        e.stopPropagation();
    });


    /*==================================================================
    [ Isotope ]*/
    var $topeContainer = $('.isotope-grid');
    var $filter = $('.filter-tope-group');

    // filter items on button click
    $filter.each(function () {
        $filter.on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $topeContainer.isotope({filter: filterValue});
        });
        
    });

    // init Isotope
    $(window).on('load', function () {
        var $grid = $topeContainer.each(function () {
            $(this).isotope({
                itemSelector: '.isotope-item',
                layoutMode: 'fitRows',
                percentPosition: true,
                animationEngine : 'best-available',
                masonry: {
                    columnWidth: '.isotope-item'
                }
            });
        });
    });

    var isotopeButton = $('.filter-tope-group button');

    $(isotopeButton).each(function(){
        $(this).on('click', function(){
            for(var i=0; i<isotopeButton.length; i++) {
                $(isotopeButton[i]).removeClass('how-active1');
            }

            $(this).addClass('how-active1');
        });
    });

    /*==================================================================
    [ Filter / Search product ]*/
    $('.js-show-filter').on('click',function(){
        $(this).toggleClass('show-filter');
        $('.panel-filter').slideToggle(400);

        if($('.js-show-search').hasClass('show-search')) {
            $('.js-show-search').removeClass('show-search');
            $('.panel-search').slideUp(400);
        }    
    });

    $('.js-show-search').on('click',function(){
        $(this).toggleClass('show-search');
        $('.panel-search').slideToggle(400);

        if($('.js-show-filter').hasClass('show-filter')) {
            $('.js-show-filter').removeClass('show-filter');
            $('.panel-filter').slideUp(400);
        }    
    });




    /*==================================================================
    [ Cart ]*/
    $('.js-show-cart').on('click',function(){
        console.log('youare at cart')
        $("#your_cart").load(" #your_cart > *");
        $("#side_cart").load(" #side_cart > *");
        $('.js-panel-cart').addClass('show-header-cart');
    });

    $('.js-hide-cart').on('click',function(){
        $('.js-panel-cart').removeClass('show-header-cart');
    });

    /*==================================================================
    [ Cart ]*/
    $('.js-show-sidebar').on('click',function(){
        $('.js-sidebar').addClass('show-sidebar');
    });

    $('.js-hide-sidebar').on('click',function(){
        $('.js-sidebar').removeClass('show-sidebar');
    });

    /*==================================================================
    [ +/- num product ]*/
    $('.btn-num-product-down').on('click', function(){
        var numProduct = Number($(this).next().val());
        var product_id = $(this).prev().val();
        if(numProduct > 1) $(this).next().val(numProduct - 1);
        var price_id = $(this).prev().attr("pid");
        var item_id = 'total_item_price'+product_id
        $.ajax({
            url: '/modify_cart',
            type: "POST",
            dataType: "json",
            data: JSON.stringify({numProduct: numProduct, product_id: product_id, change : 'minus', total_price: total_price}),
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,  
            },
            
            success: (data) => {
                if(data.sucess == true){
                    document.getElementById(price_id).innerHTML = '₹ '+data.total_price    
                    document.getElementById('total_price').innerHTML = '₹ '+data.cart_price
                    document.getElementById('discount_total_price').innerHTML = '₹ '+data.total_discount
                    document.getElementById('sub_total_price').innerHTML = '₹ '+data.sub_total
                    // document.getElementById(item_id).innerHTML = '₹ '+data.total_item_price
                    document.getElementById('data-notify').setAttribute('data-notify',data.new_quantity)
                }else{
                    
                    swal('','Product out of stock', 'warning')
                } 
            },
            error: (error) => {
              console.log(error);
            }
          });
    });
    
    $('.btn-num-product-up').on('click', function(){
        var numProduct = Number($(this).prev().val());
        if(numProduct < 10) $(this).prev().val(numProduct + 1);
        var product_id = $(this).next().val();
        var price_id = $(this).next().attr("pid");
        
        console.log(price_id)
        
        $.ajax({
            url: '/modify_cart',
            type: "POST",
            dataType: "json",
            data: JSON.stringify({numProduct: numProduct, product_id: product_id, change : 'plus'}),
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,  
            },
            success: (data) => {

                document.getElementById(price_id).innerHTML = '₹ '+data.total_price    
                document.getElementById('total_price').innerHTML = '₹ '+data.cart_price
                document.getElementById('discount_total_price').innerHTML = '₹ '+data.total_discount
                document.getElementById('sub_total_price').innerHTML = '₹ '+data.sub_total
                document.getElementById('data-notify').setAttribute('data-notify',data.new_quantity)
            },
            error: (error) => {
              console.log(error);
            }
          });
    });

    $('.del_item').on('click',function(){
        let product_id = $(this).next().val();
        let div_id = 'table'.concat(product_id) 
        console.log($(this).next())
        console.log(div_id)
        $.ajax({
            url: '/del_cart_item',
            type: "POST",
            dataType: "json",
            data: JSON.stringify({ product_id: product_id}),
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,  
            },
            success: (data) => {
                document.getElementById(div_id).remove();
                document.getElementById('total_price').innerHTML = '₹ '+ data.cart_price;
                document.getElementById('data_notify').setAttribute('data-notify',data.cart_items);
                let cart_id = 'side_cart'+product_id
                document.getElementById(cart_id).style.display = 'none'
                if(data.cart_items < 1){
                    window.location.href = "/";
                }
                
            },
            error: (error) => {
                console.log(error);
              },
        });
    });
    
    /*==================================================================
    [ Rating ]*/
    $('.wrap-rating').each(function(){
        var item = $(this).find('.item-rating');
        var rated = -1;
        var input = $(this).find('input');
        $(input).val(0);

        $(item).on('mouseenter', function(){
            var index = item.index(this);
            var i = 0;
            for(i=0; i<=index; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });

        $(item).on('click', function(){
            var index = item.index(this);
            rated = index;
            $(input).val(index+1);
        });

        $(this).on('mouseleave', function(){
            var i = 0;
            for(i=0; i<=rated; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });
    });
    
    /*==================================================================
    [ Show modal1 ]*/
    $('.js-show-modal1').on('click',function(e){
        e.preventDefault();
        $('.js-modal1').addClass('show-modal1');
        
        $.ajax({
            url: '/modal',
            type: "POST",
            dataType: "json",
            data: {
                product_id : $(this).prev().val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: (data) => {
                console.log(data)
                document.getElementById('product_price').innerHTML = '₹ '+data.data.product_price;
                document.getElementById('product_name').innerHTML = data.data.product_name;
                document.getElementById('product_description').innerHTML = data.data.product_description;
                document.getElementById('product_color').innerHTML = data.data.product_color;
                document.getElementById('product_size').innerHTML = data.data.product_size;
                document.getElementById('product_id2').value = data.data.product_id;
                document.getElementById('cartitemcount').value = data.data.product_id;
                document.getElementById('product_name2').value = data.data.product_name;
                document.getElementsByName('product_img')[0].src = data.data.product_image;
                document.getElementsByName('product_img')[1].src = data.data.product_image;
                document.getElementsByName('product_img')[2].src = data.data.product_image;
                document.getElementsByName('product_img')[3].src = data.data.product_image;
                document.getElementsByName('product_img')[4].src = data.data.product_image;
                document.getElementsByName('product_img')[5].src = data.data.product_image;
                
            },
            error: (error) => {
                console.log(error);
              },
        });
    });

    $('#add_cart_button').on('click',function(e){
        e.preventDefault()
        let product_name = $(this).next().next().val()
        console.log(product_name+'dfasdfasdfasdfasdf')
        
        $.ajax({
            url: '/cart',
            type: "POST",
            dataType: "json",
            data: {
                color:$('#color_select').val(),
                size:$('#size_select').val(),
                product_id: $(this).next().val(),
                cart_count: 1,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                swal(product_name, "is added to cart !", "success");
                document.getElementById('data_notify').setAttribute('data-notify',data.cart_items)		 
            },
            error: (error) => {
                console.log(error);
              },
        });
   
    });


    $('.js-hide-modal1').on('click',function(){
        $('.js-modal1').removeClass('show-modal1');
        // $("#add_to_cart").load(" #add_to_cart > *");
        // location.reload()
    });
    // [ +/- num product modal ]*/
    $('.btn-num-product-down2').on('click', function(){
        var numProduct = Number($(this).next().val());
        if(numProduct > 0) $(this).next().val(numProduct - 1);
    });

    $('.btn-num-product-up2').on('click', function(){
        var numProduct = Number($(this).prev().val());
        if(numProduct < 10)$(this).prev().val(numProduct + 1);
    });

    //order////////////////////////////////
    
    $(document).on('submit','#order_form',function(e){
        e.preventDefault();
        $("#added_add").load(" #added_add > *");
        let payment_option = $('input[name="payment_option"]:checked').val()
        let address_option = $('input[name="address_option"]:checked').val()
        console.log('***** ',address_option,'***********************')
        if(payment_option=='razorpay'){
            $('#rzp-button1').html('Make Payment')
        }
        $.ajax({
            url: '/order',
            type: "POST",
            dataType: "json",
            data: {
                fname: $('#fname').val(),
                lname: $('#lname').val(),
                email: $('#email').val(),
                pincode: $('#pincode').val(),
                phone: $('#phone').val(),
                state: $('#state').val(),
                address1: $('#address1').val(),
                address2: $('#address2').val(),
                discount: $('#discount_amount').attr('dis'),
                save_address: $('#save_address').is(':checked'),
                payment_option:$('input[name="payment_option"]:checked').val(),
                address_option:$('input[name="address_option"]:checked').val(),
                coupon_code:$('#coupon_input').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                
                console.log(data)
                console.log('success')
         
                
                if(data.error==true){
                    swal(data.message, "!", "error");
                }
                else if(data.payment=='paypal'){                   
                    let price = data.cart_total
                    let paypal_id = data.paypal_id
                    // $('input[name="payment_option"]').hide(),
                    paypal.Buttons({
                       
                        // Set up the transaction
                        createOrder: function(data, actions) {
                            return actions.order.create({
                                purchase_units: [{
                                    amount: {
                                        value: price
                                    }
                                }]
                            });
                        },
            
                        // Finalize the transaction
                      
                        onApprove: function(data, actions) {
                            return actions.order.capture().then(function(orderData) {
                                // Successful capture! For demo purposes:
                                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
                                var transaction = orderData.purchase_units[0].payments.captures[0];                             
                               
                                $.ajax({
                                    url: '/paypal_success',
                                    type: "GET",
                                    dataType: "json",
                                    data: {
                                        paypal_id:paypal_id
                                    },
                                    success: (data) =>{
                                        console.log(data)
                                        console.log('paypal payment success')
                                        document.getElementById('data_notify').setAttribute('data-notify', '0')
                                        document.getElementById('order_page').style.display ='none'
                                        document.getElementById('order_success').style.display='block' 
                                    },
                                });
                                
                            });
                        }
            
            
                    }).render('#paypal-button-container');
                }
                else if(data.payment=='razorpay'){
                   
                    var amount = data.razorpay.amount
                    var id = data.razorpay.id
                    var razor_id = data.razor_id
                    console.log(data.razorpay.id)
                    var options = {
                        "key": razor_id, // Enter the Key ID generated from the Dashboard
                        "amount": amount, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "cozastore",
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        "order_id": id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (response){
                        
                            $.ajax({
                                url: '/razorpay_success',
                                type: "GET",
                                dataType: "json",
                                data: {
                                    razor_order_id:response.razorpay_order_id,
                                    razor_payment_id:response.razorpay_payment_id,
                                    razor_sign:response.razorpay_signature,
                                    order_search_id:id
                                },
                                success: (data) =>{
                                    console.log(data)
                                    document.getElementById('data_notify').setAttribute('data-notify', '0')
                                    document.getElementById('order_page').style.display ='none'
                                    document.getElementById('order_success').style.display='block'
                                    
                                },
                            });
                        },
                        
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.on('payment.failed', function (response){
                        console.log('razorpay payment failed')
                        $.ajax({
                            url: '/razorpay_failed',
                            type: "GET",
                            dataType: "json",
                            data: {
                                razor_order_id:razorpay_order_id,
                                razor_payment_id:response.razorpay_payment_id,
                                razor_sign:response.razorpay_signature,
                                order_search_id:id
                            },
                            success: (data) =>{
                                console.log(data)
                                console.log('payment failed')
                                
                                
                            },
                        });
            
                    });
                    document.getElementById('rzp-button1').onclick = function(e){
                        rzp1.open();
                        e.preventDefault();
                    }
                }
                else {
                    document.getElementById('data_notify').setAttribute('data-notify', '0')
                    document.getElementById('order_page').style.display ='none'
                    document.getElementById('order_success').style.display='block'
                    	
                }						 
            },
            error: (error) => {
                console.log(error);
              },
        });
    });
    
    

    $('#signup_order').on('click', function(){
        window.location.href = "/signin";
    });

    $('#customer_profile_address').on('click', function(){
        document.getElementById('customer_wishlist').style.display = 'none';
        document.getElementById('customer_orders').style.display = 'none';
        document.getElementById('customer_addresses').style.display = 'block';
        document.getElementById('customer_account').style.display = 'none';  
        document.getElementById('customer_password').style.display = 'none';  
    });
    
    $('#customer_profile_orders').on('click', function(){
        document.getElementById('customer_wishlist').style.display = 'none';
        document.getElementById('customer_addresses').style.display = 'none';
        document.getElementById('customer_orders').style.display = 'block';
        document.getElementById('customer_account').style.display = 'none'; 
        document.getElementById('customer_password').style.display = 'none';      
    });

    $('#customer_profile_account').on('click', function(){
        document.getElementById('customer_wishlist').style.display = 'none';
        document.getElementById('customer_addresses').style.display = 'none';
        document.getElementById('customer_orders').style.display = 'none';
        document.getElementById('customer_account').style.display = 'block'; 
        document.getElementById('customer_password').style.display = 'none';     
    });

    $('#customer_profile_password').on('click', function(){
        document.getElementById('customer_wishlist').style.display = 'none';
        document.getElementById('customer_addresses').style.display = 'none';
        document.getElementById('customer_orders').style.display = 'none';
        document.getElementById('customer_account').style.display = 'none'; 
        document.getElementById('customer_password').style.display = 'block';     
    });

    $('#customer_profile_wishlist').on('click', function(){
        document.getElementById('customer_addresses').style.display = 'none';
        document.getElementById('customer_orders').style.display = 'none';
        document.getElementById('customer_account').style.display = 'none'; 
        document.getElementById('customer_password').style.display = 'none'; 
        document.getElementById('customer_wishlist').style.display = 'block';         
    });



    $('#goto_wish').on('click', function(e){      
        localStorage.setItem('wish',true)      
        location.href = '/profile' 
                
    });

   
    
      


    

    $('#customer_profile_cart').on('click', function(){
        $.ajax({
            url: '/check_cart',
            type: "GET",
            dataType: "json",
            success: (data) =>{
                if(data.cart_items==0){
                    swal('','Your Cart is Empty','warning') 
                }
                else{
                    window.location.href = "/cart";
                }
            },
        })
        
    });
    
    $('.delete_address').on('click', function(){
        let address_card = $(this).next().val()
        document.getElementById(address_card).remove()
    
        $.ajax({
            url: '/del_customer_address',
            type: "GET",
            dataType: "json",
            data: {
                address_id: $(this).next().val(),  
            },
            success: (data) =>{
                console.log(data) 
                swal('','Address deleted successfully','success')
            },
        })  
    });

     $(document).on('submit','#edit_acc_detail',function(e){
        e.preventDefault();
        let add = document.getElementById('profile_edit_name').value
        console.log(add)
        $.ajax({
            url: '/edit_account',
            type: "POST",
            dataType: "json",
            data: {
                user_name:$('#profile_edit_name').val(),
                email:$('#profile_edit_email').val(),
                mobile:$('#profile_edit_mobile').val(),
                password:$('#edit_profile_pass').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                if(data.error_message==undefined){
                   swal('','Account edited successfully','success')
                }else{
                    swal('', data.error_message,'error')
                }       
            },
            error: (error) => {
                console.log(error);
              },
        });
    });


    $(document).on('submit','#edit_acc_pass',function(e){
        e.preventDefault();
        let add = document.getElementById('profile_edit_name').value
        console.log(add)
        $.ajax({
            url: '/edit_password',
            type: "POST",
            dataType: "json",
            data: {
                current_pass:$('#current_password').val(),
                new_pass:$('#new_password').val(),
                conf_pass:$('#edit_confirm_password').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                if(data.error_message==undefined){
                   swal('','Password edited successfully','success')
                }else{
                    swal('', data.error_message,'error')
                }       
            },
            error: (error) => {
                console.log(error);
              },
        });
    });

    $('.edit_address').on('click', function(){
        let fname = $(this).next().val()
        let lname = $(this).next().next().val()
        let email = $(this).next().next().next().val()
        let mobile = $(this).next().next().next().next().val()
        let address1 = $(this).next().next().next().next().next().val()
        let address2 = $(this).next().next().next().next().next().next().val()
        let state = $(this).next().next().next().next().next().next().next().val()
        let pin = $(this).next().next().next().next().next().next().next().next().val()
        let address_id = $(this).next().next().next().next().next().next().next().next().next().val()
        document.getElementById('edit_fname').value = fname   
        document.getElementById('edit_lname').value = lname
        document.getElementById('edit_email').value = email
        document.getElementById('edit_mobile').value = mobile
        document.getElementById('edit_state').value = state
        document.getElementById('edit_address').value= address1
        document.getElementById('edit_address2').value = address2
        document.getElementById('edit_pin').value = pin
        document.getElementById('edit_address_id').value = address_id
    });

    $(document).on('submit','#edit_address_form',function(e){
        e.preventDefault();
        let add = document.getElementById('edit_lname').value
        console.log(add+'fsdfasggfsfhdh')
        $.ajax({
            url: '/edit_customer_address',
            type: "POST",
            dataType: "json",
            data: {
                fname:$('#edit_fname').val(),   
                lname:$('#edit_lname').val(),
                email:$('#edit_email').val(),
                mobile:$('#edit_mobile').val(),
                state:$('#edit_state').val(),
                address:$('#edit_address').val(),
                address2:$('#edit_address2').val(),
                pin:$('#edit_pin').val(),
                address_id:$('#edit_address_id').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                 console.log(data)
                 swal('','Address edited successfully','success')       
            },
            error: (error) => {
                console.log(error);
              },
        });
    });

    // $(document).on('submit','#add_address_form',function(e){
    //     e.preventDefault();
    //     let add = $('#add_address1').val()
    //    console.log(add + ' sdfasfgasdffgsdfgsd')
       
    //     $.ajax({
    //         url: '/add_customer_address',
    //         type: "POST",
    //         dataType: "json",
    //         data: {
    //             fname:$('#add_fname').val(),   
    //             lname:$('#add_lname').val(),
    //             email:$('#add_email').val(),
    //             mobile:$('#add_mobile').val(),
    //             state:$('#add_state').val(),
    //             address1:$('#add_address1').val(),
    //             address2:$('#add_address2').val(),
    //             pin:$('#add_pin').val(),
    //             address_id:$('#add_address_id').val(),
    //             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    //         },
            
    //         success: (data) => {
    //              console.log(data)
    //              swal('','Address edited successfully','success')
    //             //  $("#profile_address").load(" #profile_address > *");  
    //              $(window).load('#profile_address')     
    //         },
    //         error: (error) => {
    //             console.log(error);
    //           },
    //     });
    // });

    $('.customer_order_cancel').on('click', function(){
        let add = $(this).next().val()
        swal('',"Confirm Cancel !", "warning");
        console.log(add)
        $.ajax({
            url: '/cancel_order',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).next().val(),
                order_item_id: $(this).next().next().val(),
            },
            success: (data) =>{
                console.log(data)
               $(this).css('display','none')
               $(this).prev().css('display','block')
                
            },
        })  
    });

    $('.customer_order_return').on('click', function(e){
        e.preventDefault()
        let add = $(this).attr('cid')
        swal("Confirm Return !", "warning");
        console.log(add)
        $.ajax({
            url: '/return_order',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).attr('oid'),
                order_item_id: $(this).attr('cid')
            },
            success: (data) =>{
                console.log(data)
               $(this).css('display','none')
               $(this).prev().css('display','block')
               $(this).prev().prev().css('display','none')
               location.reload()
                
            },
        })  
    });


    $('.order-info-button').on('click', function(){
        let id = $(this).attr('oid')
        console.log(id)
        $.ajax({
            url: '/order_info',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).attr('oid'),
                order_item_id: $(this).attr('cid')
            },
            success: (data) =>{
                document.getElementById('order-info-name').innerHTML = '₹ '+data.product_name;
                document.getElementById('order-info-price').innerHTML = 'Price: ' + data.product_price;
                document.getElementById('order-info-color').innerHTML = 'Color: '+ data.product_color;
                document.getElementById('order-info-size').innerHTML = 'Size: '+ data.product_size;
                document.getElementById('order-info-quantity').innerHTML = 'Quantity: ' + data.product_quantity;
                document.getElementById('order-info-img').src = data.product_image;
            },
        })
    });


    $('#coupon_btn').on('click', function(){
        
        $.ajax({
            url: '/apply_coupon',
            type: "GET",
            dataType: "json",
            data: {
                coupon_code:$('#coupon_input').val(),   
         
            },
            
            success: (data) => {
                console.log(data)
                let sub_total = Number($('#sub_total').attr('sub'))
                let discount = Number(data.discount)
                let total_amount = data.cart_value
                 if(discount==0){
                    swal('','Invalid coupon code','warning') 
                    $('#discount_amount').html('00.0')
                    $('#order_total').html(sub_total) 
                 }else if(discount==-1){
                    swal('','Coupon code Expired','warning')
                    $('#discount_amount').html('00.0')
                    $('#order_total').html(sub_total)
                 }
                 else if(sub_total>500){
                    let total = sub_total - discount
                    $('#discount_amount').html(data.discount)
                    $('#order_total').html(total)
                    swal('','Coupon code applied','success') 
                 }
                 else{
                    swal('','Cart Total should be above ₹'+total_amount,'warning') 
                 }
                 
            },
            error: (error) => {
                console.log(error);
              },
        });
        
    });


    $('.delete_address').on('click', function(){
        let address_card = $(this).next().val()
        document.getElementById(address_card).remove()
    
        $.ajax({
            url: '/del_customer_address',
            type: "GET",
            dataType: "json",
            data: {
                address_id: $(this).next().val(),  
            },
            success: (data) =>{
                console.log(data) 
                swal('','Address deleted successfully','success')
            },
        })  
    });


    $('.js-addwish-b2').on('click', function(e){
        e.preventDefault();
    });

    $('.js-addedwish-b2').on('click', function(e){
        e.preventDefault();
    });

    $('.js-addwish-b2').each(function(){
        var nameProduct = $(this).parent().parent().find('.js-name-b2').html();
        $(this).on('click', function(){
            let p = $(this).attr('prd_id')
            console.log(p)
            $.ajax({
                url: '/wishlists',
                type: "GET",
                dataType: "json",
                data: {
                    product_id: $(this).attr('prd_id')
                },
                success: (data) =>{
                    console.log(data)

                    if(data.message==1){
                        swal(nameProduct, "is added to wishlist !", "success");
                        $('.wishlist_item_count').attr('data-notify',data.wish_count+1)
                        $(this).removeClass('js-addwish-b2')
                        $(this).addClass('js-addedwish-b2')
                    }else if(data.message==0){
                        $('.wishlist_item_count').attr('data-notify',data.wish_count-1)
                        swal(nameProduct, "Product removed from wishlist !", "warning");

                        $(this).removeClass('js-addedwish-b2')
                        $(this).addClass('js-addwish-b2')
                    }else if(data.message==2){
                        swal('', "Login to add product to wishlist !", "warning"); 
                    }
                },
            }) 
           
        });
    });

    $('.js-addedwish-b2').each(function(){
        var nameProduct = $(this).parent().parent().find('.js-name-b2').html();
        $(this).on('click', function(){
            $.ajax({
                url: '/wishlists',
                type: "GET",
                dataType: "json",
                data: {
                    product_id: $(this).attr('prd_id')
                },
                success: (data) =>{
                    if(data.message==1){
                        swal(nameProduct, "is added to wishlist !", "success");
                        $('.wishlist_item_count').attr('data-notify',data.wish_count+1)
                        $(this).removeClass('js-addwish-b2')
                        $(this).addClass('js-addedwish-b2')
                    }else if(data.message==0){
                        $('.wishlist_item_count').attr('data-notify',data.wish_count-1)
                        swal(nameProduct, " product removed from wishlist !", "warning");
                        $(this).removeClass('js-addedwish-b2')
                        $(this).addClass('js-addwish-b2')
                    }
                    else if(data.message==2){
                        swal('', "Login to add product to wishlist !", "warning"); 
                    }
                       
                },
            })           
        });
    });



    $('.js-addcart-detail').each(function(){
        var nameProduct = $(this).parent().parent().parent().parent().find('.js-name-detail').html();
        $(this).on('click', function(){
            swal(nameProduct, "is added to cart !", "success");
        });
    });



    $('.add_from_wishlist').on('click',function(e){
        e.preventDefault()
        let product_name = $(this).prev().val()
        let product_id = $(this).attr('pid')
        let card_id = 'wishlist_card'+product_id
        console.log(product_name+'dfasdfasdfasdfasdf')
        
        $.ajax({
            url: '/cart',
            type: "POST",
            dataType: "json",
            data: {
                product_id: $(this).attr('pid'),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                swal(product_name, "is added to cart !", "success");
                $.ajax({
                    url: '/remove_wishlists',
                    type: "GET",
                    dataType: "json",
                    data: {
                        product_id: product_id
                    },
                    success: (data) =>{
                        console.log(data)
                        $('.wishlist_item_count').attr('data-notify',data.wish_count)
                        document.getElementById(card_id).remove()
                        
                    },
                })
                $('.cart_count_noti').attr('data-notify',data.cart_count)	 
            },
            error: (error) => {
                console.log(error);
              },
        });
   
    });


    $('.remove_from_wishlist').on('click',function(e){
        e.preventDefault()
        let product_name = $(this).prev().prev().val()
        let product_id = $(this).attr('pid')
        let card_id = 'wishlist_card'+product_id
       
        
        $.ajax({
            url: '/remove_wishlists',
            type: "GET",
            dataType: "json",
            data: {
                product_id: $(this).attr('pid'),
              
            },
            
            success: (data) => {
                swal(product_name, "is removed from wishlist !", "error");
                
                $('.wishlist_item_count').attr('data-notify',data.wish_count)
                document.getElementById(card_id).remove() 
                if ($(card_id).attr('data-count')<1){
                    $('#empty_wish_pic1').css("display", "block");
                }
                if(product_name==undefined){
                    alert('empty wishlist')
                }
            },
            error: (error) => {
                console.log(error);
              },
        });
   
    });
    
      
     



    $('.choose-color').hide();

    $('.choose-size').on('change',function(){
        var color = $('#size_select').val()
        $('.choose-color').hide();
        $('.size'+color).show();
})
    

})(jQuery);



if(localStorage.getItem('wish')){     
document.getElementById('customer_wishlist').style.display = 'block';
document.getElementById('customer_orders').style.display = 'none';
localStorage.removeItem('wish')
}