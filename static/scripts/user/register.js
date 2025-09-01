function validatePasswords() {
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
    return true;
}


function checking(event) {
    // جلوگیری از submit پیش‌فرض فرم
    event.preventDefault();

    if (!validatePasswords()) {
        return false;
    }
    const form = document.querySelector("form.log");
    const url = form.dataset.checkUrl;  
    var code = document.querySelector("input[name='code']").value;
    var data = { 'code': code };
    const csrfToken = document.querySelector("meta[name='more_of_page']").getAttribute("content");


    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(status => {
        if (status.result === true) {
            Swal.fire({
                title: 'مشخصات قبلا در سامانه ثبت شده!',
                html: 'این مشخصات قبلا در سامانه ثبت شده است. لطفا مشخصات دیگری وارد کنید.',
                icon: 'warning',
                confirmButtonColor: '#ffc000',
                confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i class="fa fa-times" style="margin-left:5px;"></i> تائید</div>',
                showCloseButton: true,
                allowOutsideClick: false
            });
        } else {
            // اگه همه چیز اوکی بود → فرم دستی submit کن
            form.submit();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false; // جلوگیری از submit پیش‌فرض
}
