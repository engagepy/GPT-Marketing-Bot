const loadingElement = document.getElementById('loading');
const rocketsElement = document.querySelector('.rockets');
let rocketCount = 1;

function increaseRockets() {
  rocketCount += 1;
  rocketsElement.textContent = '🚀'.repeat(rocketCount);
}

setTimeout(increaseRockets, 2000);