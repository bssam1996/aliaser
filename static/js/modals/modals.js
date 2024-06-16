// Get the modal
var create_replace_modal = document.getElementById("create_replace_modal");

// Get the button that opens the modal
var create_replace_btn = document.getElementById("create_replace_modal_button");

// Get the <span> element that closes the modal
var create_replace_span = document.getElementsByClassName("create-replace-modal-close")[0];

// When the user clicks on the button, open the modal
create_replace_btn.onclick = function() {
    create_replace_modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
create_replace_span.onclick = function() {
    create_replace_modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == create_replace_modal) {
    create_replace_modal.style.display = "none";
  }
}


function add_alias(replace=false){
    alias = document.getElementById('alias').value;
    link = document.getElementById('link').value;
    owner = document.getElementById('owner').value;
    category = document.getElementById('category').value;

    errormsg = document.getElementById('error_create_replace');
    successmsg = document.getElementById('success_create_replace');

    if(alias.length == 0){
        errormsg.innerHTML = `Alias is required`;
        successmsg.innerHTML = "";
        return
    }
    if(link.length == 0){
        errormsg.innerHTML = `Link is required`;
        successmsg.innerHTML = "";
        return
    }
    if(validateUrl(link) == 0){
        errormsg.innerHTML = `Link must start with http:// or https://`;
        successmsg.innerHTML = "";
        return
    }

    url_link = "add"

    if(replace){
        url_link = "replace"
    }

    $.ajax({
        url: './' + url_link,
        type: "POST",
        data: { 
                alias: alias,
                link: link,
                owner: owner,
                category: category,
             },
        success: function (data) {
            console.log(`${data.responseText}`);
            errormsg.innerHTML = "";
            successmsg.innerHTML = "Done";
            reset();
        },
        error: function (err) {
            console.log(`${err.responseText}`);
            errormsg.innerHTML = `${err.responseText}`;
            successmsg.innerHTML = "";
        }
    });
}

function validateUrl(url) {
    // Define the regular expression to check if the URL starts with "http" or "https"
    const regex = /^https?:\/\//;
    // Test the URL against the regex
    return regex.test(url);
}

function reset(){
    document.getElementById('alias').value = "";
    document.getElementById('link').value = "";
    document.getElementById('owner').value = "";
    document.getElementById('category').value = "";
}
