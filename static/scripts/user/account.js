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