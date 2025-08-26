window.onload = function () {
  const themeToggle = document.getElementById("theme-toggle");
  const theme = localStorage.getItem("theme");
  const body = document.body;
  if (theme) {
    body.classList.add(theme);
  } else if (
    !(
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    )
  ) {
    body.classList.add("light-mode");
  }
  themeToggle.addEventListener("click", () => {
    body.classList.toggle("light-mode");
    if (body.classList.contains("light-mode")) {
      localStorage.setItem("theme", "light-mode");
    } else {
      localStorage.setItem("theme", "dark-mode");
    }
  });

  var lyric =
    "Bright morning sunlight painted rooftops golden while distant traffic echoed across empty streets. Curious birds circled above gardens searching hidden seeds. Young children chased colorful kites drifting higher through gentle breezes. Strong determination pushed athletes beyond limits during long practice sessions. Quiet libraries preserved knowledge, inspiring thoughtful minds exploring infinite possibilities. Evening shadows stretched slowly across silent courtyards while lanterns flickered gently, revealing hidden corners filled with whispers. Rustling leaves carried memories from forgotten journeys, stirring emotions buried within restless hearts. Towering structures reflected glowing skies, reminding wanderers about endless horizons waiting beyond crowded avenues. Distant mountains stood proudly, crowned with snow, guarding valleys nourished by rushing rivers. Farmers guided animals through fertile fields, preparing soil for harvest seasons. Travelers followed winding trails, discovering villages where traditions survived centuries despite storms, droughts, struggles. Voices from marketplaces rose above drumbeats, creating rhythms uniting strangers through celebration. Creative minds filled notebooks with sketches, melodies, formulas, shaping visions destined to influence generations. Silent determination fueled progress, while curiosity sparked discoveries across laboratories, libraries, workshops. Dreams collided with obstacles, yet resilience lifted spirits, proving strength emerges whenever hope remains steady.";
  var words = {};
  var words_attr = [];
  string_handle(lyric);

  var canvas = document.getElementById("c");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  if (canvas.getContext) {
    var c = canvas.getContext("2d"),
      w = canvas.width,
      h = canvas.height;

    c.strokeStyle = "blue";
    c.fillStyle = "white";
    c.lineWidth = 5;

    // constructor
    Word = function (key) {
      this.text = key;
      this.x = Math.random() * w;
      this.y = Math.random() * h;
      this.font = words[key] * 10 + "px arial";
      this.speed = words[key];
    };
    for (key in words) {
      words_attr.push(new Word(key));
    }
    console.log(words_attr.length);

    function animation() {
      for (var i = 0; i < words_attr.length; i++) {
        c.font = words_attr[i].font;
        c.fillText(words_attr[i].text, words_attr[i].x, words_attr[i].y);
        words_attr[i].width = c.measureText(words_attr[i].text).width;
        c.stroke();
      }
      move();
    }

    function move() {
      for (var i = 0; i < words_attr.length; i++) {
        if (words_attr[i].x > w) {
          words_attr[i].x = -words_attr[i].width;
          words_attr[i].y = Math.random() * h;
        } else {
          words_attr[i].x += words_attr[i].speed;
        }
      }
    }

    setInterval(function () {
      c.clearRect(0, 0, w, h);
      animation();
    }, 24);
  }

  function string_handle(str) {
    var split_str = str.split(" ");
    var word_array = [];
    var word_count = [];
    for (var i = 0; i < split_str.length; i++) {
      check = true;
      for (var j = 0; j <= word_array.length; j++) {
        if (split_str[i] == word_array[j]) {
          word_count[j]++;
          check = false;
          break;
        }
      }
      if (check) {
        word_array.push(split_str[i]);
        word_count.push(1);
      }
    }
    for (var i = 0; i < word_array.length; i++) {
      words[word_array[i]] = word_count[i];
    }
    return words;
  }
};

function output(text){
    const messageArea = document.getElementById('output');
    messageArea.textContent = text;
}

function displayMessage(status, message){
    const messageArea = document.getElementsByClassName('message-area')[0];

    messageArea.className = 'message-area';
    messageArea.textContent = '';
    messageArea.style.display = 'none';

    messageArea.classList.add(status);
    const symbol = status === 'success' ? '✔' : (status === 'error' ? 'X' : '');
    messageArea.innerHTML = `<p style = "font-size: 1em">${symbol} <span style = "font-size: 0.5em">${message}</span></p>`;

    messageArea.style.display = 'block';
    messageArea.style.opacity = '1';

    messageArea.addEventListener('click', function(){
        messageArea.style.opacity = '0';
        messageArea.style.display = 'none';
        return;
    });

    setTimeout(() => {
        messageArea.style.opacity = '0';
        messageArea.style.display = 'none';
    }, 7000);
}

document.addEventListener('DOMContentLoaded', function() {
    const generation = document.getElementById('generation');
    const choose = document.getElementById('check_choose');
    const predict_many = document.getElementById('predict_many');
    const word_count = document.getElementById('word_count_label');

    predict_many.addEventListener('click', function(){
        if (predict_many.checked){
            choose.disabled = true;
            word_count.hidden = false;
        } else {
            choose.disabled = false;
            word_count.hidden = true;
        }
    });

    generation.addEventListener('submit', async function(event){
        console.log('DEBUG: Submit event caught by formsContainer!');
        const form = event.target.closest('.intercept');

        if (!form) {
            return;
        }

        event.preventDefault();
        
        const formAction = form.action;
        const formData = new FormData(form);

        try{
            const response = await fetch(formAction, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                displayMessage('error', errorText);
            }

            const data = await response.json();

            if(!data.next_word){
                 displayMessage(data.status, data.message);
                 return;
            }

            output(data.next_word);
            displayMessage('success', 'Text generated successfully.');
        }

        catch(error){
            console.error('Fetch error:', error);
            displayMessage('error', error);
        }
    });
});
