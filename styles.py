card1_front_template_one_side = """
{{#Choices}}
<div class="info">Multiple Choices Card</div>
<div class="info">{{Id}}</div>

<script>
    pycmd("ans");
</script>
{{/Choices}}
"""

card1_back_template_one_side = """
<div id="Container">
    <div id="card">
        <div id="Q-E">
            <div id="Q">{{Question}}</div>
            <div id="E">
                {{#Explanation}}
                <hr>{{Explanation}}{{/Explanation}}
                {{#Extra}}
                <hr>{{Extra}}{{/Extra}}
            </div>
        </div>
        <div id="A">
            <!-- Answer below -->
            {{Answer}}
            <!-- Answer above -->
        </div>
        <div id="C">
            <!-- Other choice below -->
            {{Choices}}
            <!-- Other choice above -->
        </div>
    </div>
    <a id="showHideAnswer" onClick="showHide(this)">Show Answer</a>
</div>

<script>
    // split questions
    var questions = document
        .getElementById("Q")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var q = document.getElementById("Q");
    q.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let x = document.createElement("div");
        x.innerHTML = questions[i];
        q.appendChild(x);
    }

    // split answers and choices
    var answers = document
        .getElementById("A")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var opts = document.getElementById("C").innerHTML;
    document.getElementById("C").remove();
    var nchoices = 0;
    hide();
    document.addEventListener("keydown", (e) => {
        parsed = parseInt(e.key, 10);
        if(!isNaN(parsed) && parsed > 0  && parsed <= nchoices && e.altKey) {
            document.getElementById(parsed.toString()).click();
        }
        if(e.key.toLowerCase() == "q") {
            document.getElementById("showHideAnswer").click();
        } 
    });
    function hide() {
        let options = shuffle([
            ...answers,
            ...opts.split("|").map((i) => i.trim()),
        ]);
        nchoices = options.length;
        var c = document.getElementById("A");
        c.innerHTML = "";
        var e = document.getElementById("E");
        e.style.display = "none";
        for (let i = 0; i < options.length; i++) {
            let x = document.createElement("a");
            x.innerHTML = options[i];
            x.setAttribute("class", "options");
            x.setAttribute("id", (i+1).toString());
            x.onclick = (e) => check(e.target);
            c.appendChild(x);
        }
        document.getElementById("showHideAnswer").innerHTML = "Show Answer";
    }
    function check(e) {
        let tg = e;
        if (!e.classList.contains("options")) {
            tg = e.closest(".options");
        }

        let option = tg.innerHTML;
        if (answers.find((i) => i == option)) {
            tg.classList.add("right");
        } else {
            tg.classList.add("wrong");
        }
        if (document.getElementsByClassName("right").length == answers.length) {
            show();
        }
    }
    function show() {
        let opts = document.getElementsByClassName("options");
        let wrongs = document.getElementsByClassName("wrong");
        for (let opt of opts) {
            let option = opt.innerHTML;
            if (answers.find((i) => i == option)) {
                opt.classList.add("right");
            } else {
                opt.classList.add("wrong");
            }
        }
        for (let wrong of wrongs) {
            wrong.style.display = "none";
        }
        document.getElementById("E").style.display = "block";
        document.getElementById("showHideAnswer").innerHTML = "Shuffle Choices";
    }
    function shuffle(array) {
        let currentIndex = array.length,
            randomIndex;
        while (currentIndex != 0) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;
            [array[currentIndex], array[randomIndex]] = [
                array[randomIndex],
                array[currentIndex],
            ];
        }
        return array;
    }
    function showHide(e) {
        if (e.innerHTML === "Show Answer") {
            show();
        } else {
            let opts = document.getElementsByClassName("options");
            for (let opt of opts) {
                opt.classList.remove("wrong");
                opt.classList.remove("right");
                opt.style.display = "block";
            }
            hide();
        }
    }
</script>
"""

card2_front_template_one_side = """
{{#Reversed Choices}}
<div class="info">Multiple Choices Card</div>
<div class="info">{{Id}}</div>

<script>
    pycmd("ans");
</script>
{{/Reversed Choices}}
"""

card2_back_template_one_side = """
<div id="Container">
    <div id="card">
        <div id="Q-E">
            <div id="Q">{{Answer}}</div>
            <div id="E">
                {{#Explanation}}
                <hr>{{Explanation}}{{/Explanation}}
                {{#Extra}}
                <hr>{{Extra}}{{/Extra}}
            </div>
        </div>
        <div id="A">
            <!-- Answer below -->
            {{Question}}
            <!-- Answer above -->
        </div>
        <div id="C">
            <!-- Other choice below -->
            {{Reversed Choices}}
            <!-- Other choice above -->
        </div>
    </div>
    <a id="showHideAnswer" onClick="showHide(this)">Show Answer</a>
</div>

<script>
    // split questions
    var questions = document
        .getElementById("Q")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var q = document.getElementById("Q");
    q.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let x = document.createElement("div");
        x.innerHTML = questions[i];
        q.appendChild(x);
    }

    // split answers and choices
    var answers = document
        .getElementById("A")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var opts = document.getElementById("C").innerHTML;
    document.getElementById("C").remove();
    var nchoices = 0;
    hide();
    document.addEventListener("keydown", (e) => {
        parsed = parseInt(e.key, 10);
        if(!isNaN(parsed) && parsed > 0  && parsed <= nchoices && e.altKey) {
            document.getElementById(parsed.toString()).click();
        }
        if(e.key.toLowerCase() == "q") {
            document.getElementById("showHideAnswer").click();
        } 
    });
    function hide() {
        let options = shuffle([
            ...answers,
            ...opts.split("|").map((i) => i.trim()),
        ]);
        nchoices = options.length;
        var c = document.getElementById("A");
        c.innerHTML = "";
        var e = document.getElementById("E");
        e.style.display = "none";
        for (let i = 0; i < options.length; i++) {
            let x = document.createElement("a");
            x.innerHTML = options[i];
            x.setAttribute("class", "options");
            x.setAttribute("id", (i+1).toString());
            x.onclick = (e) => check(e.target);
            c.appendChild(x);
        }
		document.getElementById("showHideAnswer").innerHTML = "Show Answer";
    }
    function check(e) {
        let tg = e;
        if (!e.classList.contains("options")) {
            tg = e.closest(".options");
        }

        let option = tg.innerHTML;
        if (answers.find((i) => i == option)) {
            tg.classList.add("right");
        } else {
            tg.classList.add("wrong");
        }
        if (document.getElementsByClassName("right").length == answers.length) {
            show();
        }
    }
    function show() {
        let opts = document.getElementsByClassName("options");
        let wrongs = document.getElementsByClassName("wrong");
        for (let opt of opts) {
            let option = opt.innerHTML;
            if (answers.find((i) => i == option)) {
                opt.classList.add("right");
            } else {
                opt.classList.add("wrong");
            }
        }
        for (let wrong of wrongs) {
            wrong.style.display = "none";
        }
        document.getElementById("E").style.display = "block";
        document.getElementById("showHideAnswer").innerHTML = "Shuffle Choices";
    }
    function shuffle(array) {
        let currentIndex = array.length,
            randomIndex;
        while (currentIndex != 0) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;
            [array[currentIndex], array[randomIndex]] = [
                array[randomIndex],
                array[currentIndex],
            ];
        }
        return array;
    }
    function showHide(e) {
        if (e.innerHTML === "Show Answer") {
            show();
        } else {
            let opts = document.getElementsByClassName("options");
            for (let opt of opts) {
                opt.classList.remove("wrong");
                opt.classList.remove("right");
                opt.style.display = "block";
            }
            hide();
        }
    }
</script>
"""

card1_front_template_two_sides = """
{{#Choices}}
<div id="Container">
    <div id="card">
        <div id="Q-E">
            <div id="Q">{{Question}}</div>
            <div id="E">
                {{#Explanation}}
                <hr>{{Explanation}}{{/Explanation}}
                {{#Extra}}
                <hr>{{Extra}}{{/Extra}}
            </div>
        </div>
        <div id="A">
            <!-- Answer below -->
            {{Answer}}
            <!-- Answer above -->
        </div>
        <div id="C">
            <!-- Other choices below -->
            {{Choices}}
            <!-- Other choices above -->
        </div>
    </div>
    <a id="showHideAnswer" onClick="showAns(this)">Show Answer</a>
</div>

<script>
    // split questions
    var questions = document
        .getElementById("Q")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var q = document.getElementById("Q");
    q.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let x = document.createElement("div");
        x.innerHTML = questions[i];
        q.appendChild(x);
    }

    // split answers and choices
    var answers = document
        .getElementById("A")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var opts = document.getElementById("C").innerHTML;
    document.getElementById("C").remove();
    var nchoices = 0;
    hide();
    document.addEventListener("keydown", (e) => {
        parsed = parseInt(e.key, 10);
        if(!isNaN(parsed) && parsed > 0  && parsed <= nchoices && e.altKey) {
            document.getElementById(parsed.toString()).click();
        }
    });
    function hide() {
        let options = shuffle([
            ...answers,
            ...opts.split("|").map((i) => i.trim()),
        ]);
        nchoices = options.length;
        var c = document.getElementById("A");
        c.innerHTML = "";
        var e = document.getElementById("E");
        e.style.display = "none";
        for (let i = 0; i < options.length; i++) {
            let x = document.createElement("a");
            x.innerHTML = options[i];
            x.setAttribute("class", "options");
            x.setAttribute("id", (i+1).toString());
            x.onclick = (e) => check(e.target);
            c.appendChild(x);
        }
    }
    function check(e) {
        let tg = e;
        if (!e.classList.contains("options")) {
            tg = e.closest(".options");
        }

        let option = tg.innerHTML;
        if (answers.find((i) => i == option)) {
            tg.classList.add("right");
        } else {
            tg.classList.add("wrong");
        }
        if (document.getElementsByClassName("right").length == answers.length) {
            document.getElementById("showHideAnswer").click();;
        }
    }
    function shuffle(array) {
        let currentIndex = array.length,
            randomIndex;
        while (currentIndex != 0) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;
            [array[currentIndex], array[randomIndex]] = [
                array[randomIndex],
                array[currentIndex],
            ];
        }
        return array;
    }
    function showAns(e) {
        pycmd("ans");
    }
</script>

{{/Choices}}
"""

card1_back_template_two_sides = """
<div id="Container">
    <div id="card">
        <div id="Q-E">
            <div id="Q">{{Question}}</div>
            <div id="E">
                {{#Explanation}}
                <hr>{{Explanation}}{{/Explanation}}
                {{#Extra}}
                <hr>{{Extra}}{{/Extra}}
            </div>
        </div>
        <div id="A">
            <!-- Answer below -->
            {{Answer}}
            <!-- Answer above -->
        </div>
    </div>
</div>

<script>
    // split questions
    var questions = document
        .getElementById("Q")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var q = document.getElementById("Q");
    q.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let x = document.createElement("div");
        x.innerHTML = questions[i];
        q.appendChild(x);
    }

    // split answers and choices
    var answers = document
        .getElementById("A")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var c = document.getElementById("A");
    c.innerHTML = "";
    for (let i = 0; i < answers.length; i++) {
        let x = document.createElement("a");
        x.innerHTML = answers[i];
        x.setAttribute("class", "options");
        x.classList.add("right")
        c.appendChild(x);
    }
</script>
"""

card2_front_template_two_sides = """
{{#Reversed Choices}}
<div id="Container">
    <div id="card">
        <div id="Q-E">
            <div id="Q">{{Answer}}</div>
            <div id="E">
                {{#Explanation}}
                <hr>{{Explanation}}{{/Explanation}}
                {{#Extra}}
                <hr>{{Extra}}{{/Extra}}
            </div>
        </div>
        <div id="A">
            <!-- Answer below -->
            {{Question}}
            <!-- Answer above -->
        </div>
        <div id="C">
            <!-- Other choices below -->
            {{Reversed Choices}}
            <!-- Other choices above -->
        </div>
    </div>
    <a id="showHideAnswer" onClick="showAns(this)">Show Answer</a>
</div>

<script>
    // split questions
    var questions = document
        .getElementById("Q")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var q = document.getElementById("Q");
    q.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let x = document.createElement("div");
        x.innerHTML = questions[i];
        q.appendChild(x);
    }

    // split answers and choices
    var answers = document
        .getElementById("A")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var opts = document.getElementById("C").innerHTML;
    document.getElementById("C").remove();
    var nchoices = 0;
    hide();
    document.addEventListener("keydown", (e) => {
        parsed = parseInt(e.key, 10);
        if(!isNaN(parsed) && parsed > 0  && parsed <= nchoices && e.altKey) {
            document.getElementById(parsed.toString()).click();
        }
    });
    function hide() {
        let options = shuffle([
            ...answers,
            ...opts.split("|").map((i) => i.trim()),
        ]);
        nchoices = options.length;
        var c = document.getElementById("A");
        c.innerHTML = "";
        var e = document.getElementById("E");
        e.style.display = "none";
        for (let i = 0; i < options.length; i++) {
            let x = document.createElement("a");
            x.innerHTML = options[i];
            x.setAttribute("class", "options");
            x.setAttribute("id", (i+1).toString());
            x.onclick = (e) => check(e.target);
            c.appendChild(x);
        }
    }
    function check(e) {
        let tg = e;
        if (!e.classList.contains("options")) {
            tg = e.closest(".options");
        }

        let option = tg.innerHTML;
        if (answers.find((i) => i == option)) {
            tg.classList.add("right");
        } else {
            tg.classList.add("wrong");
        }
        if (document.getElementsByClassName("right").length == answers.length) {
            document.getElementById("showHideAnswer").click();;
        }
    }
    function shuffle(array) {
        let currentIndex = array.length,
            randomIndex;
        while (currentIndex != 0) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;
            [array[currentIndex], array[randomIndex]] = [
                array[randomIndex],
                array[currentIndex],
            ];
        }
        return array;
    }
    function showAns(e) {
        pycmd("ans");
    }
</script>

{{/Reversed Choices}}
"""

card2_back_template_two_sides = """
<div id="Container">
    <div id="card">
        <div id="Q-E">
            <div id="Q">{{Answer}}</div>
            <div id="E">
                {{#Explanation}}
                <hr>{{Explanation}}{{/Explanation}}
                {{#Extra}}
                <hr>{{Extra}}{{/Extra}}
            </div>
        </div>
        <div id="A">
            <!-- Answer below -->
            {{Question}}
            <!-- Answer above -->
        </div>
    </div>
</div>

<script>
    // split questions
    var questions = document
        .getElementById("Q")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var q = document.getElementById("Q");
    q.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let x = document.createElement("div");
        x.innerHTML = questions[i];
        q.appendChild(x);
    }

    // split answers and choices
    var answers = document
        .getElementById("A")
        .innerHTML.split("|")
        .map((i) => i.trim());
    var c = document.getElementById("A");
    c.innerHTML = "";
    for (let i = 0; i < answers.length; i++) {
        let x = document.createElement("a");
        x.innerHTML = answers[i];
        x.setAttribute("class", "options");
        x.classList.add("right")
        c.appendChild(x);
    }
</script>
"""


css = """
body {
  margin: 0;
  padding: 0;
}

:root {
  font-size: 25px;
}

.mobile :root {
  font-size: 25px;
}

#Container {
  height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  border-radius: 10px;
  position: fixed;
  left: 5vw;
  right: 5vw;
  top: 10px;
  background-color: var(--background) !important;
  color: var(--font-color) !important;
  padding: 20px 10px 0 10px;
}

#card {
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 75vw;
  height: 83vh;
  padding-right: 5px;
  word-wrap: break-word;
}

#Q-E {
  width: 66vw;
  padding: 10px;
  padding-top: 20px;
  padding-bottom: 20px;
  margin-top: 20px;
  margin-bottom: 20px;
  background-color: #66a5ad;
  box-shadow: rgba(14, 13, 16, 0.2) 0px 2px 8px 0px;
  border-radius: 5px;
}

.options {
  width: 66vw;
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
  background-color: #ffffff;
  box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
}

.nightMode .options {
   background-color: grey;
}

.options:hover {
  box-shadow: rgba(14, 13, 16, 0.2) 0px 2px 8px 0px;
}

.right {
  background-color: #98fb98 !important; 
}

.wrong {
  background-color: #f08080 !important;  
}

#showHideAnswer {
  position: absolute;
  border: none;
  bottom: 0;
  width: 100%;
  border-radius: 0 0 10px 10px;
  padding: 10px 0 10px 0;
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px,
    rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
  background-color: var(--background);
}

#showHideAnswer:hover {
  box-shadow: rgba(0, 0, 0, 0.06) 0px 2px 4px 0px inset;
}

.info {
  	text-align: center;
	color: gray;
}

a {
  text-align: center;
  text-decoration: none;
  display: inline-block;
  color: inherit;
}
"""