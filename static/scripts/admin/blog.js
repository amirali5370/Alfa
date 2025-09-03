const container = document.querySelector(".news-container");

// داده‌ها از attribute
let currentPage = parseInt(container.dataset.currentPage);
let hasNext = container.dataset.hasNext === "true";
const csrfToken = document.querySelector('meta[name="more_of_page"]').getAttribute('content')

let isLoading = false;

// لود بیشتر وقتی اسکرول رسید انتها
window.addEventListener("scroll", () => {
    if (!hasNext || isLoading) return;

    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
        loadMore();
    }
});

function loadMore() {
    isLoading = true;
    document.getElementById("loading").style.display = "flex";

    fetch(`/admin/api/blog?page=${currentPage + 1}`, {
        method: 'GET', // GET برای لود داده‌ها
        headers: {
            'X-CSRF-TOKEN': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(res => res.json())
    .then(data => {
        // اضافه کردن هر خبر به DOM
        data.items.forEach(item => {
            let article = document.createElement("article");
            article.classList.add("news-card");
            article.innerHTML = `
                <img src="${item.image}" alt="خبر ${item.id}">
                <div class="news-content">
                    <h2 class="news-title">${item.title}</h2>
                    <p class="news-desc">${item.description}</p>
                    <a href="${item.url}" class="read-more">ویرایش خبر</a>
                    <span class="news-date">منتشر شده در ${item.jalali_date}</span> 
                </div>
            `;
            container.appendChild(article);
        });

        // آپدیت مقادیر صفحه و hasNext
        currentPage++;
        hasNext = data.has_next;
        isLoading = false;
        document.getElementById("loading").style.display = "none";
    })
    .catch(err => {
        console.error("Error loading more news:", err);
        isLoading = false;
        document.getElementById("loading").style.display = "none";
    });
}
