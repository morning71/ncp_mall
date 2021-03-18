// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    // "ordering": false,  /*关闭插件自带排序*/
    "pageLength": 40,      /*每页数目*/
    language: {
        // "sProcessing": "处理中...",
        "sLengthMenu": "显示 _MENU_ 条记录",
        "sZeroRecords": "没有匹配结果",  //无数据时显示的内容
        "sInfo": "显示第 _START_ 至 _END_ 条记录，共 _TOTAL_ 条订单",
        "sInfoEmpty": "显示第 0 至 0 条记录，共 0 条",  //数据为空时显示的内容
        "sInfoFiltered": "(由 _MAX_ 条记录过滤)",
        // "sInfoPostFix": "",
        "sSearch": "搜索:",
        // "sUrl": "",
        "sEmptyTable": "表中数据为空",   //无数据时的显示结果
        // "sLoadingRecords": "载入中...",
        // "sInfoThousands": ",",
        "oPaginate": {
            // "sFirst": "首页",
            "sPrevious": "<",
            "sNext": ">",
            // "sLast": "末页"
         },
        // "oAria": {
            // "sSortAscending": ": 以升序排列此列",
            // "sSortDescending": ": 以降序排列此列"
        // }
    }
  });
});
