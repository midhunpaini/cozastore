document.querySelector('.img-btn').addEventListener('click', function()
	{
		document.querySelector('.cont').classList.toggle('s-signup')
	}
);

$(document).on('submit','#signin_form',function(e){
	e.preventDefault();
	email=  $('#email').val(),
    password  = $('#password').val()
	console.log(email,password)
	$.ajax({
		url: '/signin',
		type: "POST",
		dataType: "json",
		data: {
			email: $('#email').val(),
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
	mobile=  $('#mobile').val(),
	otp = $('#otp').val(),
	console.log(mobile)
	$.ajax({
		url: '/otp_login',
		type: "POST",
		dataType: "json",
		data: {
			mobile: $('#mobile').val(),
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		},
		
		success: (data) => {
			console.log(data)
			
			if(data.message==undefined){
				console.log('you are herer')
				document.getElementById('otpinput').style.display = 'block';
				document.getElementById('otp').setAttribute = 'required'
				document.getElementById('send_otp_btn').style.display = 'none';
				document.getElementById('signin_btn').style.display = 'block';
				$(document).on('submit','#otp_form',function(e){
					e.preventDefault();
					console.log(mobile)
					$.ajax({
						url: '/verify_otp',
						type: "POST",
						dataType: "json",
						data: {
							mobile: $('#mobile').val(),
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

$(document).on('submit','.register',function(e){
	e.preventDefault();
	$.ajax({
		url: '/signup',
		type: "POST",
		dataType: "json",
		data: {
			// uname: $('.name').val(),
			// email: $('.email').val(),
			// mobile: $('.mobile').val(),
			// password :$('.pass').val(),
			// conf_pass:$('.conf_pass').val(),
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
