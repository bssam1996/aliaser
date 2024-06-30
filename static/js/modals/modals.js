// Get the modal
var create_replace_modal = document.getElementById("create_replace_modal");
var delete_modal = document.getElementById("delete_modal");
var edit_modal = document.getElementById("edit_modal");

// Get the button that opens the modal
var create_replace_btn = document.getElementById("create_replace_modal_button");

// Get the <span> element that closes the modal
var create_replace_span = document.getElementsByClassName("create-replace-modal-close")[0];
var delete_modal_span = document.getElementsByClassName("delete-modal-close")[0];
var edit_modal_span = document.getElementsByClassName("edit-modal-close")[0];

// When the user clicks on the button, open the modal
create_replace_btn.onclick = function() {
    create_replace_modal.style.display = "block";
}

function undisplay_delete(){
    delete_modal.style.display = "none";
}
function undisplay_edit(){
    // Reset
    edit_modal.style.display = "none";
    document.getElementById('edit-old-alias').value = "";
    document.getElementById('edit-new-alias').value = "";
    document.getElementById('edit-link').value = "";
    document.getElementById('edit-owner').value = "";
    document.getElementById('edit-category').value = "";
    document.getElementById('edit-site').value = "";
}

function display_delete(alias){
    delete_modal.style.display = "block";
    var delete_msg_title = document.getElementById("delete-title-message");
    delete_msg_title.innerHTML = "Are you sure you want to delete "+ alias + "?";
    document.getElementById("delete-modal-btn").setAttribute('onclick','delete_alias("' + alias +'")')
}

function display_edit(alias, link, owner, category, site){
    edit_modal.style.display = "block";

    alias = check_none(alias);
    link = check_none(link);
    owner = check_none(owner);
    category = check_none(category);
    site = check_none(site);

    document.getElementById('edit-old-alias').value = alias;
    document.getElementById('edit-new-alias').value = alias;
    document.getElementById('edit-link').value = link;
    document.getElementById('edit-owner').value = owner;
    document.getElementById('edit-category').value = category;
    document.getElementById('edit-site').value = site;
}

function check_none(str){
    if(str == "None"){
        return ""
    }
    return str
}
// When the user clicks on <span> (x), close the modal
create_replace_span.onclick = function() {
    create_replace_modal.style.display = "none";
}
delete_modal_span.onclick = function() {
    undisplay_delete();
}
edit_modal_span.onclick = function() {
    undisplay_edit();
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == create_replace_modal) {
    create_replace_modal.style.display = "none";
  }else if (event.target == delete_modal){
    delete_modal.style.display = "none";
  }else if (event.target == edit_modal){
    edit_modal.style.display = "none";
  }
}


function add_alias(replace=false){
    alias = document.getElementById('alias').value;
    link = document.getElementById('link').value;
    owner = document.getElementById('owner').value;
    category = document.getElementById('category').value;
    site = document.getElementById('site').value;

    errormsg = document.getElementById('error_create_replace');

    if(alias.length == 0){
        errormsg.innerHTML = `Alias is required`;
        return
    }
    if(link.length == 0){
        errormsg.innerHTML = `Link is required`;
        return
    }
    if(validateUrl(link) == 0){
        errormsg.innerHTML = `Link must start with http:// or https://`;
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
                site: site,
             },
        success: function (data) {
            console.log(`${data.responseText}`);
            errormsg.innerHTML = "";
            reset();
            create_replace_span.click();
            location.reload();
        },
        error: function (err) {
            console.log(`${err.responseText}`);
            errormsg.innerHTML = `${err.responseText}`;
        }
    });
}

function edit_alias(){
    old_alias = document.getElementById('edit-old-alias').value;
    new_alias = document.getElementById('edit-new-alias').value;
    link = document.getElementById('edit-link').value;
    owner = document.getElementById('edit-owner').value;
    category = document.getElementById('edit-category').value;
    site = document.getElementById('edit-site').value;

    errormsg = document.getElementById('error_edit');

    if(old_alias.length == 0){
        errormsg.innerHTML = `Alias is required`;
        return
    }
    if(new_alias.length == 0){
        errormsg.innerHTML = `Alias is required`;
        return
    }
    if(link.length == 0){
        errormsg.innerHTML = `Link is required`;
        return
    }
    if(validateUrl(link) == 0){
        errormsg.innerHTML = `Link must start with http:// or https://`;
        return
    }

    $.ajax({
        url: './edit',
        type: "POST",
        data: { 
                old_alias: old_alias,
                new_alias: new_alias,
                link: link,
                owner: owner,
                category: category,
                site: site,
             },
        success: function (data) {
            console.log(`${data.responseText}`);
            errormsg.innerHTML = "";
            undisplay_edit();
            location.reload();
        },
        error: function (err) {
            console.log(`${err.responseText}`);
            errormsg.innerHTML = `${err.responseText}`;
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
    document.getElementById('site').value = "";
}

function delete_alias(alias){
    $.ajax({
        url: './delete/' + alias,
        type: "DELETE",
        success: function (data) {
            // Delete TD Row
            dt = document.getElementById("keys_table");
            dt.querySelector(`[data-row-id="${alias}"]`).remove();
            delete_modal_span.click();
        },
        error: function (err) {
            console.log(`${err.responseText}`);
            alert(err.responseText);
        }
    });
}