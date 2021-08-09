/*
  Script Nossas guerreiras
  CITINOVA - Prefeitura de Fortaleza
  14/05/2021 -

*/

(function($) {
  $(document).ready(function() {

    ////// Variáveis de checagem de URL 
    let href = location.href;
    let lastUrl = href.match(/([^\/]*)\/*$/)[1];
    let url_atual = $(location).attr('href');
    var lastPath = url_atual.substring(url_atual.lastIndexOf('/') + 1);
    
    ////// Função para checar se existe string na url
    const checkExistUrl = (urlString) => window.location.href.indexOf(urlString);


    ///// Declaracao visibilidade da declação
    $('.btnDeclaracaoSde').click(function(){
      $('.declaracaoSde').toggle();
    })
    $('#decIrSde').click(function(){
      $('.formProjectName').toggle();
    })


    ///// Script mascáras dos formulários
    $('#id_data_nascimento').mask('00/00/0000');

    ///// Máscaras Telefone sem DDD
    var maskBhavior = (val) => {
      return val.replace(/\D/g, '').length === 9 ? '00000-0000' : '0000-00009';
    },
    optionTel = {
      onKeyPress: function(val, e, field, options) {
        field.mask(maskBhavior.apply({}, arguments), options);
      }
    }
    $('#id_ddd_1').mask('000');
    $('#id_ddd_2').mask('000');
    $('#id_telefone_1').mask(maskBhavior, optionTel);
    $('#id_telefone_2').mask(maskBhavior, optionTel);
    $('#id_cpf').mask('000.000.000-00');
    $('#id_cep').mask('00.000-000');
    // $('.dinheiro').mask('#.##0,00', {reverse: true});

    $(".dinheiro").maskMoney(
      { 
        showSymbol:false, 
        thousands:'.', 
        decimal:',', 
        symbolStay: false,
        allowZero: true,
    });

    $('textarea').prop('rows','6');


    ///// função formatacao dinheiro 
    const getMoney = (str) => parseInt( str.replace(/[\D]+/g,''));
    const formatReal = (int) => {
      var tmp = int+'';
      tmp = tmp.replace(/([0-9]{2})$/g, ",$1");
      if( tmp.length > 6 )
              tmp = tmp.replace(/([0-9]{3}),([0-9]{2}$)/g, ".$1,$2");
      return tmp;
    }

    ///// Função para verificar biblioteca select2
    const select2ShowOutra = (idSelect, selectVal, divIdOutra, idOutra) => {
      var select2var = $(idSelect).select2();
      console.log(selectVal);
      selectVal.find((element) => {
        if(element == "Outros, qual?"){
          console.log(element);
          $(divIdOutra).show();
        }else{
          $(divIdOutra).hide();
        }
      });
      if(selectVal.length < 1){
        $(idOutra).val('');
        $(divIdOutra).hide();
      }
    }
    
    ///// função checa se existe valor outro pra demonstrar o campo
    const checkOutraForm = (idSelect, divOutra) => {

      $(idSelect).val() == 'outro' || $(idSelect).val() == 'Outra' ? $(divOutra).show() : $(divOutra).hide();
    }

    ///// função checa marcado outra
    const changeOutra =  (varTeste, divOutra, idOutra) => {
      $(varTeste).change(function(){
        var valAtual = $(this).val();
        console.log(valAtual);
        valAtual == 'outro' || valAtual == 'Outra' ?  $(divOutra).show() : $(idOutra).val('') && $(divOutra).hide();
      })
    }


    ///// Checa url cadastro de investimento
    if(checkExistUrl("cadastro-investimento") > 0){
      const set_total = () =>{
        let valor= parseFloat($('#id_valor').val().replace('.', '').replace(',', '.'));
        let qtde = parseInt($('#id_quantidade').val());
        if (valor && qtde) {
          var total = (valor * qtde).toFixed(2)
          console.log(`${valor} valorparse`);
          $("#id-total").val(total.toString().replace('.', ','));
          console.log(`${total} total`)
        }
        if(valor == "0"){
          $("#id-total").val("0,00");
        }
      }

      $('#id_valor').keyup(set_total);
      $('#id_quantidade').keyup(set_total);

    }

    ///// Condição checa url para cadastro proposta
    if( checkExistUrl("cadastro-proposta") > 0 ) {
      
      $('#div_id_estimulo_compra label').text('Na sua opinião, o que estimula o seu cliente a comprar o seu produto?');
      $('#div_id_idade_cliente label').text('Qual a Idade dos seus clientes?');

      let idDivulgacao = `#id_divulgacao`;
      let divIdDivulgacaoOutra = `#div_id_divulgacao_outra`;
      let idDivulgacaoOutra = `#id_divulgacao_outra`;
      
      let idConcFormPag= `#id_concorrente_forma_pagamento`;
      let divIdConcFormPag = `#div_id_concorrente_forma_pagamento_outra`;
      let idConcFormPagOutr = `#id_concorrente_forma_pagamento_outra`;      
      
      checkOutraForm(idDivulgacao, divIdDivulgacaoOutra);
      changeOutra(idDivulgacao, divIdDivulgacaoOutra, idDivulgacaoOutra);

      checkOutraForm(idConcFormPag, divIdConcFormPag);
      changeOutra(idConcFormPag, divIdConcFormPag, idConcFormPagOutr);

      /// checao tipo de arquivo SETOR
      $('#id_setor').change(function(){
        var url = $("#msform").attr("data-atividades-url");
        var setorId = $(this).val();

        //ajax para pegar dado tipo de negocio referente setor
        $.ajax({
          url: url,
          data: {
            'setor': setorId
          },
          success: function (data) {
            $("#id_atividade").html(data);
          }
        });
      });

      $('#btnInvest').click(function(){
        $('#tableInvest').toggle('300');
      })

      //criação dinâmica de steps conforme a quantidade de fieldsets
      $('fieldset').each(function(i){
        let setpsVar = `step=${i}`;
        $(this).attr('id',setpsVar);
        $(this).hide();
        const arrayIcons = ['account', 'residenciais', 'financeiros', 'upload', 'confirm'];
        const arrayTexts = ['Dados do empreendimento', 'Informações do mercado I', 'Informações do mercado II', 'Investimentos', 'Finalizar']
        $("#progressbar").append(`<a class="" href="/cadastro-proposta/?${setpsVar}"><li id="${arrayIcons[i]}"><strong class="d-none d-sm-block">${arrayTexts[i]}</strong></li></a>`);

        //função clique salva form
        $("#progressbar a").click(function(){
          submitForm();
        })

        if(checkExistUrl(setpsVar) > -1){
          $(this).show();
          $("#progressbar li").addClass('active');
        }
      });

    }


    ///// Condição checa url para cadastro proponente
    if( checkExistUrl("cadastro-proponente") > 0  ) {

      var deficienciaMulti = $('.select2multiplewidget').select2();
      var multiDefGlobal = $("select#id_deficiencia").val();
      
      $("select#id_deficiencia").change(function(){
        var multiDef = $(this).val();
        if(multiDef.includes("outra")){
          $("#div_id_deficiencia_outro").show();
        }else{
          $("#id_deficiencia_outro").val('');
          $("#div_id_deficiencia_outro").hide();
        }
        if(multiDef.length < 1){
          $("#id_deficiencia_outro").val('');
          $("#div_id_deficiencia_outro").hide();
        }
      })
      
      if(multiDefGlobal.includes("outra")){
        $("#div_id_deficiencia_outro").show();
      }else{
        $("#div_id_deficiencia_outro").hide();
      }
  
      $('#div_id_deficiencia').hide();
      $("#deficienciaButton1").change(function(){ 
        if( $(this).is(":checked") ){ 
            $('#div_id_deficiencia').show() 
        }
      });
  
      $("#deficienciaButton2").change(function(){ 
        if( $(this).is(":checked") ){ 
            $("#id_deficiencia").val('');
            $('#div_id_deficiencia').hide();
            $("#id_deficiencia_outro").val('');
            $("#div_id_deficiencia_outro").hide();
            deficienciaMulti.val(null).trigger("change");
        }
      });
  
      if($("#id_deficiencia_outro").val() !== ''){
        console.log("checado nao existe");
        $("#deficienciaButton1").prop('checked', true);
        $('#div_id_deficiencia').show();
        $("#div_id_deficiencia_outro").show();
      }    
  
      if(multiDefGlobal.length > 0 ){
        $("#deficienciaButton1").prop('checked', true);
        $('#div_id_deficiencia').show();
      }else{
        $("#deficienciaButton2").prop('checked', true);
        $(".divDeficiencia").css('margin-bottom','10px');
      }

      $('#id_sexo').prop('disabled', true)
      $('.formMain').addClass("formGestora");
      $('#progressbar').addClass("progressSocia");
      $('.next').removeClass("btn-teal-300");
      $('.next').addClass("btn-pink");
      $('.alertCad').removeClass('bg-teal-light');
      $('.alertCad').addClass('bgMulher');
      $('.alertCad i').removeClass('text-main');
      $('.alertCad i').addClass('text-mulher');
      $('.btnFixoGestora').show();
      $('.radiotextsty').addClass('text-mulher');
      $('.checkmark').addClass('border-mulher');
      $('.deficienciaProp').addClass('radioMulher');      
      
      //Loop para construir steps fieldsets 
      $('fieldset').each(function(i){
        let setpsVar = `step=${i}`;
        $(this).attr('id',setpsVar);
        $(this).hide();
        const arrayIcons = ['account', 'residenciais', 'financeiros', 'upload', 'confirm'];
        const arrayTexts = ['Dados Pessoais', 'Dados Residenciais', 'Dados Socioeconômicos', 'Submissão de documentos', 'Finalizar']
        $("#progressbar").append(`<a class="" href="/cadastro-proponente/?${setpsVar}"><li id="${arrayIcons[i]}"><strong class="d-none d-sm-block">${arrayTexts[i]}</strong></li></a>`);

        if(checkExistUrl(setpsVar) > -1){
          $(this).show();
          $("#progressbar li").addClass('active');
        }
      });
    }


      $('.modelExclude').hide();
      $('.btnExclude').click(function(e){
        e.preventDefault();
        $('.modelExclude').show();
        $('.btnProjetoBlock').hide();
      })
      //form cadastro projeto
      $('.btnVoltar').click(function(e){
        e.preventDefault();
        $('.modelExclude').hide();
        $('.btnProjetoBlock').show();
      })

      $('.txtEnviando').hide();

      //SUBMIT FORM LOAD

      const submitForm = () =>{
        $(".post-form").on("submit", function(){
          $('.txtEnviando').show(100)
          $('.txtHideEviando').hide(100)
        });
        $(".btnProjeto").on("click", function(){
          $('.txtHideEviando').hide(100)
          $('.txtEnviando').show(100)
        });
      }

      submitForm();

      $('.btnHideFloat').click(function(){
        $('.btnFloat').hide();
      })
      $('.btnShowFloat').click(function(){
        $('.btnFloat').show();
      })
      
      //library FORM MULTISTEP
      var current_fs, 
      next_fs, 
      previous_fs;
      var opacity;
      $(".next").click(function(){

        current_fs = $(this).parent();
        var curStep = $(this).closest(current_fs); //fieldsets
        var curInputs = curStep.find("input[type='text'], input[type='date'], input[type='email'], input[type='file'], input[type='number'],textarea, select");
        var isValid = true;
        for (let i= 0; i< curInputs.length; i++) {
          //VERIFICA CPF AO TENTAR PASSAR NO FIELDSET
          if(!curInputs[i].validity.valid) {
            isValid = false;
            $('.msgError').show();
            $(curInputs[i]).closest(".form-control").addClass('is-invalid');
          }else{
            $(curInputs[i]).closest(".form-control").addClass('is-valid');
          }
        }
        
        //fieldset validado
        if(isValid){
          $('.msgError').hide();
          next_fs = $(this).parent().next();
      
          //Add Class Active
          $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
          
          //show the next fieldset
          next_fs.show();
          //hide the current fieldset with style
          current_fs.animate({opacity: 0}, {
          step: function(now) {
          // for making fielset appear animation
          opacity = 1 - now;
          
          current_fs.css({
          'display': 'none',
          'position': 'relative'
          });
          next_fs.css({'opacity': opacity});
          },
          duration: 600
          });
        }
      });
      
      $(".previous").click(function(){
      
      current_fs = $(this).parent();
      previous_fs = $(this).parent().prev();
      
      //Remove class active
      $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
      
      //show the previous fieldset
      previous_fs.show();
      
      //hide the current fieldset with style
      current_fs.animate({opacity: 0}, {
      step: function(now) {
      // for making fielset appear animation
      opacity = 1 - now;
      
      current_fs.css({
      'display': 'none',
      'position': 'relative'
      });
      previous_fs.css({'opacity': opacity});
      },
      duration: 600
      });
      });

    //mobile regras 
    if (parseInt($(window).width()) < 420) {
      $('.divGroupBtn').removeClass('btn-group');
      $('.divGroupBtn button').addClass('mb-2');
    }

  })  
})(jQuery);

