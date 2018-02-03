    var buffer= '';
    var start = 0;
    var count = 50;
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
    count= 50;
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
                $('#tbody').empty();
                total = data.total;
                if (total < count){
                count = total;
                }
                $('#total').text(start+count + ' из ' + total);

                $.each(data.data, function(index, value){
                /*
                          <th>Дата/время</th>
                            <th>Тип</th>
                            <th>Код карты</th>
                            <th>Накопления</th>
                            <th>Бонусов до операции</th>
                            <th>Начисление бонусов</th>
                            <th>Списание бонусов</th>
                            <th>Номер магазина</th>
                            <th>Рабочее место</th>
                            <th>Номер документа</th>
                            <th>Номер смены</th>
                            <th>Пользователь</th>

                */
                   var html = $('#tbody').append("<tr></tr>");
                     $(html).append("<td>"+emptyIfNull(value["date"])+"</td>");
                     $(html).append("<td>"+emptyIfNull(value["type"])+"</td>");
                       $(html).append("<td><a href='#' onclick='showCard("+ '"'+value["card"]+'"'+");'>"+ emptyIfNull(value["card"])+"</a></td>");
                       $(html).append("<td>"+emptyIfNull(value["sum"])+"</td>");
                        $(html).append("<td>"+emptyIfNull(value["bonus_before"])+"</td>");
                         $(html).append("<td>"+emptyIfNull(value["bonus_add"])+"</td>");
                          $(html).append("<td>"+emptyIfNull(value["bonus_reduce"])+"</td>");
                           $(html).append("<td>"+emptyIfNull(value["shop"])+"</td>");
                            $(html).append("<td>"+emptyIfNull(value["workplace"])+"</td>");
                             $(html).append("<td>"+emptyIfNull(value["doc_number"])+"</td>");
                              $(html).append("<td>"+emptyIfNull(value["session"])+"</td>");
                               $(html).append("<td>"+emptyIfNull(value["doc_close_user"])+"</td>");
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
                          <th>Дата/время</th>
                            <th>Тип</th>
                            <th>Код карты</th>
                            <th>Накопления</th>
                            <th>Бонусов до операции</th>
                            <th>Начисление бонусов</th>
                            <th>Списание бонусов</th>
                            <th>Номер магазина</th>
                            <th>Рабочее место</th>
                            <th>Номер документа</th>
                            <th>Номер смены</th>
                            <th>Пользователь</th>

                */
                   var html = $('#tbody').append("<tr></tr>");
                     $(html).append("<td>"+emptyIfNull(value["date"])+"</td>");
                     $(html).append("<td>"+emptyIfNull(value["type"])+"</td>");
                      $(html).append("<td><a href='#' onclick='showCard("+ '"'+value["card"]+'"'+");'>"+ emptyIfNull(value["card"])+"</a></td>");
                       $(html).append("<td>"+emptyIfNull(value["sum"])+"</td>");
                        $(html).append("<td>"+emptyIfNull(value["bonus_before"])+"</td>");
                         $(html).append("<td>"+emptyIfNull(value["bonus_add"])+"</td>");
                          $(html).append("<td>"+emptyIfNull(value["bonus_reduce"])+"</td>");
                           $(html).append("<td>"+emptyIfNull(value["shop"])+"</td>");
                            $(html).append("<td>"+emptyIfNull(value["workplace"])+"</td>");
                             $(html).append("<td>"+emptyIfNull(value["doc_number"])+"</td>");
                              $(html).append("<td>"+emptyIfNull(value["session"])+"</td>");
                               $(html).append("<td>"+emptyIfNull(value["doc_close_user"])+"</td>");
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
    count = 50;
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


function showCard(card_code)
{
    var card_data = {"code": card_code}
    var cmd = "get";
    var cData;
    $('#CardModal').modal('show');

    $.ajax({
        url: '/cards/maintenance/',
        type: "POST",
        data: {
          "cmd": cmd,
          "data": JSON.stringify(card_data)
        },
        dataType: "json",
        success: function (response) {
          if (response.result) {
            if (response.result == "ok"){
                cData = response.data;
                $('#id_code').val(cData.code);
                 $('#id_holder_name').val(cData.holder_name);
                  $('#id_holder_phone').val(cData.holder_phone);
                  $('#id_accumulation').val(cData.accumulation);
                   $('#id_bonus').val(cData.bonus);
                    $('#id_discount').val(cData.discount);
                     $('#id_type').val(cData.type);
                      $('#id_reg_date').val(cData.reg_date);
                       $('#id_changes_date').val(cData.changes_date);
                        $('#id_last_transaction_date').val(cData.last_transaction_date);

            }
            else
            {
               alert(data.msg);
            }
         }
        }
      });
}



$(window).scroll(function()
{
     if  ($(window).scrollTop() +$(window).height() >= $(document).height())
     {
          dataAdd();
     }
});
