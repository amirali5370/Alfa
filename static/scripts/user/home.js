const colorbox = document.querySelectorAll(".up_top_user");
const ph_cir = document.querySelectorAll(".top_img");
const h = colorbox[0].offsetHeight;
const w = ph_cir[0].offsetWidth;
ph_cir.forEach((e)=>{
    e.style.top=(h-w/2)+'px'
})



const colors = [
    "#FF6B6B", // قرمز-مرجانی شاد
    "#FFD93D", // زرد طلایی
    "#6BCB77", // سبز تازه و زنده
    "#4D96FF", // آبی شاد و واضح
    "#FF9F1C", // نارنجی زنده
    "#845EC2", // بنفش پررنگ
    "#FF70A6", // صورتی پرانرژی
    "#00C9A7", // فیروزه‌ای شاد
    "#F9F871"  // زرد روشن و برجسته
  ];

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

const shuffledColors = shuffle([...colors]); // کپی آرایه

colorbox.forEach((box, index) => {
    box.style.backgroundColor = shuffledColors[index];
    box.parentNode.style.boxShadow= `0px 0px 15px 0px ${shuffledColors[index]}`
  });



const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
        item.classList.toggle('active');
    });
});
  