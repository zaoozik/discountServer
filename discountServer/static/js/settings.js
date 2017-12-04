  var cur_alg = null;

  function addRule(dis, accum)
       {
            var html= '<div class="form-row rule">  \
                        <div class="col-3 ">    \
                            <label class="form-control-sm">Процент скидки</label>  \
                            <input type="number" min="0"  value="' + dis + '" \
                            class="form-control form-control-sm discount" placeholder="Процент скидки"> \
                        </div> \
                        <div class="col-3 "> \
                            <label class="form-control-sm">Необходимые накопления</label> \
                            <input type="number" min="0" value="' + accum + '" \
                             class="form-control form-control-sm accum" placeholder="Необходимые накопления"> \
                        </div> \
                    </div>';
            $('#discount-rules').append(html);
       }

        function remRule()
       {

            $('.rule').last().remove();
       }


       function makeDiscountRules()
       {
            var rules_list = {};
            $.each($('.rule'), function(index, value){
                    var dis = value.children[0].getElementsByClassName("discount")[0].value;
                    var accum = value.children[1].getElementsByClassName("accum")[0].value;
                    rules_list[dis] = parseFloat(accum);
            });
            return rules_list;
       }


       function sendSettings(cmd, type)
       {
            var data = {};
            if (type == 'discount')
            {
                var rules = makeDiscountRules();
                var form_data = $('#bonus-form').serializeArray();
                $.each(form_data, function(index, value){
                        data[value['name']] = value['value'];
                    });
                data['rules']=rules;
            }
             if (type == 'workplace')
            {
                $('#CashBoxModal').modal('hide');
                var form_data = $('#CashBoxForm').serializeArray();
                $.each(form_data, function(index, value){
                        data[value['name']] = value['value'];
                    });
            }

            $.ajax({
            url: '/settings/'+type+'/',
            type: "POST",
            data: {
                "cmd": cmd,
              "data": JSON.stringify(data),
              "algorithm": $('#id_algorithm').val()
            },
            dataType: "json",
            success: function (data) {
              if (data.html) {

               $('#'+type).empty();
                 $('#'+type).append(data.html);
                  $(document).change();

                }
                if (data.algorithm)
                {
                    if (($('#id_algorithm').val() == 'discount') || ($('#id_algorithm').val() == 'combo'))
                    {
                        $('#discount-rules-controls').show();
                        $('#discount-label').show();
                     }
                     else
                     {
                        $('#discount-rules-controls').hide();
                        $('#discount-label').hide();
                      }
                }
                if (data.rules)
                {
                    var rules_list = {};
                    $.each(data.rules, function(index, value){
                            addRule(index, value);

                    });
                    return rules_list;
                }
                if (data.result)
                {
                    if (data.result == "ok")
                    {
                        alert('Сохранено');
                        sendSettings('get', type);
                    }
                }

             }
              });
    }


 function deleteWorkplace(key)
       {
            var data = {};
            data = {'key':key};
            cmd = 'delete';
            type = 'workplace';

            $.ajax({
            url: '/settings/'+type+'/',
            type: "POST",
            data: {
                "cmd": cmd,
              "data": JSON.stringify(data),
            },
            dataType: "json",
            success: function (data) {
              if (data.result) {
                  if (data.result == "ok")
                        {
                            sendSettings('get', type);
                        }
              }


              }});
    }



$(document).ready( function(){

    sendSettings('get', 'discount');
    sendSettings('get', 'workplace');
    sendSettings('get', 'org');
    });


    $(document).on('change', '#id_algorithm', function() {
        sendSettings('update', 'discount');


        });
