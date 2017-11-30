  function addRule()
       {
            var html= '<div class="form-row rule">  \
                        <div class="col-3 ">    \
                            <label>Процент скидки</label>  \
                            <input type="number" min="0" class="form-control discount" placeholder="Процент скидки"> \
                        </div> \
                        <div class="col-3 "> \
                            <label>Необходимые накопления</label> \
                            <input type="number" min="0" class="form-control accum" placeholder="Необходимые накопления"> \
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


       function sendSettings(cmd, algorithm, data)
       {
            var rules = makeDiscountRules();
            //var form_data = $('#bonus-form').serializeArray();
           // $.each(form_data, function(index, value){
            //        data[value['name']] = value['value'];
            //    });
           // data['rules']=rules;
            $.ajax({
            url: '/settings/',
            type: "POST",
            data: {
                "cmd": cmd,
              "data": JSON.stringify(data),
              "algorithm": algorithm
            },
            dataType: "html",
            success: function (data) {
              if (data) {
               $('#settingsContent').empty();
                 $('#settingsContent').append(data);
                  $(document).change();

                }}
              });
    }





$(document).ready( function(){

    sendSettings('get', '', '');

    });


    $(document).on('change', '#id_algorithm', function() {
        sendSettings('update', $('#id_algorithm').val(), '');
        if ($('#id_algorithm').val() == 'discount')
        {
            $('#discount-rules-controls').show();
         }
         else
         {
            $('#discount-rules-controls').hide();
          }
        });
