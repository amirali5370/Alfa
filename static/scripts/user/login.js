const csrfToken = document.querySelector('meta[name="more_of_page"]').getAttribute('content')

const starsContainer = document.getElementById('stars');
const divElement=document.querySelector('#content')
let width = divElement.offsetWidth;
let height = divElement.offsetHeight;
const numberOfStars = Math.ceil(width*height/2500);
for (let i = 0; i < numberOfStars; i++) {
  const star = document.createElement('div');
  star.classList.add('star');
  star.style.top = `${Math.random() * height}px`;
  star.style.left = `${Math.random() * (width-10)}px`;
  star.style.animationDelay = `${Math.random() * 2}s`;
  starsContainer.appendChild(star);
}


// function c(){
//   Swal.fire({
//       title: 'رمزعبور جدید',
//       html: `<form class="log" action="/ch_passw" method="post">
//                     <input type="hidden" name="csrf_token" value="${csrfToken}" />
//                     <div class="form-group" style="display: flex;
//                       flex-direction: column;
//                       align-items: center;">
//                         <label for="code">کدملی (از وارد کردن شماره تلفن خودداری کنید!)</label>
//                         <input name="code" type="text" id="code" class="log" placeholder="مثال : 0371234567" required inputmode="numeric" pattern="^[0-9]{10}$" maxlength="10" minlength="10" oninput="this.value = this.value.replace(/[^0-9]/g, '');">
//                         <button type="submit" class="login-btn" style="margin-right:40%;">دریافت رمز جدید</button>
//                     </div>
//               </form>`,

//       icon: 'warning',
//       showCloseButton: true,
//       showConfirmButton: false,
//       showLoaderOnConfirm:true,
//       allowOutsideClick:false,
//   }).then((result) => {swal.close();})
// };