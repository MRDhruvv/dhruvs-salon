document.addEventListener('DOMContentLoaded', ()=>{
  const serviceCheckboxes = Array.from(document.querySelectorAll('.service-checkbox'));
  const estimateEl = document.getElementById('estimate');
  const form = document.getElementById('appointment-form');
  const clearBtn = document.getElementById('clearBtn');
  const modal = document.getElementById('modal');
  const modalBody = document.getElementById('modal-body');
  const closeModal = document.getElementById('closeModal');
  const modalOk = document.getElementById('modal-ok');

  function formatCurrency(n){ return '₹' + n.toFixed(2); }

  function updateEstimate(){
    let total = 0;
    serviceCheckboxes.forEach(cb=>{
      if(cb.checked) total += Number(cb.dataset.price || 0);
    });
    estimateEl.textContent = formatCurrency(total);
    return total;
  }

  serviceCheckboxes.forEach(cb=>cb.addEventListener('change', updateEstimate));

  clearBtn.addEventListener('click', ()=>{
    form.reset();
    updateEstimate();
  });

  function validateDateTime(dateStr, timeStr){
    if(!dateStr || !timeStr) return false;
    const now = new Date();
    // Parse date and time properly to avoid timezone issues
    const [year, month, day] = dateStr.split('-').map(Number);
    const [hours, minutes] = timeStr.split(':').map(Number);
    const sel = new Date(year, month - 1, day, hours, minutes);
    if(isNaN(sel)) return false;
    // No past appointments
    if(sel < now) return false;
    // Business hours 09:00 - 19:00
    const h = sel.getHours();
    if(h < 9 || h > 19) return false;
    return true;
  }

  function showModal(html){
    modalBody.innerHTML = html;
    document.body.classList.add('modal-open');
    modal.setAttribute('aria-hidden','false');
  }
  function hideModal(){
    document.body.classList.remove('modal-open');
    modal.setAttribute('aria-hidden','true');
  }

  closeModal.addEventListener('click', hideModal);
  modalOk.addEventListener('click', hideModal);

  form.addEventListener('submit', (e)=>{
    e.preventDefault();
    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const phone = form.phone.value.trim();
    const date = form.date.value;
    const time = form.time.value;
    const selected = serviceCheckboxes.filter(cb=>cb.checked).map(cb=>({label:cb.parentNode.textContent.trim(), price:Number(cb.dataset.price)}));

    if(!name || !email || !phone){
      alert('Please fill name, email and phone.');
      return;
    }
    if(selected.length === 0){
      alert('Please select at least one service.');
      return;
    }
    if(!validateDateTime(date,time)){
      alert('Please choose a valid future date/time during business hours (9:00-19:00).');
      return;
    }

    const total = updateEstimate();
    const appointment = {name,email,phone,date,time,services:selected,total,createdAt: new Date().toISOString()};

    // Save in localStorage (simple mock persistence)
    const list = JSON.parse(localStorage.getItem('appointments')||'[]');
    list.push(appointment);
    localStorage.setItem('appointments', JSON.stringify(list));

    // Build modal summary
    const servicesHtml = selected.map(s=>`<li>${s.label} — ₹${Number(s.price).toFixed(2)}</li>`).join('');
    const html = `
      <p>Thanks, <strong>${name}</strong> — your appointment is scheduled.</p>
      <ul>${servicesHtml}</ul>
      <p><strong>Date:</strong> ${date} <strong>Time:</strong> ${time}</p>
      <p><strong>Estimated Total:</strong> ${formatCurrency(total)}</p>
      <p class="small">We've saved your appointment locally. You'll receive a confirmation email shortly.</p>
    `;
    showModal(html);
    form.reset();
    updateEstimate();
  });

  // init
  updateEstimate();

  // Date/Time Popup Functionality
  const dateTimePopup = document.getElementById('dateTimePopup');
  const popupTitle = document.getElementById('popupTitle');
  const popupBody = document.getElementById('popupBody');
  const popupClose = dateTimePopup.querySelector('.popup-close');
  const dateInput = form.date;
  const timeInput = form.time;

  function hideDateTimePopup(){
    dateTimePopup.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
  }

  function showDateOptions(){
    popupTitle.textContent = 'Select Date';
    popupBody.innerHTML = '';
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    // Generate dates for next 30 days (excluding past dates)
    for(let i = 1; i <= 30; i++){
      const date = new Date(today);
      date.setDate(date.getDate() + i);
      
      // Skip Sundays
      if(date.getDay() === 0) continue;
      
      // Create date string from local date components (not UTC)
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const dateStr = `${year}-${month}-${day}`;
      
      const displayStr = date.toLocaleDateString('en-IN', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
      
      const option = document.createElement('button');
      option.type = 'button';
      option.className = 'popup-option';
      option.textContent = displayStr;
      option.dataset.value = dateStr;
      
      if(dateInput.value === dateStr){
        option.classList.add('selected');
      }
      
      option.addEventListener('click', (e) => {
        e.preventDefault();
        dateInput.value = dateStr;
        // Auto-show time picker
        setTimeout(showTimeOptions, 200);
      });
      
      popupBody.appendChild(option);
    }
    
    dateTimePopup.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
  }

  function convertTo12Hour(hour){
    if(hour === 0) return 12;
    if(hour > 12) return hour - 12;
    return hour;
  }

  function getAMPM(hour){
    return hour >= 12 ? 'PM' : 'AM';
  }

  function showTimeOptions(){
    popupTitle.textContent = 'Select Time';
    popupBody.innerHTML = '';
    
    // Generate times from 9:00 to 19:00 in 30-minute intervals
    for(let h = 9; h <= 19; h++){
      for(let m = 0; m < 60; m += 30){
        if(h === 19 && m > 0) break; // Stop at 19:00
        
        const timeStr = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
        const hour12 = convertTo12Hour(h);
        const ampm = getAMPM(h);
        const displayTime = `${String(hour12).padStart(2, '0')}:${String(m).padStart(2, '0')} ${ampm}`;
        
        const option = document.createElement('button');
        option.type = 'button';
        option.className = 'popup-option';
        option.textContent = displayTime;
        option.dataset.value = timeStr;
        
        if(timeInput.value === timeStr){
          option.classList.add('selected');
        }
        
        option.addEventListener('click', (e) => {
          e.preventDefault();
          timeInput.value = timeStr;
          hideDateTimePopup();
        });
        
        popupBody.appendChild(option);
      }
    }
    
    dateTimePopup.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
  }

  // Event listeners for date and time inputs
  dateInput.addEventListener('click', (e) => {
    e.preventDefault();
    showDateOptions();
  });

  timeInput.addEventListener('click', (e) => {
    e.preventDefault();
    if(!dateInput.value){
      alert('Please select a date first.');
      return;
    }
    showTimeOptions();
  });

  popupClose.addEventListener('click', hideDateTimePopup);

  // Close popup when clicking outside
  dateTimePopup.addEventListener('click', (e) => {
    if(e.target === dateTimePopup){
      hideDateTimePopup();
    }
  });

  // Prevent date/time native pickers from showing
  dateInput.addEventListener('focus', (e) => {
    e.target.blur();
    showDateOptions();
  });

  timeInput.addEventListener('focus', (e) => {
    e.target.blur();
    if(!dateInput.value){
      alert('Please select a date first.');
      return;
    }
    showTimeOptions();
  });

  // Smooth scrolling for in-page nav links (with fallback for `#appointment`)
  document.querySelectorAll('a[href^="#"]').forEach(a=>{
    a.addEventListener('click', function(e){
      const href = this.getAttribute('href');
      if(!href || href === '#') return;
      const id = href.slice(1);
      let el = document.getElementById(id) || document.getElementById(id + '-form');
      if(!el && id === 'appointment') el = document.querySelector('.hero-card');
      if(el){
        e.preventDefault();
        const y = el.getBoundingClientRect().top + window.pageYOffset - 18;
        window.scrollTo({top: y, behavior: 'smooth'});
        history.replaceState(null, '', href);
      }
    });
  });

  // Live moving sparkles in the background
  (function(){
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(prefersReduced) return;
    const container = document.querySelector('.sparkles');
    if(!container) return;

    let running = true;
    const max = 36;

    function rand(min, max){ return Math.random() * (max - min) + min; }

    function spawn(){
      if(!running) return;
      const count = Math.random() > 0.7 ? 2 : 1;
      for(let i=0;i<count;i++){
        if(container.children.length >= max) break;
        const el = document.createElement('span');
        el.className = 'sparkle';
        const size = Math.round(rand(4,14));
        el.style.width = size + 'px';
        el.style.height = size + 'px';
        const left = rand(2,98);
        const top = rand(2,88);
        el.style.left = left + '%';
        el.style.top = top + '%';
        const dx = Math.round(rand(-120,120));
        const dy = Math.round(rand(-160,160));
        el.style.setProperty('--dx', dx + 'px');
        el.style.setProperty('--dy', dy + 'px');
        const durVal = rand(3.2,7.2);
        const dur = durVal.toFixed(2) + 's';
        el.style.setProperty('--dur', dur);
        // stagger twinkle by applying a delay to the second animation
        const twinkleDelay = (Math.random() * Math.min(2.0, durVal)).toFixed(2) + 's';
        el.style.animationDelay = `0s, ${twinkleDelay}`;
        container.appendChild(el);
        el.addEventListener('animationend', ()=>{ if(el.parentNode) el.parentNode.removeChild(el); });
      }
    }

    // spawn steady stream
    const interval = setInterval(spawn, 550);

    // stop when page is hidden
    document.addEventListener('visibilitychange', ()=>{
      if(document.hidden){ running = false; clearInterval(interval); }
      else { running = true; setInterval(spawn, 550); }
    });
  })();
});