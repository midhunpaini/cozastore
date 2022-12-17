(function ($){

    $('.confirm_order').on('click', function(){
    let id = $(this).next().val()
       console.log(id+' sadfjaskdfkjas')

       $.ajax({
        url: '/del_customer_address',
        type: "GET",
        dataType: "json",
        data: {
            address_id: $(this).next().val(),  
        },
        success: (data) =>{
            console.log(data)
            $("#profile_address_card").load(" #profile_address_card > *");
            
        },
    })
    });

    $('.cancel_order').on('click', function(){
        let id = $(this).prev().val()
           console.log(id+' sadfjaskdfkjas')
           $.ajax({
            url: '/admincancel_order_admin',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).prev().val(),
                order_item_id: $(this).next().val(),
            },
            success: (data) =>{
                console.log(data)
                // $("#cancel_order_button").load(" #cancel_order_button > *");
                location.reload()
                
            },
        })
    });
    

    $('.confirm_order_admin').on('click', function(){
            let id = $(this).next().val()
            console.log(id)
        $.ajax({
            url: '/adminconfirm_order_admin',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).next().val(),
            },
            success: (data) =>{
                console.log(data)
                location.reload()
                // $("#cancel_order_button").load(" #cancel_order_button > *");
                
            },
        })
    });

    $('.deliver_order_admin').on('click', function(){
        let id = $(this).next().val()
        console.log(id)
        $.ajax({
            url: '/admindeliver_order_admin',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).next().val(),
            },
            success: (data) =>{
                console.log(data)
                location.reload()
              
            },
        })
    });

    $('.ship_order_admin').on('click', function(){
        let id = $(this).next().val()
        console.log(id)
        $.ajax({
            url: '/adminship_order_admin',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).next().val(),
            },
            success: (data) =>{
                console.log(data)
                location.reload()
                // $("#cancel_order_button").load(" #cancel_order_button > *");
            },
        })
    });

    $('.refund_order_admin').on('click', function(){
        let id = $(this).next().val()
        console.log(id)
        $.ajax({
            url: '/adminrefund_order',
            type: "GET",
            dataType: "json",
            data: {
                order_id: $(this).next().val(),
            },
            success: (data) =>{
                console.log(data)
                location.reload()
                // $("#cancel_order_button").load(" #cancel_order_button > *");
            },
        })
    });

    $(".clickable-row").click(function() {

        // let cid = $(this).attr('cid')
        let oid = $(this).attr('oid')
      
       location.href='/admincustomer_order/'+oid
    });

    $("#get_report").click(function() {
    
        let from_date = $('#from_date').val()
        let to_date =$('#to_date').val()
        console.log(from_date)
        if(from_date==''||to_date==''){
            console.log(from_date)
            window.alert('Select date fields')
        }else{
            location.href='/adminfilter_report/' + from_date+'/'+ to_date
        }
        
    
    });

    $("#download_report").click(function() {
        let from_date = $('#from_date').val()
        let to_date =$('#to_date').val()
        if(from_date==''||to_date==''){
            console.log(from_date)
            window.alert('Select date fields')
        }else{
            window.open(/admindownload_report/+ from_date+'/'+ to_date, '_blank') 
            // location.href='/admindownload_report/' + from_date+'/'+ to_date
        }
    });

    $("#download_report_csv").click(function() {
        let from_date = $('#from_date').val()
        let to_date =$('#to_date').val()
        if(from_date==''||to_date==''){
            console.log(from_date)
            window.alert('Select date fields')
        }else{
            window.open(/admindownload_report_csv/+ from_date+'/'+ to_date, '_blank') 
            // location.href='/admindownload_report/' + from_date+'/'+ to_date
        }
    });



    $(document).on('submit','#add_coupon_form',function(e){
        e.preventDefault();  
        if($('#coupon_status').prop('checked')){
            coupon = true
        }
        else{
            coupon = false
        }
        $.ajax({
            url: '/adminset_coupon',
            type: "POST",
            dataType: "json",
            data: {
                coupon_name:$('#coupon_name').val(),   
                coupon_code:$('#coupon_code').val(),
                coupon_status:coupon,
                discount:$('#coupon_discount').val(),
                discount_type:$('#coupon_discount_type').val(),
                minimum_amount:$('#coupon_minimum_amount').val(),
                coupon_validity:$('#coupon_validity').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                 console.log(data)
                 swal('','Coupon added successfully','success')
                //  $("#profile_address").load(" #profile_address > *");  
                   
            },
            error: (error) => {
                console.log(error);
              },
        });
    });


    $(document).on('submit','#category_offer_form',function(e){
        e.preventDefault();  
        if($('#category_offer_status').prop('checked')){
            category = true
        }
        else{
            category = false
        }
        $.ajax({
            url: '/adminset_category_offer',
            type: "POST",
            dataType: "json",
            data: {
                category_name:$('#category_name').val(),   
                category_discount:$('#category_discount').val(),
              
                minimum_amount:$('#category_minimum_amount').val(),
                discount:$('#category_discount').val(),
                discount_type:$('#category_discount_type').val(),
                category_validity:$('#category_validity').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                 console.log(data)
                 swal('','Category offer added successfully','success')
                //  $("#profile_address").load(" #profile_address > *");  
                   
            },
            error: (error) => {
                console.log(error);
              },
        });
    });



    $(document).on('submit','#product_offer_form',function(e){
        e.preventDefault();  
      
        $.ajax({
            url: '/adminset_product_offer',
            type: "POST",
            dataType: "json",
            data: {
                product_name:$('#product_name').val(),   
                product_discount:$('#product_discount').val(),
                minimum_amount:$('#product_minimum_amount').val(),
                discount:$('#product_discount').val(),
                discount_type:$('#product_discount_type').val(),
                product_validity:$('#product_validity').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            
            success: (data) => {
                 console.log(data)
                 swal('','Category offer added successfully','success')
                //  $("#profile_address").load(" #profile_address > *");  
                   
            },
            error: (error) => {
                console.log(error);
              },
        });
    });

    $('.stop_offer').on('click', function(){
        let prev = $(this).prev().html()
       
        $.ajax({
            url: '/admincancel_offer',
            type: "POST",
            dataType: "json",
            data: {
                offer_id: $(this).val(),
                offer_type : $(this).attr('offer_type'),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: (data) =>{
                console.log(data)
                location.reload()
                // swal('',' offer Stopped successfully','success')
                
                
            },
        })
    });

    $('#monthly_report').change(function(){
        let month = $('#monthly_report').val()
        console.log(month,'******************')
        location.href=/adminmonthly_report/+ month
    });

})(jQuery);