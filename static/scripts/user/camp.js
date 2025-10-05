
const csrfToken = document.querySelector("meta[name='more_of_page']").getAttribute("content");
document.querySelectorAll('button.note-btn').forEach((button)=>{
    button.addEventListener('click',(e)=>{
        const auth = button.parentNode.parentNode.dataset.coA;
        const amo = button.parentNode.parentNode.dataset.coP;
        Swal.fire({
            title: `آیا از ثبت نام در این اردو با هزینه ${amo} سکه اطمینان دارید؟`,
            html: '',
            icon: 'warning',
            reverseButtons: true,
            showCancelButton: true,
            confirmButtonColor: '#dc1225',
            confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i style="margin-left: 5px;" class="fa fa-times"></i> بله</div>',
            cancelButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;border: 3 solid #ffd700;"><i style="margin-left: 5px;" class="fa fa-times"></i> انصراف</div>',
            showLoaderOnConfirm:true,
            allowOutsideClick:false,
            showCloseButton: false,
            focusConfirm: true,
        }).then((result) => {
        if(result.value){

            var data = {
                "auth":auth
              }
              fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRF-TOKEN': csrfToken
                },
                body: JSON.stringify(data)
              })
              .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
                })
                .then(data => {
                    if (data.result === "buy") {
                        Swal.fire({
                            title: 'خرید اردو موفقیت آمیز بود!',
                            html: '',
                            icon: 'success',
                            confirmButtonColor: '#3f9b0b',
                            confirmButtonText: '<div class="b123"><i class="i123 fa fa-times"></i> باشه</div>',
                            showCloseButton: true,
                            showLoaderOnConfirm:true,
                            allowOutsideClick:false,
                        }).then((result) => {swal.close();window.location.reload();})
                    } else if (data.result === "little") {
                        Swal.fire({
                            title: 'موجودی سکه های شما کافی نیست!',
                            html: "",
                            icon: 'error',
                            confirmButtonColor: '#dc1225',
                            confirmButtonText: '<div class="b123"><i class="i123 fa fa-times"></i> باشه</div>',
                            showCloseButton: true,
                            showLoaderOnConfirm:true,
                            allowOutsideClick:false,
                        }).then((result) => {swal.close();window.location.reload();})
                    } else {
                        return
                    }
                })
                .catch(error => {
                    console.error("خطا در ارتباط با سرور:", error);
                });

        };
        });
    });
});

