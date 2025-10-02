// scroll navbar
const navbar = document.querySelector("#navbar");
// let last_scroll = 0;

// window.addEventListener("scroll",() => {
    
//     let scrollY = window["scrollY"];
//     if (true==false){
//         return
//     };        
//     if (last_scroll>scrollY){
//         navbar.style.top = "0";
//     } else if(scrollY>60) {
//         navbar.style.top = (navbar.offsetHeight + 15)* -1 + "px";
//     };
//     last_scroll = scrollY;
// },
// {passive: true}
// );

// document.querySelector(".form_fo>.button").addEventListener("click", function(e) {
//     const inputs = this.parentNode.querySelectorAll("input, textarea");
//     inputs.forEach(input => input.value = "");
// });

document.querySelector("#content").style.top = navbar.offsetHeight + "px"

