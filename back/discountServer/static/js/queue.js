    var buffer= '';
    var start = 0;
    var count = 10;
    var total =3;
    var elems_end = false;
    var selection_parameters ={
        "sort": "date",
        "card": "",
        "document_close_user": "",
        "dateFrom": "",
        "dateTo": "",
        "doc_number": "",
        "session": "",
        "shop": "",
        "workplace": "",
        "type": "",
    };

    function emptyIfNull(val)
    {
        if ((val== null) || (val == 0)){
        return "-"
        } else {
        return val;
        }
    }

    // Устанавливаем строку поиска
    $('#dateFrom').change(function(){
        selection_parameters["dateFrom"] = $(this).val();
    });

    $('#dateTo').change(function(){
        selection_parameters["dateTo"] = $(this).val();
    });

     // Устанавливаем порядок сортировки
    $('#type').change(function(){
        selection_parameters["type"] = $(this).val();
    });

    $('#doc_close_user').change(function(){
        selection_parameters["doc_close_user"] = $(this).val();
    });

    $('#card').change(function(){
        selection_parameters["card"] = $(this).val();
    });
    $('#doc_number').change(function(){
        selection_parameters["doc_number"] = $(this).val();
    });
    $('#session').change(function(){
        selection_parameters["session"] = $(this).val();
    });
    $('#shop').change(function(){
        selection_parameters["shop"] = $(this).val();
    });
    $('#workplace').change(function(){
        selection_parameters["workplace"] = $(this).val();
    });





$(document).ready(function(){
        dataUpdate();

        //$('#data').css('margin-top', '200px');
});


function dataUpdate(){
    var cmd = "update";
    start= 0;
    count= 10;
    var data = {
            "start": start,
            "count": count,
        }

     $.ajax({
        url: '/queue/',
        type: "POST",
        data: {
          "cmd": cmd,
          "data": JSON.stringify(data),
          "selection_parameters": JSON.stringify(selection_parameters)
        },
        dataType: "json",
        success: function (data) {
          if (data.result) {
            if (data.result == "ok"){
                $('#tbody').empty();
                total = data.total;
                if (total < count){
                count = total;
                }
                $('#total').text(start+count + ' из ' + total);

                $.each(data.data, function(index, value){
                /*
                          "execution_date": task.execution_date.strftime('%Y-%m-%d / %H:%M'),
                            "queue_date": task.queue_date.strftime('%Y-%m-%d / %H:%M'),
                            "operation": task.operation,
                            "card": task.card.code,
                            "sum": task.transaction.sum,
                            "shop": task.transaction.shop,
                            "workplace": task.transaction.workplace,
                            "session": task.transaction.session,
                            "doc_number": task.transaction.doc_number,

                */
                   var html = $('#tbody').append("<tr></tr>");
                     $(html).append("<td>"+emptyIfNull(value["execution_date"])+"</td>");
                     $(html).append("<td>"+emptyIfNull(value["queue_date"])+"</td>");
                      $(html).append("<td>"+emptyIfNull(value["operation"])+"</td>");
                       $(html).append("<td>"+emptyIfNull(value["card"])+"</td>");
                        $(html).append("<td>"+emptyIfNull(value["sum"])+"</td>");
                         $(html).append("<td>"+emptyIfNull(value["shop"])+"</td>");
                          $(html).append("<td>"+emptyIfNull(value["workplace"])+"</td>");
                           $(html).append("<td>"+emptyIfNull(value["session"])+"</td>");
                            $(html).append("<td>"+emptyIfNull(value["doc_number"])+"</td>");
                });
             start = start + count;
                    if (start > total)
                    {
                        start = start - count;
                        elems_end = true;
                    }
            }
            else
            {
               alert("Ошибка!");
            }
         }
        }
      });
}

function dataAdd(){
if (elems_end)
    {
        return;
    }
    var cmd = "update";
    if (start+count > total)
    {
        count = total - start;
        }

    var data = {
            "start": start,
            "count": count,
        }

     $.ajax({
        url: '/transactions/',
        type: "POST",
        data: {
          "cmd": cmd,
          "data": JSON.stringify(data),
          "selection_parameters": JSON.stringify(selection_parameters)
        },
        dataType: "json",
        success: function (data) {
          if (data.result) {
            if (data.result == "ok"){
               total = data.total;
                $('#total').text(start+count + ' из ' + total);
                $.each(data.data, function(index, value){
                /*


                */
                   var html = $('#tbody').append("<tr></tr>");
                     $(html).append("<td>"+emptyIfNull(value["execution_date"])+"</td>");
                     $(html).append("<td>"+emptyIfNull(value["queue_date"])+"</td>");
                      $(html).append("<td>"+emptyIfNull(value["operation"])+"</td>");
                       $(html).append("<td>"+emptyIfNull(value["card"])+"</td>");
                        $(html).append("<td>"+emptyIfNull(value["sum"])+"</td>");
                         $(html).append("<td>"+emptyIfNull(value["shop"])+"</td>");
                          $(html).append("<td>"+emptyIfNull(value["workplace"])+"</td>");
                           $(html).append("<td>"+emptyIfNull(value["session"])+"</td>");
                            $(html).append("<td>"+emptyIfNull(value["doc_number"])+"</td>");
                });
                start = start + count;
                    if (start > total)
                    {
                        start = start - count;
                        elems_end = true;
                    }
            }
            else
            {
               alert("Ошибка!");
            }
         }
        }
      });
}



function clearFilter(){
    selection_parameters ={
        "sort": "date",
        "card": "",
        "document_close_user": "",
        "dateFrom": "",
        "dateTo": "",
        "doc_number": "",
        "session": "",
        "shop": "",
        "workplace": "",
        "type": "",
    };
    start = 0;
    count = 10;
    $('#dateFrom').val("");
    $('#dateTo').val("");
    $('#type').val("");
    $('#doc_close_user').val("");
    $('#card').val("");
    $('#doc_number').val("");
    $('#session').val("");
    $('#shop').val("");
    $('#workplace').val("");
    dataUpdate();
}

$(window).scroll(function()
{
     if  ($(window).scrollTop() +$(window).height() >= $(document).height())
     {
          dataAdd();
     }
});