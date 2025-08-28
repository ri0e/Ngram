window.onload = function () {
  const themeToggle = document.getElementById("theme-toggle");
  const body = document.body;

  let theme = localStorage.getItem("theme");
  if (theme) {
    body.classList.add(theme);
  } else if (
    !(
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    )
  ) {
    body.classList.add("light-mode");
    theme = "light-mode";
  }

  themeToggle.addEventListener("click", () => {
    body.classList.toggle("light-mode");
    theme = body.classList.contains("light-mode") ? "light-mode" : "dark-mode";
    localStorage.setItem("theme", theme);
    c.fillStyle = theme === "light-mode" ? "black" : "white";
  });

  var lyric =
    "i couldn't take it couldn't stand another minute couldn't bear another day without you in it all of the joy that I had known for my life was stripped away from me the minute that you died to have you in my life was all i ever wanted but now without you I'm a soul forever haunted can't help but feel that i had taken you for granted no way in hell that i can ever comprehend this i wasn't dreaming when they told me you were gone i was wide awake and feeling that they had to be wrong how could you leave me when you swore that you would stay now i'm trapped inside a nightmare every single fucking day it's like a movie but there's not a happy ending every scene fades black and there's no pretending this little fairy tale doesn't seem to end well theres no knight in shining armor who will wake me from the spell i know you didn't plan this you tried to do what's right but in the middle of this madness i'm the one you left to win this fight red like roses fills my head with dreams and finds me always closer to the emptiness and sadness that has come to take the place of you i know you're broken down by anger and by sadness you feel I left you in a world that's full of madness wish i could talk to you if only for a minute make you understand the reasons why i did it i wanna tell you that you're all that ever mattered want you to know that for eternity i'm shattered i tried so hard just to protect you but i failed to and in a prison of abandonment i've jailed you i never planned that i would leave you there alone i was sure that i would see you when i made it back home and all the times I swore that it would be okay now i'm nothing but a liar and you're thrown into the fray this bedtime story ends with misery ever after the pages are torn and there's no final chapter i didn't have a choice I did what I had to do i made a sacrifice but forced a bigger sacrifice on you i know you've lived a nightmare i caused you so much pain but baby please don't do what i did i don't want you to waste your life in vain red like roses fills my head with dreams and finds me always closer to the emptiness and sadness that has come to take the place of you you're not the only one who needed me i thought you understood you were the one i needed and you left me as I always feared you would would I change it if i could? it doesn't matter how the petals scatter now every nightmare just discloses it's your blood that's red like roses and no matter what I do nothing ever takes the place of you red like roses fills my head with dreams and finds me always closer to the emptiness and sadness that has come to take the place of you";
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
    c.fillStyle = theme === "light-mode" ? "black" : "white";
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

function output(text) {
  const messageArea = document.getElementById("output");
  messageArea.textContent = text;
}

function displayMessage(status, message) {
  const messageArea = document.getElementsByClassName("message-area")[0];
  const errorIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" viewBox="0 0 24 24" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zm-1.5-5.009c0-.867.659-1.491 1.491-1.491.85 0 1.509.624 1.509 1.491 0 .867-.659 1.509-1.509 1.509-.832 0-1.491-.642-1.491-1.509zM11.172 6a.5.5 0 0 0-.499.522l.306 7a.5.5 0 0 0 .5.478h1.043a.5.5 0 0 0 .5-.478l.305-7a.5.5 0 0 0-.5-.522h-1.655z" fill="#d6d6d6"/></svg>`;

  const successIcon = `<svg xmlns="http://www.w3.org/2000/svg" fill="#d6d6d6" width="30px" height="30px" viewBox="0 0 52 52" enable-background="new 0 0 52 52" xml:space="preserve"><path d="M26,2C12.7,2,2,12.7,2,26s10.7,24,24,24s24-10.7,24-24S39.3,2,26,2z M39.4,20L24.1,35.5  c-0.6,0.6-1.6,0.6-2.2,0L13.5,27c-0.6-0.6-0.6-1.6,0-2.2l2.2-2.2c0.6-0.6,1.6-0.6,2.2,0l4.4,4.5c0.4,0.4,1.1,0.4,1.5,0L35,15.5  c0.6-0.6,1.6-0.6,2.2,0l2.2,2.2C40.1,18.3,40.1,19.3,39.4,20z"/>
  </svg>`;
  messageArea.className = "message-area";
  messageArea.textContent = "";
  messageArea.style.display = "none";

  messageArea.classList.add(status);
  const symbol =
    status === "success" ? successIcon : status === "error" ? errorIcon : "";

  const span = document.createElement("span");
  span.className = "span-text";
  span.textContent = message;

  const p = document.createElement("p");
  p.className = "message-text";
  p.innerHTML = symbol;
  p.appendChild(span);

  messageArea.appendChild(p);

  messageArea.style.display = "block";
  messageArea.style.opacity = "1";

  messageArea.onclick = function () {
    messageArea.style.opacity = "0";
    setTimeout(() => {
      messageArea.style.display = "none";
    }, 300);
  };

  setTimeout(() => {
    if (messageArea.style.display === "block") {
      messageArea.style.opacity = "0";
      setTimeout(() => {
        messageArea.style.display = "none";
      }, 3000);
    }
  }, 7000);
}

document.addEventListener("DOMContentLoaded", function () {
  const generation = document.getElementById("generation");
  const choose = document.getElementById("check_choose");
  const predict_many = document.getElementById("predict_many");
  const word_count = document.getElementById("word_count_label");

  predict_many.addEventListener("click", function () {
    if (predict_many.checked) {
      choose.disabled = true;
      word_count.hidden = false;
    } else {
      choose.disabled = false;
      word_count.hidden = true;
    }
  });

  generation.addEventListener("submit", async function (event) {
    console.log("DEBUG: Submit event caught by formsContainer!");
    const form = event.target.closest(".intercept");

    if (!form) {
      return;
    }

    event.preventDefault();

    const formAction = form.action;
    const formData = new FormData(form);

    try {
      const response = await fetch(formAction, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        displayMessage("error", errorText);
      }

      const data = await response.json();

      if (!data.next_word) {
        displayMessage(data.status, data.message);
        return;
      }

      output(data.next_word);
      displayMessage("success", "Text generated successfully.");
    } catch (error) {
      console.error("Fetch error:", error);
      displayMessage("error", error);
    }
  });
});
