import './App.css';
import React, {useState} from 'react';
import card from './card';

function App() {
  // USERNAME (FFN)
  const [usernameFFN, setUsernameFFN] = useState("");
  // ID, TITLE, URL
  const [selectedWork, setSelectedWork] = useState([]);
  var works = [];

  async function getWorks(e) {
    // console.log("[DISPLAY WORK]");
    e.preventDefault();

    showBlock('greeting');
    showBlock('reload');
    hideBlock('ffn-user');
    const formData = new FormData();
    formData.append('username', usernameFFN);

    await fetch ('/api/ffn/', {
        method: 'post',
        body: formData,
    }).then( (response) => response.json()).then(data => {
      works = data;
      // console.log(data);
      displayWorks();
    });
    
  }

  const displayWorks = () => {
    hideBlock('submitBtn');
    var len = (Object.keys(works).length) / 2;
    var list = document.getElementById('workList');
    if (len == 0) list.innerHTML = "<b>Empty or Invalid user</b><br/><p class='tinyText'>unless this is what you want...? weird flex but ok</p>";
    else {
      list.innerHTML = "<b>Select a work:</b>";
      for (let i = 0; i < len; i++) {
        newTitle(list, i + 1, works[2 * i]);
      }
    }
  }
  
  const newTitle = (list, number, title) => {
    var workElement = document.createElement('div');
    workElement.id = number;
    workElement.className = 'workTitle';
    workElement.innerHTML = number + ". " + title;
    workElement.onclick = function() {showInfo(number - 1)};

    list.insertAdjacentElement('beforeend', workElement);
  }

  const hideBlock = (id) => {
    // console.log("hide!");
    var block = document.getElementById(id);
    block.style.display = "none";
  }

  const showBlock = (id) => {
    // console.log("show!");
    var block = document.getElementById(id);
    block.style.display = "";
  }

  async function showInfo (id) {
    var selected = [id, works[2 * id], works[2 * id + 1]];
    setSelectedWork(selected);
    // console.log(selectedWork);
    // console.log("show info for " + id);
    hideBlock('workList');
    showBlock('workInfo');
  }

  

  return (
    <div className="App">
      <h1>HELLO</h1>
      <p id='intro'>Welcome to FTO3, transferring works on <a href="https://www.fanfiction.net/">fanfiction.net</a> to <a href="https://archiveofourown.org/">archiveofourown</a>.<br/> psst don't forget to go update that fic you haven't updated in like, 5 years.</p>
      <p id='greeting' style={{display:'none'}}>currently browsing as <b>{usernameFFN}</b> (ffn)</p>
      <div id='reload' style={{display: 'none'}}><button class='trans-btn' onClick={() => window.location.reload(false)}>start over</button></div>
      <form id='ffn-user' onSubmit={getWorks}>
        <p> 
            Your Fanfiction.net Username: <br/>
            <input class='input' id="username" type="username" name="username" onChange={e => setUsernameFFN(e.target.value)}/>
        </p>

        <button class='trans-btn' id="submitBtn" type="submit">search</button>
      </form>
      <div id="mainDisplay">
        <div id="workList" style={{textAlign:"left"}}></div>
        {card(selectedWork)}
        <div id="mainWork"></div>
      </div>

      <a id="credit" href="https://github.com/clostone/ffnToAO3">@clostone</a>
    </div>
  );
}

export default App;
