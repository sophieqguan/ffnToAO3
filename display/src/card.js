import React, {useEffect, useState} from 'react';
import loader from './loader';
import App from './App';

function Card(work) {
    const apiURL = '/api/metadata/';

    var title = work.title;
    var url = work.url;

    const [usernameAO3, setUsernameAO3] = useState("");
    const [wordAO3, setWordAO3] = useState("");
    const [newWorkURL, setNewWorkURL] = useState("");

    async function getAO3Login () {
        hideBlock('confirm');
        hideBlock('workInfo');
        showBlock('ao3Log');
    }

    async function getAO3Session (e) {
        e.preventDefault();

        hideBlock('ao3Log');
        console.log('submitted!');
        const formData = new FormData();
        formData.append('username', usernameAO3);
        formData.append('password', wordAO3);
        formData.append('meta', JSON.stringify(work));
        showLoading();


        await fetch ('/api/AO3Login/', {
            method: 'post',
            body: formData,
        }).then( (response) => response.text()).then(data => {
            hideLoading();
            if (data === 1) {
                console.log("Sorry, I think something went wrong lmao. Let's try again.");
                showBlock('invalidLogin');
                showBlock('ao3Log');
            } else {
                setNewWorkURL(data);
                showBlock('newURL');

                updateMetaDataDisplay();
                showBlock('ao3CardLink');
                showBlock('workInfo');

                setWordAO3(""); // clear password
            }
        });
    }

    const cancelSelect = () => {
        showBlock('workList');
        hideBlock('workInfo');
    }

    const updateMetaDataDisplay = () => {
        var displayLoc = document.getElementById('metadata');
        displayLoc.innerHTML = "";
        newMeta(displayLoc, 'fandom', work.fandom);
        newMeta(displayLoc, 'chapters', work.chapters);
        newMeta(displayLoc, 'summary', work.summary);
        newMeta(displayLoc, 'published date', work.submit_date);
    }
    const newMeta = (loc, key, val) => {
        var newMeta = document.createElement('p');
        newMeta.innerText = key + ": " + val;
        loc.insertAdjacentElement('beforeend', newMeta);
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

    let text;
    const showLoading = () => {
        showBlock('loading');
        showBlock('note');
        document.getElementById("loading").classList.add("loader");
        const loadingText = new loader(document.getElementById("loadText"));
        loadingText.start();
        text = setInterval(function(){document.getElementById("loadText").innerHTML = loadingText.get()},2000);
    }

    const hideLoading = () => {
        clearInterval(text);
        hideBlock('note');
        hideBlock('loadText');
        hideBlock('loading');
    }
    
    return (
        <div class="container">
            <div class='row'>
                <div class ='col-sm-12 col-m-12 col-12'>
                    <div id='newURL' style={{display:'none'}}>tada! <a href={newWorkURL}>{title} - {usernameAO3} - archiveofourown.com</a></div>
                    <div id='invalidLogin' style={{display:'none'}}>Your password or username was wrong.</div>
                    <div id="workInfo" class="card" style={{display:'none'}}>
                        <div class="card-body">
                            <h5 class="card-title">{title}</h5>
                            <h6 class="card-subtitle mb-2 text-muted"><a href={url} class="card-link">ff.net/{title}</a></h6>
                            <h6 id='ao3CardLink' class="card-subtitle mb-2 text-muted" style={{display: 'none'}}><a href={newWorkURL} class="card-link">ao3.com/{title}</a></h6>
                            <div id='metadata' class="card-text">
                                <p> <b>Fandom</b> : {work.fandom} </p>
                                <p> <b>Chapters</b> :  {work.chapters} </p>
                                <p> <b>Summary</b> : {work.summary} </p>
                                <p> <b>Published Date</b> : {work.submit_date} </p>
                            </div>
                            <div id='confirm'>
                                <p>is this the right story?</p>
                                <button class='trans-btn' type="submit" onClick={getAO3Login}>this one alright</button>
                                <button class='trans-btn' type="cancel" onClick={cancelSelect}>no go back</button>

                            </div>
                        </div>
                    </div>
                </div>

                <div id='ao3Log' class ='col-sm-12 col-m-12 col-12' style={{display:'none'}}>
                    <div class='login'>
                        <p>Login to AO3</p>
                        <form id='ao3Form' onSubmit={getAO3Session}>
                            <p>AO3 Username: 
                            <input class='input' type='username' name='userAO3' id='userAO3' onChange={e => setUsernameAO3(e.target.value)}></input></p>
                            <p>AO3 Password: 
                            <input class='input' type='password' name='passwordAO3' id='passwordAO3' onChange={e => setWordAO3(e.target.value)}></input></p>

                            <button class='trans-btn' type="submit">Log In</button>
                        </form>
                    </div>
                </div>
                <div id="loading" style={{color:"black", paddingBottom:"1%", fontSize: "30px", display: 'none'}}>.</div>
                <div id='loadText'></div>
                <div id='note' style={{display: 'none'}}>
                    <p id='timeText'> 
                        <br/>To prevent overloading the server, each chapter takes 1 to 2 secs to be uploaded.
                        <br/>If your work is like 100 chapters, ah man....
                        <br/><br/>
                    </p>
                </div>

            </div>
        </div>
    );
}

export default Card;