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
        $('[data-toggle="tooltip"]').tooltip({
            trigger : 'hover'
        });
});

function copy_alias(full_link){
    navigator.clipboard.writeText(full_link);
}