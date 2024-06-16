// new DataTable('#example', {
//     searching: true
// });
$(document).ready(function(){
    let dataTable = new DataTable('#keys_table', {
        info: true,
        ordering: true,
        paging: true,
        columnDefs: [
            { "orderable": false, "targets": 5 }
        ]
        });
});



function delete_alias(alias){

    console.log("Delete Function");

    $.ajax({
        url: './delete/' + alias,
        type: "DELETE",
        success: function (data) {
            // Delete TD Row
            dt = document.getElementById("keys_table");
            dt.querySelector(`[data-row-id="${alias}"]`).remove();
        },
        error: function (err) {
            console.log(`${err.responseText}`);
            alert(err.responseText);
        }
    });
}