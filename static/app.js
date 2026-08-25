const thread   = document.getElementById('thread');
const hero     = document.getElementById('hero');
const imgSlot  = document.getElementById('imgSlot');
const imgInput = document.getElementById('imgInput');
const imgEmpty = document.getElementById('imgEmpty');
const imgPrev  = document.getElementById('imgPreview');
const textIn   = document.getElementById('textInput');
const sendBtn  = document.getElementById('sendBtn');
const status   = document.getElementById('status');
const pdfInput = document.getElementById('pdfInput');

let currentFile = null;

function refreshSend(){
  sendBtn.disabled = !(currentFile && textIn.value.trim().length);
}
textIn.addEventListener('input', () => {
  textIn.style.height = 'auto';
  textIn.style.height = Math.min(textIn.scrollHeight, 160) + 'px';
  refreshSend();
});
imgSlot.addEventListener('click', () => imgInput.click());
imgInput.addEventListener('change', () => {
  const f = imgInput.files[0];
  if(!f) return;
  currentFile = f;
  const reader = new FileReader();
  reader.onload = e => {
    imgPrev.src = e.target.result;
    imgPrev.hidden = false;
    imgEmpty.hidden = true;
  };
  reader.readAsDataURL(f);
  refreshSend();
});

function hideHero(){ if(hero) hero.style.display = 'none'; }
function scrollDown(){ thread.scrollTop = thread.scrollHeight; }

function addUser(text, imgUrl){
  hideHero();
  const el = document.createElement('div');
  el.className = 'msg user';
  el.innerHTML =
    '<div class="who">You</div>' +
    '<div class="body">' +
      (imgUrl ? '<img class="thumb" src="' + imgUrl + '">' : '') +
      '<div class="bubble"></div>' +
    '</div>';
  el.querySelector('.bubble').textContent = text;
  thread.appendChild(el);
  scrollDown();
}

function addTyping(){
  const el = document.createElement('div');
  el.className = 'msg bot';
  el.innerHTML =
    '<div class="who">V</div>' +
    '<div class="body"><div class="typing"><span></span><span></span><span></span></div></div>';
  thread.appendChild(el);
  scrollDown();
  return el;
}

function fillBot(el, data, isError){
  const body = el.querySelector('.body');
  body.innerHTML = '';

  const bubble = document.createElement('div');
  bubble.className = 'bubble' + (isError ? ' err' : '');
  bubble.textContent = isError ? data : data.answer;
  body.appendChild(bubble);

  if(isError){ scrollDown(); return; }

  const chips = document.createElement('div');
  chips.className = 'chips';
  const c1 = document.createElement('span');
  c1.className = 'chip';
  c1.textContent = data.label;
  chips.appendChild(c1);
  if(data.caption){
    const c2 = document.createElement('span');
    c2.className = 'chip muted';
    c2.textContent = 'caption: ' + data.caption;
    chips.appendChild(c2);
  }
  body.appendChild(chips);

  if(data.sources && data.sources.length){
    const det = document.createElement('details');
    det.className = 'sources';
    const sum = document.createElement('summary');
    sum.textContent = 'Retrieved context (' + data.sources.length + ')';
    det.appendChild(sum);
    data.sources.forEach(s => {
      const d = document.createElement('div');
      d.className = 'source';
      const via = document.createElement('div');
      via.className = 'via';
      via.textContent = 'matched via ' + s.via;
      const txt = document.createElement('div');
      txt.className = 'txt';
      txt.textContent = s.content;
      d.appendChild(via); d.appendChild(txt);
      det.appendChild(d);
    });
    body.appendChild(det);
  }
  scrollDown();
}

async function send(){
  const text = textIn.value.trim();
  if(!currentFile || !text) return;

  const imgUrl = imgPrev.src;
  addUser(text, imgUrl);

  textIn.value = ''; textIn.style.height = 'auto';
  sendBtn.disabled = true;
  status.classList.add('busy');
  status.querySelector('.dot').nextSibling.textContent = ' Thinking';
  const typing = addTyping();

  const fd = new FormData();
  fd.append('text', text);
  fd.append('image', currentFile);

  try{
    const res = await fetch('/chat', { method:'POST', body: fd });
    const data = await res.json();
    if(!res.ok) throw new Error(data.error || ('Server error ' + res.status));
    fillBot(typing, data, false);
  }catch(err){
    fillBot(typing, err.message || 'Something went wrong.', true);
  }finally{
    status.classList.remove('busy');
    status.querySelector('.dot').nextSibling.textContent = ' Ready';
    refreshSend();
  }
}
sendBtn.addEventListener('click', send);
textIn.addEventListener('keydown', e => {
  if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); send(); }
});

document.getElementById('navNew').addEventListener('click', () => {
  thread.querySelectorAll('.msg').forEach(m => m.remove());
  if(hero) hero.style.display = '';
  currentFile = null;
  imgInput.value = '';
  imgPrev.hidden = true; imgEmpty.hidden = false;
  textIn.value = ''; refreshSend();
});

document.getElementById('navPdf').addEventListener('click', () => pdfInput.click());
pdfInput.addEventListener('change', async () => {
  const f = pdfInput.files[0];
  if(!f) return;
  status.classList.add('busy');
  status.querySelector('.dot').nextSibling.textContent = ' Rebuilding KB';
  const fd = new FormData();
  fd.append('pdf', f);
  try{
    const res = await fetch('/upload-pdf', { method:'POST', body: fd });
    const data = await res.json();
    hideHero();
    const el = addTyping();
    fillBot(el, res.ok ? { answer: data.status || 'Knowledge base updated.', label: 'PDF ingested', caption:'', sources: [] }
                       : (data.error || 'Upload failed.'), !res.ok);
  }catch(err){
    const el = addTyping(); fillBot(el, err.message, true);
  }finally{
    status.classList.remove('busy');
    status.querySelector('.dot').nextSibling.textContent = ' Ready';
    pdfInput.value = '';
  }
});

const aboutModal = document.getElementById('aboutModal');
document.getElementById('navAbout').addEventListener('click', () => aboutModal.hidden = false);
document.getElementById('aboutClose').addEventListener('click', () => aboutModal.hidden = true);
aboutModal.addEventListener('click', e => { if(e.target === aboutModal) aboutModal.hidden = true; });

textIn.focus();
