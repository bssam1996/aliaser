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