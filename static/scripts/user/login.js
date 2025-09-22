//set top of login card
const el = document.querySelector('nav#navbar');
const heightNav = el.offsetHeight;
document.querySelector('.login-card').style.marginTop=`${heightNav + 52}px`;