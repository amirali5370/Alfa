const url = document.querySelector("meta[name='res_u']").getAttribute("content");
const csrfToken = document.querySelector("meta[name='more_of_page']").getAttribute("content");

document.querySelectorAll("button.report").forEach(item => {
    item.addEventListener('click', e => {
        let quiz_id = e.target.dataset.re;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': csrfToken
            },
            body: JSON.stringify({ "quiz_id" : quiz_id })
        })
        .then(response => response.json())
        .then(status => {
                Swal.fire({
                    title: `نمره شما از این آزمون : ${status.result} درصد`,
                    html: '',
                    icon: 'success',
                    confirmButtonColor: '#3f9b0b',
                    confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i class="fa fa-times" style="margin-left:5px;"></i> تائید</div>',
                    showCloseButton: true,
                    allowOutsideClick: false
                });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});