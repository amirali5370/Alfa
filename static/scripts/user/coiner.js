    const input = document.getElementById('numInput');
    const signBadge = document.getElementById('signBadge');
    const btnUp = document.getElementById('btnUp');
    const btnDown = document.getElementById('btnDown');
    const errorDiv = document.getElementById('error');

    const MIN = 10; // حداقل مقدار
    const STEP = 1; // گام ثابت

    function sanitizeDigits(value){
      if(!value) return '';
      let s = value.replace(/[^0-9]/g,'');
      if(s.length > 1) s = s.replace(/^0+/, '') || '0';
      return s;
    }

    input.addEventListener('input', (e)=>{
      const old = e.target.value;
      const cleaned = sanitizeDigits(old);
      if(old !== cleaned){
        const pos = e.target.selectionStart - (old.length - cleaned.length);
        e.target.value = cleaned;
        e.target.setSelectionRange(pos, pos);
      }
      validateAndShow();
    });

    input.addEventListener('keydown', (e)=>{
      const allowedKeys = ['Backspace','Tab','ArrowLeft','ArrowRight','Delete','Home','End'];
      if(allowedKeys.includes(e.key)) return;
      const isNumber = /^[0-9]$/.test(e.key);
      if(isNumber) return;
      e.preventDefault();
    });

    input.addEventListener('paste', (e)=>{
      const txt = (e.clipboardData || window.clipboardData).getData('text');
      const cleaned = sanitizeDigits(txt);
      if(cleaned !== txt){
        e.preventDefault();
        const start = input.selectionStart;
        const end = input.selectionEnd;
        const newVal = input.value.slice(0,start) + cleaned + input.value.slice(end);
        input.value = sanitizeDigits(newVal);
        validateAndShow();
      }
    });

    function parseIntSafe(s){
      if(!s) return NaN;
      const n = Number(s);
      return Number.isInteger(n) ? n : NaN;
    }

    function validateAndShow(){
      const v = input.value;
      const n = parseIntSafe(v);
      if(v === ''){ hideError(); updateBadge(); return; }
      if(Number.isNaN(n)){
        showError('ورودی باید عدد صحیح باشد');
        updateBadge();
        return;
      }
      if(n < MIN){
        showError('تعداد سکه ها برای خرید نمی تواند کمتر از ' + MIN + ' باشد');
      } else {
        hideError();
      }
      updateBadge();
    }

    function showError(msg){ errorDiv.style.display = 'block'; errorDiv.textContent = msg; input.setAttribute('aria-invalid','true'); }
    function hideError(){ errorDiv.style.display = 'none'; errorDiv.textContent = ''; input.removeAttribute('aria-invalid'); }

    function updateBadge(){
      const n = parseIntSafe(input.value);
      if(Number.isNaN(n)){
        signBadge.textContent = '#';
        signBadge.style.background = 'linear-gradient(180deg,#f0f7ff,#e6f0fb)';
        signBadge.style.color = 'var(--accent)';
      } else {
        signBadge.textContent = n >= MIN ? '✓' : '⚠';
        if(n >= MIN){ signBadge.style.background = 'linear-gradient(180deg,#e6fbff,#e6f9f6)'; signBadge.style.color = 'green'; }
        else { signBadge.style.background = 'linear-gradient(180deg,#fff6f6,#fff2f2)'; signBadge.style.color = 'var(--danger)'; }
      }
    }

    function changeBy(delta){
      const cur = parseIntSafe(input.value);
      if(Number.isNaN(cur)){
        const base = MIN;
        const next = Math.max(base, base + delta);
        input.value = String(next);
      } else {
        const next = cur + delta;
        input.value = String(Math.max(0, next));
      }
      validateAndShow();
    }

    btnUp.addEventListener('click', ()=> changeBy(STEP));
    btnDown.addEventListener('click', ()=> changeBy(-STEP));

    input.addEventListener('keydown', (e)=>{
      if(e.key === 'ArrowUp'){ e.preventDefault(); changeBy(STEP); }
      if(e.key === 'ArrowDown'){ e.preventDefault(); changeBy(-STEP); }
    });

    updateBadge();
    
    function getValidatedValue(){
        const n = parseIntSafe(input.value);
        if (Number.isNaN(n) || n < MIN) return null;
        return n;
      }
      
