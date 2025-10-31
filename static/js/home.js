const track = document.querySelector('.slideshow-track');
const templates = document.querySelectorAll('.template');

let scrollX = 0;
let speed = 1.75; // faster scroll
let isPaused = false;
let lastZoomed = null;
let zoomCooldown = false;

function animate() {
  if (!isPaused) {
    scrollX += speed;
    track.style.transform = `translateX(-${scrollX}px)`;
  }

  // Only reset after zoom cooldown is over and not paused
  const totalWidth = track.scrollWidth / 2;
  if (scrollX >= totalWidth && !isPaused && !zoomCooldown) {
    scrollX = 0;
  }

  checkCenterTemplate();
  requestAnimationFrame(animate);
}

function checkCenterTemplate() {
  const container = document.querySelector('.slideshow-container');
  const containerRect = container.getBoundingClientRect();
const containerCenter = window.innerWidth / 2;


  templates.forEach(template => {
    const rect = template.getBoundingClientRect();
    const templateCenter = rect.left + rect.width / 2;
    const distance = Math.abs(templateCenter - containerCenter);

    if (distance < 20 && !zoomCooldown) {
      if (lastZoomed !== template) {
        zoomCooldown = true;
        isPaused = true;
        lastZoomed = template;

        template.classList.add('zoomed');
template.style.transform = 'scale(1.2)';

        setTimeout(() => {
          template.style.transform = 'scale(1)';
          template.classList.remove('zoomed');

          setTimeout(() => {
            isPaused = false;
            zoomCooldown = false;
          }, 400); // allow smooth shrink before resuming
        }, 2000); // hold zoom for 2 sec
      }
    } else if (template !== lastZoomed) {
      template.style.transform = 'scale(1)';
    }
  });
}
// Get the button wrapper
const buttonWrapper = document.querySelector('.button-wrapper');

function revealButtonOnScroll() {
  const rect = buttonWrapper.getBoundingClientRect();
  const isVisible = rect.top < window.innerHeight;

  if (isVisible) {
    // Wait 0.1s before showing
    setTimeout(() => {
      buttonWrapper.classList.add('visible');
    }, 100);
    // Remove scroll listener after showing once
    window.removeEventListener('scroll', revealButtonOnScroll);
  }
}

window.addEventListener('scroll', revealButtonOnScroll);

animate();
