const faqItems = document.querySelectorAll('.faq-item');
console.log(faqItems);

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
        item.classList.toggle('active');
    });
});



