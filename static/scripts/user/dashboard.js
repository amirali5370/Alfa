// پیام دعوت
const ms_inv_button = document.getElementById('inv_bt'); 
ms_inv_button.addEventListener('click', () => {
  const message = encodeURIComponent(`سلام! این کد دعوت شما است \n ${ms_inv_button.parentNode.querySelector('.invite-code').innerText}`);
  let smsLink;
    if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
      smsLink = `sms:&body=${message}`;  // iOS
    } else {
      smsLink = `sms:?body=${message}`;  // Android
    }
  window.location.href = smsLink;
});


//پیام دعوت معاون
const sub_inv_button = document.getElementById('inv_sub_bt');
sub_inv_button.addEventListener('click', () => {

    const phoneNumber = sub_inv_button.parentNode.querySelector('input').value; // شماره مورد نظر را اینجا وارد کن
    const message = encodeURIComponent(`سلام! این کد دعوت معاون شما است \n ${sub_inv_button.parentNode.parentNode.querySelector('.invite-code').innerText}`);
    let smsLink;
    if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
      smsLink = `sms:${phoneNumber}&body=${message}`;  // iOS
    } else {
      smsLink = `sms:${phoneNumber}?body=${message}`;  // Android
    }
    window.location.href = smsLink;
  });



// کپی کد ها
const copy_al = document.querySelector('#copy_al')
const copy_boxs = document.querySelectorAll('.invite-code')
copy_boxs.forEach(el => {
    el.addEventListener("click", async () => {
        try {
            const text = el.innerText
            if (navigator.clipboard && navigator.clipboard.writeText) {
              // روش مدرن
              await navigator.clipboard.writeText(text);
            } else {
              // روش قدیمی (fallback برای موبایل/سافاری)
              const textarea = document.createElement("textarea");
              textarea.value = text;
              textarea.style.position = "fixed"; // برای جلوگیری از اسکرول
              textarea.style.opacity = "0";
              document.body.appendChild(textarea);
              textarea.focus();
              textarea.select();
              document.execCommand("copy");
              document.body.removeChild(textarea);
            }
      
            // انیمیشن موفقیت
            copy_al.style.opacity = '1';
            setTimeout(() => copy_al.style.opacity = '0', 1500);
      
          } catch (err) {
            console.error("کپی کردن متن موفق نبود:", err);
          }
    });
})




//سایز باکس آدرس
document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.querySelector("textarea");
  if (!textarea) return;

  const FONT_SIZE = 14;         // px
  const LINE_HEIGHT = 1.6;      // line-height
  const MAX_CHARS = 150;
  const AVG_CHAR_WIDTH = 7.5;   // px، تقریبی برای Vazir 14px
  const PADDING = 20;           // px، جمع پدینگ بالا و پایین

  const adjustHeight = () => {
    const width = textarea.clientWidth;
    // تعداد کاراکترهایی که در هر خط جا می‌شن
    const charsPerLine = Math.floor(width / AVG_CHAR_WIDTH);
    // تعداد خطوط مورد نیاز برای MAX_CHARS
    const linesNeeded = Math.ceil(MAX_CHARS / charsPerLine);
    // تنظیم ارتفاع نهایی
    textarea.style.height = `${linesNeeded * LINE_HEIGHT * FONT_SIZE + PADDING}px`;
  };

  // محاسبه اولیه
  adjustHeight();

  // محاسبه مجدد در صورت تغییر اندازه پنجره
  window.addEventListener("resize", adjustHeight);
});



const url_switch_sub = document.querySelector("meta[name='url_of_']").getAttribute("content");

document.querySelectorAll('.assistant>.btn').forEach(item => {
	item.addEventListener('click', (e) => {
		const csrfToken = document.querySelector("meta[name='more_of_page']").getAttribute("content");
		const invite_id = e.target.parentNode.dataset.object;
		var data = {
			'invite_id':invite_id,
			'do':e.target.classList.contains('secondary') ? "deactivate" : "activate"
		}

		fetch(url_switch_sub, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRF-TOKEN': csrfToken
			},
			body: JSON.stringify(data)
		})
		.then(response => response.json())
		.then(status => {
			if(status.result=="200"){
			Swal.fire({
				title: 'وضعیت معاون با موفقیت تغییر کرد!',
				html: 'حداکثر ۳ معاون فعال می‌تواند وجود داشته باشد.<br>جمعاً ۱۰ معاون (فعال یا غیرفعال) قابل تعریف است.',
				icon: 'success',
				confirmButtonColor: '#3f9b0b',
				confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i style="margin-left: 5px;" class="fa fa-times"></i> تائید</div>',
				showCloseButton: true,
				showLoaderOnConfirm:true,
				allowOutsideClick:false,
			}).then((result) => {swal.close();window.location.reload();})
		}else if(status.result=="403"){
			Swal.fire({
				title: 'تعداد معاونان فعال بیش از حد مجاز!',
				html: '',
				icon: 'error',
				confirmButtonColor: '#dc1225',
				confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i style="margin-left: 5px;" class="fa fa-times"></i> تائید</div>',
				showCloseButton: true,
				showLoaderOnConfirm:true,
				allowOutsideClick:false,
			}).then((result) => {swal.close();window.location.reload();})
		}
		})
		.catch(error => {console.error('Error:', error);
			window.location.reload();
		});
	});
});




const csrfToken = document.querySelector("meta[name='more_of_page']").getAttribute("content");
document.querySelector('#buy_coin').addEventListener('click',(e)=>{
  const coins = getValidatedValue()
  if (coins === null){return null}
  var data = {
    'coins':coins
  }

  fetch('/payment', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-TOKEN': csrfToken
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {window.location.href = data.url;})
});