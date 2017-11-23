    var buffer= '';
    var start = 0;
    var count = 10;
    var total =3;
    var elems_end = false;
    var selection_parameters ={
        "sort": "code",
        "search": "",
        "deleted": "n",
    };

    // Устанавливаем строку поиска
    $('#search').change(function(){
        selection_parameters["search"] = $(this).val();
    });

     // Устанавливаем порядок сортировки
    $('#sort').change(function(){
        selection_parameters["sort"] = $(this).val();
    });

    //Включая/выключая удаленных
    $('#showDeleted').change(function(){
        if ($(this).is(':checked')){
            selection_parameters["deleted"] = "y";
            } else {
            selection_parameters["deleted"] = "n";
            }
    });

    $('html').keydown(function(e){ //отлавливаем нажатие клавиш

        if (e.keyCode == 13) {
            if (! $('#addCardModal').hasClass("show"))
            {
            $(document).click();
            $('#addCardButton').click();}

            $('#addCardCode').val(buffer);
            $("#one").on("input", function() {

                setTimeout(function(){
                $("#addCardCode").focus();
                    }, 2);

});
            buffer= '';
            }
    if (is_numeric(String.fromCharCode(e.keyCode))){
            buffer+=String.fromCharCode(e.keyCode);}
});

function saveCard(){
    var code= $("#id_code").val();
    var holder_name = $("#id_holder_name").val();
    var card_data = {
                        "code": $('#id_code').val(),
                        "holder_name": $('#id_holder_name').val(),
                        "accumulation":  $('#id_accumulation').val(),
                        "bonus": $('#id_bonus').val(),
                        "discount":  $('#id_discount').val(),
                        "type": $('#id_type').val()
                        }
    var cmd = "save";

    $.ajax({
        url: '/cards/maintenance/',
        type: "POST",
        data: {
          "cmd": cmd,
          "data": JSON.stringify(card_data)
        },
        dataType: "json",
        success: function (data) {
          if (data.result) {
            if (data.result == "ok"){
                window.location.href = window.location.href;
            }
            else
            {
               alert("Ошибка!");
            }
         }
        }
      });

}

function clearForm(){
          $('#id_code').val('');
           $('#id_holder_name').val('');
            $('#id_accumulation').val(0);
            $('#id_bonus').val(0);
            $('#id_discount').val(0);
            $('#id_type').val('');
                      $('#id_reg_date').val('');
                       $('#id_changes_date').val('');
                        $('#id_last_transaction_date').val('');
}

function getCard(card_code)
{
    var card_data = {"code": card_code}
    var cmd = "get";
    var cData;

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

function deleteCard(){

    var select = $('.cardcode:checked');
    if (select.length == 0)
    {return;}

    var card_codes = [];

    $.each(select, function(i, item){
     card_codes[card_codes.length] = item.attributes["id"].value;
    }
    );


    var cmd = "delete";

    $.ajax({
        url: '/cards/maintenance/',
        type: "POST",
        data: {
          "cmd": cmd,
          "data": JSON.stringify(card_codes)
        },
        dataType: "json",
        success: function (data) {
          if (data.result) {
            if (data.result == "ok"){
                window.location.href = '../cards/';
            }
            else
            {
               alert("Ошибка!");
            }
         }
        }
      });

}
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
        url: '/cards/',
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
                    var tr='';
                    if (value["deleted"] == 'y')
                    {
                       tr = '<tr style="color: red; text-decoration:line-through;">'
                    }
                    else
                    {
                        tr = '<tr>'
                    }
                    /*var html = document.createElement('tr');
                     var td = document.createElement('td');
                     $(td).add('index').prop('type','checkbox');
                     $(html).add(td);
                     $(html).add('td').text(value["code"]);
                     $(html).add('td').text(value["accumulation"]);*/
                     var html = tr+
                         '<td><input class="cardcode" type="checkbox" id="' + value["code"] + '"></td> \
                         <td>' + value["code"] + '</td> \
                         <td>' + value["type"] + '</td> \
                         <td>' + value["holder_name"] + '</td> \
                         <td><button data-toggle="modal" data-target="#CardModal" type="button" onclick="getCard(';
                         html += "'" + value["code"] + "'";
                          html += ');" class="fa fa-eye" aria-hidden="true" title="Просмотр"></button></td> \
                            </tr> ';
                     //alert(html);
                    $('#tbody').append( html);
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
        url: '/cards/',
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
                    var tr='';
                    if (value["deleted"] == 'y')
                    {
                       tr = '<tr style="color: red; text-decoration:line-through;">'
                    }
                    else
                    {
                        tr = '<tr>'
                    }

                    var html = tr+
                         '<td><input class="cardcode" type="checkbox" id="' + value["code"] + '"></td> \
                         <td>' + value["code"] + '</td> \
                         <td>' + value["type"] + '</td> \
                         <td>' + value["holder_name"] + '</td> \
                         <td><button data-toggle="modal" data-target="#CardModal" type="button" onclick="getCard(';
                         html += "'" + value["code"] + "'";
                          html += ');" class="fa fa-eye" aria-hidden="true" title="Просмотр"></button></td> \
                            </tr> ';
                     //alert(html);
                    $('#tbody').append(html);
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
        "sort": "code",
        "search": "",
        "deleted": "n",
    };
    $('#showDeleted').prop('checked', false);
    start = 0;
    count = 10;
    dataUpdate();
}

$(window).scroll(function()
{
     if  ($(window).scrollTop() +$(window).height() >= $(document).height())
     {
          dataAdd();
     }
});