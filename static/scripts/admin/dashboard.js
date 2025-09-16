const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');
const progress = document.getElementById('progress');
const progressFill = document.getElementById('progressFill');
const csrfToken = document.querySelector('meta[name="more_of_page"]').getAttribute('content')

// workbooks
fileInput.addEventListener('change', () => {
    if (fileInput.files.length === 0) return;

    // جمع‌آوری اطلاعات فرم
    const formData = new FormData();
    formData.append('title', uploadForm.title.value);
    formData.append('description', uploadForm.description.value);
    formData.append('csrf_token', csrfToken);

    for (const file of fileInput.files) {
        formData.append('files', file);
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/admin/upload-multiple');

    // نمایش درصد پیشرفت
    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            progressFill.style.width = percent + '%';
            progress.textContent = `در حال آپلود: ${percent}%`;
        }
    });

    // بعد از اتمام آپلود
    xhr.addEventListener('load', () => {
        if (xhr.status === 201) {
            progress.textContent = '✅ همه فایل‌ها با موفقیت آپلود شدند';
            progressFill.style.width = '100%';
        } else {
            progress.textContent = '❌ خطا در آپلود فایل‌ها';
        }
    });

    xhr.send(formData);
});


// users
const fileInput_user = document.getElementById('fileInput_user');
const progress_user = document.getElementById('progress_user');
const progressFill_user = document.getElementById('progressFill_user');

fileInput_user.addEventListener('change', () => {
  if (fileInput_user.files.length === 0) return;

  const formData = new FormData();
  formData.append('file', fileInput_user.files[0]);
  formData.append('csrf_token', csrfToken);


  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/admin/upload-users');

  xhr.upload.addEventListener('progress', (e) => {
    if (e.lengthComputable) {
      const percent = Math.round((e.loaded / e.total) * 100);
      progressFill_user.style.width = percent + '%';
      progress_user.textContent = `در حال آپلود: ${percent}%`;
    }
  });

  xhr.addEventListener('load', () => {
    if (xhr.status === 201) {
      progress_user.textContent = '✅ فایل با موفقیت آپلود شد و کاربران ساخته شدند';
      progressFill_user.style.width = '100%';
    } else {
      progress_user.textContent = '❌ خطا در آپلود یا ساخت کاربران';
      progressFill_user.style.width = '0%';
    }
  });

  xhr.addEventListener('error', () => {
    progress_user.textContent = '❌ خطای شبکه در هنگام ارسال فایل';
  });

  xhr.send(formData);
});