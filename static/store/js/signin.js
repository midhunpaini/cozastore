
$(document).on('submit','#signin_form',function(e){
	e.preventDefault();
	email=  $('#email_email').val(),
    password  = $('#password').val()
	console.log(email,password)
	$.ajax({
		url: '/signin',
		type: "POST",
		dataType: "json",
		data: {
			email: $('#email_email').val(),
			password: $('#password').val(),
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		},
		
		success: (data) => {
			console.log(data)
			
			if(data.message==undefined){
				console.log('verified......')
				window.location.href = "/";
			}else{
				document.getElementById('errormessage').innerHTML = data.message;
			}						 
		},
		error: (error) => {
			console.log('error')
			console.log(error);
		  },
	});
});

$('#send_otp_btn').on('click',function(e){
	e.preventDefault();
	mobile=  $('#login_mobile').val(),
	otp = $('#otp').val(),
	console.log(mobile)
	$.ajax({
		url: '/otp_login',
		type: "POST",
		dataType: "json",
		data: {
			mobile: $('#login_mobile').val(),
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		},
		
		success: (data) => {
			console.log(data)
			
			if(data.message==undefined){
				document.getElementById('otpinput').style.display = 'inline';
				document.getElementById('send_otp_btn').style.display = 'none';
				document.getElementById('submit_otp').style.display = 'inline';
				$(document).on('submit','#otp_form',function(e){
					e.preventDefault();
					console.log(mobile)
					$.ajax({
						url: '/verify_otp',
						type: "POST",
						dataType: "json",
						data: {
							mobile: $('#login_mobile').val(),
							otp:  $('#otp').val(),
							csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
						},
						
						success: (data) => {
							console.log(data)
							
							if(data.message==undefined){
								window.location.href = "/";
							}else{
								document.getElementById('errorotp').innerHTML = data.message;
							}						 
						},
						error: (error) => {
							console.log(error);
						  },
					});
				});
			}else{
				document.getElementById('errorotp').innerHTML = data.message;
			}						 
		},
		error: (error) => {
			console.log(error);
		  },
	});
});

$(document).on('submit','#register',function(e){
	let uname = $('#name').val()
	let email = $('#email').val()
	console.log(uname,email)
	e.preventDefault();
	$.ajax({
		url: '/signup',
		type: "POST",
		dataType: "json",
		data: {
			uname: $('#name').val(),
			email: $('#email').val(),
			mobile: $('#mobile').val(),
			password :$('#pass').val(),
			conf_pass:$('#conf_pass').val(),
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		},
		
		success: (data) => {
			console.log(data)
			
			if(data.error_message==undefined){
				window.location.href = "/";
			}else{
				document.getElementById('error').innerHTML = data.error_message;
			}						 
		},
		error: (error) => {
			console.log(error);
		  },
	});

	
});

$('#login_id').on('click', function(){
	console.log('working')
	$("#register_form").css("display", "none");
	$("#email_login").css("display", "block");
});

$('#login_otp_btn').on('click', function(){
	console.log('working')
	$("#otp_login").css("display", "block");
	$("#email_login").css("display", "none");
});

$('.register_btn').on('click', function(){
	console.log('working')
	$("#otp_login").css("display", "none");
	$("#email_login").css("display", "none");
	$("#register_form").css("display", "block");
});
