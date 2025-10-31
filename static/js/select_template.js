// ✅ Define template fields first
const templateFields = {
  1: ["Contact", "Profile", "Technical Skills", "Certificates", "Language", "Education"],
  2: ["Contact", "Education", "Expertise", "Language", "About me", "Work Experience", "Internships"],
  3: ["Profile", "Contact", "Education", "Skills", "Professional Experience"],
  4: ["Contact", "Hard Skills", "Soft Skills", "Education", "About Me", "Professional Experience", "Achievements"],
  5: ["Contact", "Profile", "Education", "Skills", "Languages", "Certificates"],
  6: ["Contact", "About Me", "Skills", "Certificates", "Education", "Experience"] // wide template
};

// Track selected template
let selectedTemplateId = null;

// popup elements
const popup = document.getElementById('template-popup');
const popupImage = document.getElementById('popup-image');
const popupTitle = document.getElementById('popup-title');
const popupFieldsList = document.getElementById('popup-fields');
const popupSelectBtn = document.querySelector('.final-select-btn');

// defensive check
if (!popup || !popupImage || !popupTitle || !popupFieldsList || !popupSelectBtn) {
  console.error('Popup elements missing. Ensure IDs: template-popup, popup-image, popup-title, popup-fields and class final-select-btn exist in HTML.');
}

// Open popup when clicking on any template Select
document.querySelectorAll('.template-box .select-btn').forEach(button => {
  button.addEventListener('click', (e) => {
    const templateId = button.getAttribute('data-template-id');
    if (!templateId) return;

    selectedTemplateId = String(templateId);
    const fields = templateFields[selectedTemplateId] || [];

    const templateBox = e.target.closest('.template-box');
    const img = templateBox ? templateBox.querySelector('img') : null;
    const imgSrc = img ? img.getAttribute('src') : '';

    // populate popup image & fields
    popupImage.src = imgSrc;
    popupTitle.textContent = 'Resume Fields'; // fixed title
    popupFieldsList.innerHTML = '';
    fields.forEach(f => {
      const li = document.createElement('li');
      li.textContent = f;
      popupFieldsList.appendChild(li);
    });

    // show popup via class
    popup.classList.add('open');

    // accessibility: focus on final button
    popupSelectBtn.focus();
  });
});

// Close when clicking outside content
popup.addEventListener('click', (e) => {
  if (e.target === popup) popup.classList.remove('open');
});

// Close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && popup.classList.contains('open')) {
    popup.classList.remove('open');
  }
});

// Final select redirect mapping (as requested)
popupSelectBtn.addEventListener('click', () => {
  if (!selectedTemplateId) {
    alert('Please select a template first!');
    return;
  }

  // Mapping you requested:
  // upper-part: 1 -> template5, 2->2, 3->3, 4->4
  // wide template (id 6) -> template1
  const redirectMap = {
    "1": '/form/template5',
    "2": '/form/template2',
    "3": '/form/template3',
    "4": '/form/template4',
    "5": '/form/template5',
    "6": '/form/template1'
  };

  const target = redirectMap[String(selectedTemplateId)];
  if (target) {
    // close popup for a nicer UX then redirect
    popup.classList.remove('open');
    // redirect
    window.location.href = target;
  } else {
    alert('This template is not linked yet!');
  }
});
