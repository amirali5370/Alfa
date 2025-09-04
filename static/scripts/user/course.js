const csrfToken = document.querySelector("meta[name='more_of_page']").getAttribute("content");
const u_p_p = document.querySelector("meta[name='url_p_']").getAttribute("content");
const url = document.querySelector("meta[name='url_ap_']").getAttribute("content");
document.querySelectorAll(".course-card").forEach(item => {
    item.addEventListener('click', e => {
        let course_name = e.currentTarget.dataset.coT
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ "course_auth": e.currentTarget.dataset.coA })
        })
        .then(res => res.json())
        .then(data => {
            // اضافه کردن هر خبر به DOM
            const sections = data.items
            let htmlContent = '';
            sections.forEach((sec, index) => {
            htmlContent += `
                <a href="${u_p_p}${sec.auth}"><div class="swal-section" id="swal-section-${index}">
                <h4>${sec.title}</h4>
                </div></a>
            `;
            });
            Swal.fire({
                title: `قسمت های دوره:<br>${course_name}`,
                html: htmlContent,
                width: '90%',
                maxWidth: 650,
                showConfirmButton: false,
                showCloseButton: true,
                customClass: { popup: 'scrollable-sweetalert' }
              });
          
        })
        .catch(err => {
            console.error("Error loading more news:", err);
        });
    });
});