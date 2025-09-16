function checking(event) {
    event.preventDefault();
    var password = document.querySelector("#password").value;
    var confirmPassword = document.querySelector("#password2").value;

    if (password !== confirmPassword) {
        Swal.fire({
            title: 'تکرار رمز عبور، صحیح نیست!',
            icon: 'error',
            confirmButtonColor: '#dc1225',
            confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i class="fa fa-times" style="margin-left:5px;"></i> باشه</div>',
            showCloseButton: true,
            allowOutsideClick:false,
        });
        return false;
    }
    document.querySelector("form.password_change").submit();
    return true;
}

document.getElementById('out').addEventListener('click',(e) => {
    Swal.fire({
        title: 'آیا میخواهید از حساب کاربری خود، خارج شوید؟',
        html: '',
        icon: 'warning',
        reverseButtons: true,
        showCancelButton: true,
        confirmButtonColor: '#F38524',
        confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i style="margin-left: 5px;" class="fa fa-times"></i> تایید</div>',
        cancelButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;border: 3 solid #ffd700;"><i style="margin-left: 5px;" class="fa fa-times"></i> انصراف</div>',
        showLoaderOnConfirm:true,
        allowOutsideClick:false,
        showCloseButton: false,
        focusConfirm: true,
    }).then((result)=> {
        if(result.value){
            const xhr = new XMLHttpRequest();
            var url = '/logout'
            xhr.open('GET',url, true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.send();
            setInterval(function() {location.reload()}, 1000); 
        };
    });
});